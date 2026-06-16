# Second Brain — Quick Start Guide

Welcome to your Second Brain! This guide will get you up and running in 5 minutes.

---

## 🚀 Installation

### Step 1: Set Up Python Environment

```powershell
# Navigate to the project directory
cd "c:\Users\LENOVO\Documents\GitHub\Cohort-2-AI-POCs\Ai Co-pilot"

# Create a virtual environment (recommended)
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip
```

### Step 2: Install Dependencies

```powershell
# Install all required packages
pip install -r requirements.txt
```

**Note**: First installation may take 2-3 minutes. The system will also download embedding models (~80MB) on first use.

### Step 3: Configure API Key

1. **Copy the example environment file**:
   ```powershell
   Copy-Item .env.example .env
   ```

2. **Get a free Gemini API key**:
   - Visit: [https://ai.google.dev](https://ai.google.dev)
   - Sign in with your Google account
   - Click "Get API Key"
   - Copy the key

3. **Edit `.env` file**:
   ```bash
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

---

## ▶️ Running the Application

```powershell
# Make sure you're in the project directory with venv activated
streamlit run streamlit_app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 📚 First Steps in the UI

### 1. Build the Initial Index

On first run, click **"🔁 Rebuild from data/ folder"** in the sidebar. This will:
- Process the sample documents (3 markdown files with AI research notes)
- Chunk them intelligently
- Generate embeddings
- Store in ChromaDB vector database

**Time**: ~10-20 seconds for the sample documents

### 2. Try Example Queries

Click on the example chips or type your own:

**Simple Q&A**:
- *"What did I read about LLM scaling?"*
- *"What are the key techniques in prompt engineering?"*
- *"Explain RAG systems to me"*

**Temporal Queries**:
- *"What did I read about AI last month?"*
- *"Show me my research from January 2026"*

**Topic Summaries**:
- *"Summarize everything I know about RAG"*
- *"What have I learned about LLM scaling?"*
- *"Give me an overview of prompt engineering techniques"*

### 3. Upload Your Own Documents

In the sidebar under **"📤 Upload Documents"**:
1. Drag and drop files (PDF, DOCX, TXT, MD, HTML)
2. Choose a category (Personal, Research, Work, etc.)
3. Click **"🚀 Process Uploads"**
4. Wait for processing (~5-10 seconds per document)
5. Ask questions about your uploaded content!

---

## 🧠 Understanding the Interface

### Main Chat Area
- Type questions in the chat input at the bottom
- View conversation history
- See AI responses with citations

### Agent Trace (Expandable)
Click **"🔎 Agent trace"** under each response to see:
- **Planner**: What intent was detected
- **Retriever**: How many chunks retrieved, filters applied
- **Context Optimizer**: Token savings achieved
- **Reasoning**: How the answer was generated

### Sources
Click **"📚 Sources"** to see which documents were cited.

### Retrieved Context
Click **"📄 Retrieved context"** to see the actual chunks used, with similarity scores.

### Sidebar Sections

**📤 Upload Documents**: Add new files to your knowledge base

**📚 Knowledge Base**: Shows total indexed chunks, option to rebuild

**⚙️ Agent Settings**:
- **Semantic Memory**: Enable/disable conversation recall
- **Context Optimizer**: Enable/disable token optimization
- **Tool Calling**: (Disabled by default)
- **Retriever top-K**: How many chunks to retrieve (3-20)

**🧠 Semantic Memory**: Shows stored interactions count

**💰 Cost Monitor**: Per-session and daily cost tracking

---

## 💡 Tips for Best Results

### Writing Good Queries

**❌ Too vague**: *"Tell me about AI"*  
**✅ Specific**: *"What are the key findings about LLM scaling laws?"*

**❌ No context**: *"What's the latest?"*  
**✅ With context**: *"What did I save about RAG systems last month?"*

### Uploading Documents

**Best formats**:
- **PDFs**: Research papers, articles, ebooks
- **DOCX**: Reports, notes, documentation
- **Markdown**: Technical docs, personal notes
- **TXT**: Plain text notes
- **HTML**: Saved web pages, bookmarks

**Tips**:
- Use descriptive filenames
- Categorize appropriately (Research/Personal/Work)
- One topic per document works best
- Avoid scanned PDFs (need OCR first)

### Organizing Your Knowledge

**Categories to use**:
- **Research**: Academic papers, technical articles
- **Personal**: Personal notes, thoughts, journals
- **Work**: Work docs, meeting notes, reports
- **Email**: Important email threads (copy-paste to TXT)
- **Notes**: Quick notes, reminders, ideas

---

## 🎯 Common Use Cases

### For Researchers
- *"Summarize all papers I've read about transformers"*
- *"What did I learn about fine-tuning last month?"*
- *"Find my notes on evaluation metrics"*

### For Students
- *"What are the main concepts in my database notes?"*
- *"Summarize everything I know about quantum computing"*
- *"What did I study last week for the algorithms exam?"*

### For Professionals
- *"Find information about the Q4 strategy meeting"*
- *"What were the action items from last month's standup?"*
- *"Summarize our API documentation"*

### For Personal Knowledge Management
- *"What books did I save notes from this year?"*
- *"Remind me what I learned about productivity"*
- *"What are my favorite recipes from the cooking PDF?"*

---

## 🔧 Troubleshooting

### Problem: "No GOOGLE_API_KEY" error
**Solution**: 
1. Make sure `.env` file exists in the project root
2. Verify the API key is correctly pasted (no extra spaces)
3. Restart the Streamlit app

### Problem: Slow first query
**Solution**: This is normal! First run downloads embedding models (~80MB). Subsequent queries are fast.

### Problem: PDF extraction fails
**Solution**: 
- Ensure PyPDF2 is installed: `pip install PyPDF2`
- Try converting the PDF to text first
- Scanned PDFs need OCR (use an online converter)

### Problem: "Knowledge base is empty"
**Solution**: Click "🔁 Rebuild from data/ folder" or upload documents

### Problem: Answers seem irrelevant
**Solution**:
- Try more specific queries
- Check if relevant documents are uploaded
- Increase "Retriever top-K" in settings
- Enable "Context Optimizer" for better ranking

---

## 🎬 Ready for Demo?

See **DEMO_GUIDE.md** for a complete 5-minute presentation script, including:
- Pre-demo setup checklist
- Step-by-step demo flow
- Talking points
- Q&A prep
- Troubleshooting during live demos

---

## 📖 Learn More

- **README.md**: Full technical documentation
- **DEMO_GUIDE.md**: Presentation guide for judges/stakeholders
- **Code documentation**: All modules have detailed docstrings

---

## 🆘 Need Help?

### Check the logs
Streamlit shows errors in the terminal where you ran `streamlit run`.

### Verify installation
```powershell
python -c "import streamlit, chromadb, sentence_transformers; print('All imports OK!')"
```

### Test API key
```powershell
python -c "from app.llm import generate; print(generate('Say hello', temperature=0).text)"
```

### Reset everything
If something goes wrong:
```powershell
# Delete the database
Remove-Item -Recurse -Force chroma_db

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Restart the app
streamlit run streamlit_app.py
```

---

## 🚀 Next Steps

Once you're comfortable:

1. **Upload your own documents** (PDFs, notes, bookmarks)
2. **Experiment with different query types** (Q&A, temporal, summaries)
3. **Try the semantic memory** (ask similar questions, see recall)
4. **Monitor costs** (check the Cost Monitor section)
5. **Give feedback** (use 👍/👎 buttons to improve memory)

---

## 🎉 You're All Set!

Your Second Brain is ready. Start uploading your knowledge and asking questions!

**Remember**: The more you use it, the smarter it gets (semantic memory), and the more transparent it is (every answer shows its reasoning).

Welcome to the future of personal knowledge management! 🧠✨
