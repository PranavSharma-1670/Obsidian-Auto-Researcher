# 🕵️ Obsidian Auto-Researcher (Version 1.0)

## 📖 Summary
Obsidian Auto-Researcher is a fully local, privacy-first Retrieval-Augmented Generation (RAG) desktop application. It ingests local `.md` and `.txt` files into a vector database and allows users to query their personal knowledge base using locally hosted Large Language Models (LLMs). 

Designed for rigorous research and Personal Knowledge Management (PKM), the tool features a unique **Multi-Model Comparison Grid** to evaluate different LLM outputs side-by-side, and a **Human-in-the-Loop (HITL) Editor** to review, tweak, and format the AI's response before pushing it directly to a local Obsidian vault.

---

## ✨ Features
* **100% Local Execution:** Powered by Ollama and ChromaDB, ensuring no personal research data ever leaves your machine.
* **Local RAG Pipeline:** Context-aware generation grounded strictly in your provided raw source documents.
* **Multi-Model Comparison Grid:** Run queries sequentially against multiple local models (e.g., Gemma, Qwen, Llama) and evaluate their drafts side-by-side.
* **Advanced Hyper-parameter Controls:** Dynamically adjust model temperature and system instructions on the fly without changing code.
* **Human-in-the-Loop (HITL) Workspace:** An integrated text editor to refine the winning AI draft before saving.
* **Native Obsidian Integration:** Exports formatted `.md` files directly to your vault, automatically injecting YAML frontmatter (tags, dates), with the ability to append new research to existing notes.

---

## 🛠️ Architecture Stack
* **Frontend UI:** Streamlit
* **Vector Database:** ChromaDB (Persistent Local)
* **LLM Orchestration:** Ollama (Python Client)
* **Language:** Python 3.10+

---

## 🚀 Installation & Setup

### 1. Prerequisites
* [Ollama](https://ollama.com/) installed on your machine.
* Python 3.10 or higher.
* An active Obsidian Vault.

### 2. Download Local Models
Open your terminal and pull the models you wish to use via Ollama. For example:
```bash
ollama pull gemma4:e4b
ollama pull qwen3:4b
ollama pull tinyllama
```

### 3. Clone & Environment Setup
Clone this repository and set up your Python virtual environment:

```Bash
git clone [https://github.com/yourusername/obsidian-auto-researcher.git](https://github.com/yourusername/obsidian-auto-researcher.git)
cd obsidian-auto-researcher

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Your Vault Path
Open exporter.py and update the OBSIDIAN_VAULT_PATH variable to match the absolute path of your local Obsidian vault:

```Python
OBSIDIAN_VAULT_PATH = "/Users/yourname/Path/To/Your/Vault"
```
## 💻 How to Use
### 1. Start the Application:
Run the Streamlit server from your terminal:

```Bash
streamlit run app.py
```
### 2. Select Models:
Use the sidebar to select one or more downloaded local models to run your query against.
### 3. Generate Drafts: 
Enter your research topic. The app will sequentially query the models and display their outputs in a side-by-side comparison grid.
### 4. Compare & Refine: 
Review the drafts, copy/paste the best parts using the reference tabs, and click "Send to Editor" on your preferred output.
### 5. Save to Obsidian: 
Use the HITL editor to finalize the text, add custom tags, and choose whether to create a brand-new note or append the research to an existing document in your vault.
