# 🤖 Hanshika's AI Task Planner

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama_3-blue?style=for-the-badge)

A smart, AI-powered daily task prioritization agent built specifically for ML/Data Engineering workflows. Instead of manually sorting your to-do list, simply "brain-dump" your thoughts into the app, and the agent will automatically organize, categorize, and prioritize them based on strict engineering rules.

🌐 **[Live Demo: Try the App Here!](https://ai-agent-for-daily-task-planner-6z9pivd6wynxgnj6tn4upv.streamlit.app/)**

---

## ✨ Features

- **Custom Prioritization Engine:** Uses the ultra-fast Groq Llama 3 API to analyze tasks and assign priorities (P0 to P3) based on real-world engineering severity (e.g., pipeline failures are P0, reading research papers is P3).
- **Intelligent Categorization:** Automatically tags tasks into relevant categories (`MLOps`, `ETL/Data`, `GenAI`, `DevOps`, etc.).
- **Time Estimation:** Generates realistic minute-by-minute time estimations for your day and provides a total summary of hours required.
- **CSV Export:** One-click download of your optimized schedule to a `.csv` file for use in Excel, Google Sheets, or Jira.
- **Lightning Fast:** Powered by Groq's LPU inference engine, returning complex schedule generation in milliseconds.

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **LLM / Inference:** [Groq API](https://groq.com/) (Model: `llama-3.1-8b-instant`)
- **Data Handling:** Pandas
- **Language:** Python 3.x

---

## 🚀 How to Run Locally

If you want to run this application on your local machine, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/thukralhanshika64-design/AI-Agent-for-Daily-Task-Planner.git
cd AI-Agent-for-Daily-Task-Planner
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your Groq API Key
You will need a free API key from [Groq Cloud](https://console.groq.com/keys). 

Create a `.streamlit/secrets.toml` file in the root directory (or simply export it as an environment variable):
```toml
# .streamlit/secrets.toml
GROQ_API_KEY = "your_groq_api_key_here"
```

### 4. Run the app
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 🧠 AI Prioritization Rules

The agent uses a strict system prompt tailored to Data/ML workflows:
- **P0 (Critical):** Production pipeline failures, Model drift requiring immediate action, hard deadlines.
- **P1 (High):** Blocking PR reviews, broken ETL pipelines affecting downstream reports.
- **P2 (Medium):** Stakeholder communications, routine dashboard updates, MLflow logging.
- **P3 (Low):** Reading research papers, exploring new frameworks, portfolio projects.

## 🤝 Contributing
Feel free to fork this project, tweak the `SYSTEM_PROMPT` in `app.py` to fit your own professional workflow, and submit a pull request!
