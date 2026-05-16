# 📊 Smart Data Analyst Agent

A comprehensive **AI-powered data analysis tool** built with Python, Streamlit, and Google Gemini API. This application enables users to upload datasets, clean data, generate visualizations, and get AI-powered insights through an interactive chat interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Features

### 📤 Data Management
- ✅ Upload CSV and Excel files
- ✅ Multi-file upload support
- ✅ Automatic data preview and profiling
- ✅ Dataset shape and structure analysis

### 🧹 Data Cleaning
- ✅ Detect missing values
- ✅ Remove duplicate rows
- ✅ Handle missing values (multiple strategies)
- ✅ Normalize numeric columns
- ✅ Show data quality metrics

### 📊 Statistical Analysis
- ✅ Comprehensive dataset statistics
- ✅ Correlation matrix analysis
- ✅ Data distribution insights
- ✅ Outlier detection (IQR method)
- ✅ Categorical feature analysis

### 📈 Visualizations (Interactive with Plotly)
- ✅ Correlation heatmap
- ✅ Histograms
- ✅ Bar charts
- ✅ Scatter plots
- ✅ Box plots
- ✅ Pie charts
- ✅ Line charts
- ✅ Area charts
- ✅ Pair plot matrices

### 🤖 AI-Powered Chatbot
- ✅ Ask questions about your dataset
- ✅ Natural language processing
- ✅ Dataset context-aware responses
- ✅ Sample prompts for guidance
- ✅ Conversation history

### 💡 AI Insights & Recommendations
- ✅ Data quality scoring
- ✅ Automated data issue detection
- ✅ Business insight generation
- ✅ Pattern and trend analysis
- ✅ Actionable recommendations

### 💾 Export Options
- ✅ Download cleaned CSV files
- ✅ Download Excel with multiple sheets
- ✅ Generate analysis reports
- ✅ Export in multiple formats

### 🎨 User Interface
- ✅ Professional Streamlit dashboard
- ✅ Sidebar navigation
- ✅ Tabbed interfaces
- ✅ Responsive design
- ✅ Custom styling

---

## 📋 Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Google Gemini API Key** (free from https://makersuite.google.com/)

---

## 🔧 Installation

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd ai-data-analyst-agent

# Or extract the ZIP file and navigate to the project directory
cd path/to/project
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **streamlit** - Web application framework
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib** - Static visualizations
- **plotly** - Interactive visualizations
- **google-generativeai** - Gemini API client
- **openpyxl** - Excel file handling
- **python-dotenv** - Environment variables

### Step 4: Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/)
2. Click "Get API Key"
3. Create new API key (free tier available)
4. Copy the API key

---

## 🚀 Running the Application

### Basic Usage

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### With Custom Port

```bash
streamlit run app.py --server.port 8502
```

### Headless Mode (for servers)

```bash
streamlit run app.py --logger.level=error --client.showErrorDetails=false
```

---

## 📖 Usage Guide

### 1. **Home Page** (Initial Landing)
- Overview of features
- Quick start guide
- Feature highlights

### 2. **Upload Data** 📤
- Click "Choose file(s) to upload"
- Select CSV or Excel files
- Multiple file support
- Automatic validation

**Supported Formats:**
- `.csv` - Comma-separated values
- `.xlsx` - Excel 2007+
- `.xls` - Excel 97-2003

### 3. **Data Overview** 🔍
- **Data Preview Tab**: View sample rows
- **Statistics Tab**: Descriptive statistics
- **Data Types Tab**: Column information
- **Missing Values Tab**: Null value analysis

### 4. **Data Cleaning** 🧹
- **Remove Duplicates**: One-click duplicate removal
- **Handle Missing Values**: 5 strategies
  - `drop`: Remove rows with missing values
  - `mean`: Fill numeric columns with mean
  - `median`: Fill numeric columns with median
  - `forward_fill`: Propagate values forward
  - `backward_fill`: Propagate values backward
- **Normalize Columns**: Scale to 0-1 range
- **Export**: Download cleaned data

### 5. **Visualizations** 📈
- **Correlation Heatmap**: Feature relationships
- **Histogram**: Distribution of values
- **Bar Chart**: Categorical frequencies
- **Scatter Plot**: Relationship between variables
- **Box Plot**: Outlier and quartile analysis
- **Pie Chart**: Proportion visualization
- **Line Chart**: Trend analysis
- **Area Chart**: Stacked trends
- **Pair Plot**: Multi-variable relationships

