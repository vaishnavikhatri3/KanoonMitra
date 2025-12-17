import os
import pandas as pd
import numpy as np
import faiss
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai

# =====================================================
# ENV SETUP
# =====================================================
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

# =====================================================
# PATHS
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EMB_DIR = os.path.join(BASE_DIR, "embeddings")

# =====================================================
# LOAD DATA (FROM REPO)
# =====================================================
df = pd.read_pickle(os.path.join(EMB_DIR, "bns.pkl"))
index = faiss.read_index(os.path.join(EMB_DIR, "faiss_index.bin"))
mapping_df = pd.read_csv(os.path.join(DATA_DIR, "BNStoIPC.csv"))

# =====================================================
# MODELS
# =====================================================
bns_model = SentenceTransformer("all-MiniLM-L6-v2")

# =====================================================
# HELPERS
# =====================================================
def get_ipc_equivalents_with_description(bns_section):
    section = str(bns_section).strip()
    mapping_df["BNS Sections"] = mapping_df["BNS Sections"].astype(str).str.strip()

    rows = mapping_df[mapping_df["BNS Sections"] == section]
    if rows.empty:
        return []

    ipc_sections = rows["IPC Sections"].values[0].split(",")
    ipc_sections = [s.strip() for s in ipc_sections]

    result = []
    for ipc in ipc_sections:
        row = mapping_df[
            mapping_df["IPC Sections"].astype(str).str.strip() == ipc
        ]
        desc = (
            row.iloc[0].get("IPC Description", "")
            if not row.empty
            else "No description available."
        )
        result.append((ipc, desc))

    return result


def get_case_reference_links(query):
    try:
        url = f"https://indiankanoon.org/search/?formInput={query.replace(' ', '+')}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        links = []
        for a in soup.select("div.result_title > a")[:3]:
            links.append(f"{a.text.strip()} - https://indiankanoon.org{a['href']}")

        return links if links else ["No relevant cases found."]
    except Exception:
        return ["Error fetching case references."]

# =====================================================
# MAIN FUNCTION
# =====================================================
def generate_final_response(user_query):
    # -------- Semantic Search --------
    query_vec = bns_model.encode([user_query])
    _, indices = index.search(np.array(query_vec), k=3)

    results = df.iloc[indices[0]][
        ["Section", "Section _name", "Description"]
    ].to_dict(orient="records")

    joined_sections = "\n".join(
        [
            f"Section {r['Section']}: {r['Section _name']} - {r['Description']}"
            for r in results
        ]
    )

    # -------- SUMMARY PROMPT --------
    summary_prompt = f"""
You are an Indian legal expert.

Based on the following Bharatiya Nyaya Sanhita (BNS) sections:
{joined_sections}

Explain in plain English:
- What type of offence this is
- Whether it is serious or minor
"""

    # -------- ADVICE PROMPT --------
    advice_prompt = f"""
A citizen reports the following issue:
"{user_query}"

Based on Indian criminal procedure, explain:
- What immediate steps the citizen should take
- Whether filing an FIR is appropriate
- Any safety or documentation advice
"""

    # -------- GEMINI CALLS --------
    try:
        summary_resp = client.models.generate_content(
            model="models/gemma-3-12b-it",
            contents=summary_prompt
        )
        summary = summary_resp.text
    except Exception as e:
        summary = f"Summary generation failed: {e}"

    try:
        advice_resp = client.models.generate_content(
            model="models/gemma-3-12b-it",
            contents=advice_prompt
        )
        advice = advice_resp.text
    except Exception as e:
        advice = f"Advice generation failed: {e}"

    # -------- EXTRA OUTPUTS --------
    ipc_output = ""
    bns_desc_output = ""
    case_links_output = ""

    for r in results:
        ipc_map = get_ipc_equivalents_with_description(r["Section"])
        for ipc, desc in ipc_map:
            ipc_output += f"BNS {r['Section']} → IPC {ipc}\n"

        bns_desc_output += (
            f"{r['Section']} - {r['Section _name']}:\n{r['Description']}\n\n"
        )

        case_links_output += "\n".join(
            get_case_reference_links(f"{r['Section _name']} {r['Section']}")
        ) + "\n\n"

    return {
        "summary": summary,
        "advice": advice,
        "ipc_mapping": ipc_output,
        "bns_descriptions": bns_desc_output,
        "case_links": case_links_output,
    }
