# 🚀 Quick Start Guide

Get the Smart Data Analyst Agent running in **5 minutes**!

---

## ⚡ 5-Minute Setup

### Step 1️⃣: Download and Navigate
```bash
# Extract the project folder
cd path/to/ai-data-analyst-agent
```

### Step 2️⃣: Install Python Packages
```bash
# Windows
pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt
```

### Step 3️⃣: Get API Key (2 minutes)
1. Visit: https://makersuite.google.com/
2. Click "Get API Key"
3. Copy the key
4. Keep it safe for step 5

### Step 4️⃣: Run the App
```bash
streamlit run app.py
```

**Browser opens automatically** → `http://localhost:8501`

### Step 5️⃣: Add API Key in App
1. Look at the **Sidebar** (left side)
2. Paste your API key in the "Google Gemini API Key" field
3. You're ready to go! ✅

---

## 📚 What to Do Next

### First Run - Try This:
1. **Home** 🏠 - Read overview
2. **Upload Data** 📤 - Use any CSV/Excel file
3. **Data Overview** 🔍 - See your data
4. **Visualizations** 📈 - Create charts
5. **AI Chatbot** 🤖 - Ask questions (after API key!)
6. **Insights** 💡 - Get recommendations

### Sample Data:
No test data? Try these:
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Google Dataset Search](https://datasetsearch.research.google.com/)
- [UCI ML Repository](https://archive.ics.uci.edu/ml/)

---

## 🆘 Troubleshooting

### ❌ "command not found: pip"
```bash
# Try python's built-in pip
python -m pip install -r requirements.txt
```

### ❌ "ModuleNotFoundError"
```bash
# Reinstall all packages
pip install -r requirements.txt --upgrade
```

### ❌ "API key invalid"
- Double-check key (no spaces/typos)
- Visit https://makersuite.google.com/ to verify
- Try creating a new key

### ❌ App won't start
```bash
# Kill previous process
# Windows: Ctrl+C in terminal

# Then try again
streamlit run app.py
```

### ❌ Port 8501 already in use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

---

## 💡 Key Features to Explore

| Feature | Path | What It Does |
|---------|------|-------------|
| 📤 Upload | Upload Data | Import CSV/Excel files |
| 🔍 Preview | Data Overview | View data & statistics |
| 🧹 Clean | Data Cleaning | Remove duplicates, handle missing |
| 📊 Charts | Visualizations | 9+ interactive chart types |
| 🤖 Chat | AI Chatbot | Ask questions about data |
| 💡 Insights | Insights Tab | Auto-generated recommendations |

---

## 📝 Sample Questions for AI

After uploading data and adding API key, ask the chatbot:

- "What are the key statistics?"
- "Identify important features"
- "What patterns exist?"
- "Are there outliers?"
- "Suggest improvements"
- "What correlations exist?"

---

## 💾 Export Your Work

### Download Options:
- **CSV** - Cleaned data as CSV
- **Excel** - Multi-sheet workbook
- **Report** - Analysis report (text)

Location: **Data Cleaning** tab or **Insights** tab

---

## 🎓 Learning Path

### Beginner (30 mins)
1. Upload a simple CSV
2. Explore Data Overview
3. View some visualizations
4. Ask chatbot questions

### Intermediate (1 hour)
1. Load complex dataset
2. Do data cleaning
3. Create multiple charts
4. Generate insights

### Advanced (2+ hours)
1. Upload multiple files
2. Advanced cleaning strategies
3. Export full reports
4. Combine data analysis workflow

---

## 🔐 Security Notes

✅ **What's Safe:**
- Your data stays on your computer
- No data is stored in cloud
- API key only for AI features
- Session-only storage

❌ **What to Avoid:**
- Don't share API keys
- Don't commit `.env` to GitHub
- Don't upload sensitive data on public deployments

---

## 📞 Need Help?

1. **Check README.md** - Comprehensive documentation
2. **Read DEPLOYMENT.md** - For advanced setup
3. **Try Settings** ⚙️ - Reset or clear data
4. **Restart App** - Kill and rerun

---

## 🚀 Next Steps

After mastering basics:

1. **Deploy Online**
   - Streamlit Cloud (free!)
   - Heroku, AWS, Docker, etc.
   - See DEPLOYMENT.md

2. **Customize**
   - Modify themes in app.py
   - Add custom features
   - Share with team

3. **Scale Up**
   - Handle larger datasets
   - Integrate with databases
   - Build pipelines

---

## 🎉 You're All Set!

The app is ready. Start with:
```bash
streamlit run app.py
```

Then upload your first dataset and explore! 🎯

---

**Enjoy your data analysis journey!** 📊✨