### 6. **AI Chatbot** 🤖
- Ask natural language questions about data
- Sample prompts provided
- Context-aware responses using Gemini API
- Conversation history maintained
- Sample questions include:
  - "What are the key statistics of this dataset?"
  - "Identify the most important features"
  - "What patterns do you see?"
  - "Are there outliers or anomalies?"
  - "What correlations exist?"
  - "Suggest actionable insights"

### 7. **Insights & Recommendations** 💡
- **Overview Tab**:
  - Dataset statistics
  - Data quality score
  - Automated recommendations

- **Correlations Tab**:
  - Strong feature relationships
  - Correlation strength threshold

- **Distribution Tab**:
  - Skewness analysis
  - Kurtosis metrics
  - Distribution types

- **Outliers Tab**:
  - IQR-based detection
  - Outlier percentages
  - Bounds calculation

- **Report Tab**:
  - Comprehensive analysis report
  - Download as text file
  - Formatted for sharing

- **AI Insights** (with API key):
  - Generated summary
  - Data issue detection
  - Business insights

### 8. **Settings** ⚙️
- Theme configuration
- Data management
- Clear/reset options
- API configuration status

---

## 🔑 API Configuration

### Adding Gemini API Key

1. **In the Application**:
   - Navigate to sidebar
   - Enter "Google Gemini API Key" field
   - Key is stored in session only (not saved to disk)

2. **Environment Variable (Optional)**:
   ```bash
   # Create .env file in project root
   GEMINI_API_KEY=your_key_here
   ```

3. **Verify Configuration**:
   - Look for ✅ success message in sidebar
   - Navigate to Settings to confirm status

---

## 📁 Project Structure

```
ai-data-analyst-agent/
│
├── app.py                 # Main Streamlit application
├── data_cleaning.py       # Data preprocessing functions
├── visualization.py       # Chart and graph generation
├── chatbot.py            # AI chatbot implementation
├── insights.py           # Insight generation module
│
├── requirements.txt      # Python dependencies
├── README.md            # This file
│
└── sample_data/         # (Optional) Sample datasets
    ├── sales_data.csv
    ├── customer_data.xlsx
    └── ...
```

### File Descriptions

#### `app.py` (Main Application)
- Streamlit page configuration
- Navigation and UI layout
- Session state management
- Page implementations
- User input handling

#### `data_cleaning.py` (Data Processing)
- Missing value detection
- Duplicate removal
- Data imputation strategies
- Statistical calculations
- Column normalization
- Outlier detection

#### `visualization.py` (Charting)
- Plotly interactive charts
- Matplotlib fallback
- Custom styling
- Multiple chart types
- Export-ready visualizations

#### `chatbot.py` (AI Module)
- Gemini API integration
- Dataset context preparation
- Query processing
- Response generation
- Error handling

#### `insights.py` (Analytics)
- Quality scoring
- Correlation analysis
- Distribution analysis
- Outlier detection
- Recommendation generation

---

## 💡 Sample Prompts for AI Chatbot

### Data Exploration
- "What are the key statistics of this dataset?"
- "How many rows and columns does this dataset have?"
- "What are the data types of each column?"

### Pattern Analysis
- "What patterns do you see in the data?"
- "Which features have the strongest relationships?"
- "What correlations exist between variables?"

### Data Quality
- "Are there any outliers or anomalies?"
- "What data quality issues should I address?"
- "How complete is this dataset?"

### Insights
- "Provide insights about the distribution of values"
- "Identify the most important features in this dataset"
- "Suggest actionable insights from this dataset"

### Recommendations
- "What are your recommendations for data cleaning?"
- "Which variables should I focus on?"
- "What should be my next analysis step?"

---

## 🎯 Use Cases

### 👨‍💼 Business Analysis
- Sales data analysis
- Customer behavior analysis
- Marketing campaign performance
- Revenue forecasting

### 🎓 Academic Research
- Experimental data analysis
- Statistical validation
- Research insights
- Publication-ready statistics

### 📊 Data Science Projects
- EDA (Exploratory Data Analysis)
- Data preprocessing
- Feature analysis
- Model preparation

