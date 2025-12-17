⚖️ KanoonMitra
An AI-Powered Legal Assistant for Indian Law

📌 Overview
KanoonMitra is an AI-powered legal assistance web application designed to help Indian citizens understand legal issues in simple and accessible language.
Users can describe a legal problem in natural language (English or Hinglish), and the system:
Identifies relevant Bharatiya Nyaya Sanhita (BNS) sections
Generates a plain-English legal summary
Provides actionable legal advice
Maps modern BNS sections to Indian Penal Code (IPC) sections
Fetches related case law references

The application combines Machine Learning, Semantic Search, and Large Language Models (LLMs) with a clean Streamlit-based UI

🚀 Key Features
Natural language legal query input
Semantic search over BNS sections (not keyword-based)
Plain-English legal summaries
Step-by-step legal guidance
BNS → IPC section mapping
Case reference links from Indian Kanoon
Secure API key handling
Clean, citizen-friendly UI

🧠 System Architecture
User Query
   ↓
Sentence Transformer (Embeddings)
   ↓
FAISS Vector Similarity Search
   ↓
Relevant BNS Sections
   ↓
Large Language Model (Gemini / Gemma)
   ↓
Legal Summary + Advice
   ↓
Streamlit UI

📁 Project Structure
KanoonMitra/
├── app.py                 # Streamlit frontend
├── model.py               # Core backend logic
├── data/
│   ├── bns_sections.csv
│   ├── BNStoIPC.csv
│   └── ipc_sections.csv
├── embeddings/
│   ├── bns.pkl
│   └── faiss_index.bin
├── .env                   # Environment variables
├── .gitignore
├── requirements.txt
└── README.md

🛠️ Technology Stack

Frontend
Streamlit – Interactive web interface

Machine Learning & NLP
sentence-transformers – Semantic text embeddings
Model: all-MiniLM-L6-v2

Vector Search
FAISS – Fast similarity search on embeddings

Data Processing
pandas – CSV and Pickle data handling
numpy – Numerical operations

Web Scraping
requests – HTTP requests
beautifulsoup4 – Case law extraction

Large Language Models
google.genai
Gemini (when quota/billing is enabled)
Gemma (open-source fallback)

Environment Management
python-dotenv – Secure API key loading

🧠 Backend Logic (model.py)
The model.py file is the core intelligence layer of the application.
It performs semantic search, legal mapping, case tracking, and AI-based text generation.


🔍Case Reference Fetching
The get_case_reference_links function retrieves relevant legal case references from Indian Kanoon.
It sends a search request based on the legal section or query, parses the results using BeautifulSoup, and returns the top matching case titles with their links.
This adds real-world judicial context and helps users understand how laws are applied in actual cases


1️⃣ Environment & LLM Configuration
Enable secure communication with Large Language Models for text generation.
2️⃣ Dataset Loading
Three main datasets are used:
a) bns.pkl
Contains Bharatiya Nyaya Sanhita sections
Includes section number, title, and description
Acts as the primary legal knowledge base
b) faiss_index.bin
FAISS vector index built from BNS embeddings
Enables fast semantic similarity search
c) BNStoIPC.csv
Maps BNS sections to equivalent IPC sections
Includes IPC descriptions for reference
3️⃣ Semantic Search using ML
Because legal problems are expressed in natural language, not exact legal terms.
4️⃣ Legal Mapping & Case Tracking
IPC Mapping
Maps retrieved BNS sections to IPC equivalents
Helps users familiar with older IPC references
Case Reference Fetching
Scrapes Indian Kanoon for related judgments
Provides real-world legal context
5️⃣ Summary & Legal Advice Generation (LLM)
Two separate prompts are used:
Legal Summary
Explains the legal issue in plain English
Summarizes relevant BNS sections
Legal Advice
Provides actionable steps (e.g., FIR, police, magistrate)
Keeps advice clear and non-technical
Separation ensures clarity and better user understanding.
6️⃣ Final Orchestration Function
generate_final_response(user_query) integrates the entire pipeline:
Accepts user input
Generates embeddings
Performs FAISS search
Retrieves BNS sections
Maps IPC sections
Fetches case references
Generates summary and advice
Returns structured response to the UI

{
  "summary": "...",
  "advice": "...",
  "ipc_mapping": "...",
  "bns_descriptions": "...",
  "case_links": "..."
}

▶️ Running the Application Locally
pip install -r requirements.txt
streamlit run app.py

---

### Project By
**Vaishnavi Khatri**  
B.Tech / M.Tech (IT)  
Indian Institute of Professional Studies (IIPS), DAVV