### 💼 Internship Projects
- Professional portfolio showcase
- Complete data pipeline
- Business value demonstration
- Decision-making support

### 🔬 Scientific Analysis
- Experimental results
- Trend identification
- Anomaly detection
- Hypothesis testing

---

## ⚙️ Advanced Configuration

### Custom Styling

Edit the CSS section in `app.py` to customize colors:

```python
# In app.py, modify the st.markdown() CSS section
--primary-color: #your-color;
--secondary-color: #your-color;
```

### Dataset Size Limits

For large datasets (>100MB):

```bash
# Increase memory limit
streamlit run app.py --client.maxMessageSize=200
```

### Deployment

#### Streamlit Cloud
```bash
# Push to GitHub, then deploy from Streamlit Cloud dashboard
```

#### Heroku
```bash
# Create Procfile and deploy
```

#### Docker
```bash
# Build and run Docker container
docker build -t data-analyst .
docker run -p 8501:8501 data-analyst
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
# Or install individually:
pip install streamlit pandas numpy matplotlib plotly google-generativeai
```

### Issue: API Key not working

**Solution:**
1. Verify key at https://makersuite.google.com/
2. Copy exact key (no spaces)
3. Check if API is enabled
4. Try refreshing the page

### Issue: Large file upload fails

**Solution:**
```bash
# Increase upload limit in .streamlit/config.toml
[client]
maxUploadSize = 500
```

### Issue: Visualization not displaying

**Solution:**
- Check if column is selected
- Verify data type matches chart type
- Try different visualization type
- Clear cache: Ctrl+R

### Issue: Slow performance

**Solution:**
- Reduce dataset size (sample first)
- Use fewer rows for pair plot
- Limit correlation threshold
- Clear chat history

---

## 📚 Dependencies Details

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web framework |
| pandas | 2.0.3 | Data manipulation |
| numpy | 1.24.3 | Numerical computing |
| matplotlib | 3.7.2 | Plotting library |
| plotly | 5.16.1 | Interactive charts |
| google-generativeai | 0.3.0 | Gemini API |
| openpyxl | 3.1.2 | Excel support |
| python-dotenv | 1.0.0 | Environment variables |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Google Gemini API** for AI capabilities
- **Streamlit** for the amazing web framework
- **Plotly** for interactive visualizations
- **Pandas** for data manipulation

---

## 📞 Support

### Getting Help

1. **Check Documentation**: Review this README
2. **Search Issues**: Look for similar problems
3. **Create Issue**: Detail your problem with screenshots
4. **Contact**: Reach out to the development team

### Common Questions

**Q: Is my data safe?**
A: Data is processed locally. API calls only happen for AI features, and no data is stored.

**Q: Can I use this offline?**
A: Yes, except for AI features which require API key and internet.

**Q: What file sizes are supported?**
A: Up to 500MB (configurable). Larger datasets may be slow.

**Q: Can I deploy this to production?**
A: Yes, follow deployment guides in Advanced Configuration section.

---

## 📊 Example Workflows

### Workflow 1: Quick Data Exploration
1. Upload CSV → Data Overview → Visualizations → Export Report

### Workflow 2: Data Cleaning Project
1. Upload → Detect Issues → Clean Data → Validation → Export

### Workflow 3: Business Intelligence
1. Upload → Analysis → Visualizations → AI Insights → Report

### Workflow 4: Academic Research
1. Upload Data → Statistics → Outlier Detection → Insights → Publication Report

---

## 🔒 Privacy & Security

- No data is stored on servers
- All processing is local
- API keys are session-only
- HTTPS recommended for deployment
- No telemetry or tracking

---

## 🚀 Future Enhancements

- [ ] Database integration
- [ ] Real-time data streaming
- [ ] Advanced ML models
- [ ] Custom report templates
- [ ] Team collaboration features
- [ ] Version control for datasets
- [ ] API endpoint for programmatic access
- [ ] Mobile app support

---

## 📌 Version History

### v1.0 (Current)
- Initial release
- Core features implemented
- Full AI integration
- Comprehensive documentation

---

## ⭐ Star & Fork

If you find this project useful, please:
- ⭐ Star the repository
- 🍴 Fork for your own use
- 🔗 Share with others
- 💬 Provide feedback

---

**Made with ❤️ for data enthusiasts, students, and professionals**

Happy Analyzing! 🎉
