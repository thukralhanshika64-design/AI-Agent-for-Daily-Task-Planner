import streamlit as st
import json
import os
from groq import Groq

# Securely retrieve the API key from Streamlit Secrets
try:
    api_key = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing. Please set it in Streamlit Secrets.")
    st.stop()

SYSTEM_PROMPT = """
You are an expert AI task planning agent for Hanshika Thukral, a senior AI/ML and Data Engineer.

Hanshika's tech stack:
- ML/AI     : Python, Scikit-learn, XGBoost, TensorFlow, HuggingFace Transformers, MLflow
- GenAI     : GPT-4 API, LangChain, Agentic AI, RAG, Prompt Engineering
- ETL/Data  : dbt, Azure Data Factory, Apache Airflow, REST APIs, FastAPI, GitHub Actions
- Warehouses: Snowflake, Azure Synapse, PostgreSQL
- Cloud     : AWS (SageMaker, S3, IAM, CloudWatch), Azure (ADF, Databricks, Synapse), GCP
- MLOps     : SageMaker Pipelines, MLflow, Docker, Git, GitHub Actions, Model Drift Monitoring
- BI        : Tableau, Power BI

Prioritization rules (specific to her ML/data engineering role):

P0 (Critical):
  - Production pipeline failures (SageMaker, ETL, FastAPI serving endpoints)
  - Model serving downtime or 500 errors
  - Model drift alerts requiring immediate retraining/redeployment
  - Urgent client or stakeholder escalations
  - Hard deadlines due TODAY

P1 (High):
  - PR reviews that are blocking a teammate
  - dbt model changes breaking downstream tables or dashboards
  - ETL pipeline fixes affecting reporting
  - Retraining a model after confirmed drift
  - Unblocking data consumers (BI teams, product, marketing)

P2 (Medium):
  - Stakeholder replies (marketing, product, management)
  - Routine dashboard updates (Tableau, Power BI)
  - MLflow experiment logging and documentation
  - Meeting / 1:1 prep notes
  - Writing weekly automated commentary (GPT-4 pipeline)

P3 (Low):
  - Reading research papers (LLM, GenAI, MLOps)
  - Exploring new tools or frameworks
  - Long-term architecture planning
  - Portfolio / side projects (LangChain apps, RAG systems)
  - Upskilling / certifications

Output Constraints:
You MUST respond ONLY with valid JSON. No conversational text, no markdown code fences, no explanations.

Exact JSON schema:
{
  "schedule": [
    {
      "task": "Short task name",
      "priority": "P0",
      "estimated_minutes": 45,
      "reasoning": "One-sentence explanation of this priority",
      "category": "One of: MLOps | ETL/Data | GenAI | Stakeholder | DevOps | Learning"
    }
  ]
}
"""

def generate_schedule(user_input: str, api_key: str):
    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Using Groq's lightning-fast Llama 3 8B model
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_input}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()

# Streamlit App UI
st.set_page_config(page_title="Hanshika's Task Agent", page_icon="🤖", layout="centered")

st.title("🤖 Hanshika's Daily Task Planner")
st.markdown("Brain-dump your tasks below, and I'll prioritize them based on your engineering rules.")

# Default input
default_dump = """SageMaker batch transform job is failing on the churn model pipeline — need to check logs.
Sarah raised a PR for the new dbt model, she's waiting on my review to merge.
Got a Slack message from the marketing team asking about the Tableau churn dashboard numbers.
Model drift alert came in for the sentiment classifier — AUC dropped below threshold.
Want to read the new LLaMA 3 fine-tuning paper that dropped yesterday.
Should update the MLflow experiment tags for last week's XGBoost run.
Prep notes for 3 PM standup with the product manager about the GenAI reporting pipeline.
Deploy the updated FastAPI endpoint for the NLP sentiment API to staging."""

user_input = st.text_area("What's on your mind today?", height=200, value=default_dump)

if st.button("Generate Schedule", type="primary"):
    with st.spinner("Agent is thinking..."):
        try:
            raw_output = generate_schedule(user_input, api_key)
            
            # Parse JSON
            clean = raw_output.replace("```json", "").replace("```", "").strip()
            plan = json.loads(clean)
            schedule = plan.get("schedule", [])
            
            # Sort by priority
            priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
            schedule.sort(key=lambda x: priority_order.get(x.get("priority", "P3"), 4))
            
            # Summary stats
            total_mins = sum(item.get("estimated_minutes", 0) for item in schedule)
            hours, mins = divmod(total_mins, 60)
            
            st.divider()
            st.subheader("📊 Summary")
            col1, col2 = st.columns(2)
            col1.metric("Total Tasks", len(schedule))
            col2.metric("Total Time", f"{hours}h {mins}m")
            
            st.subheader("📋 Optimized Schedule")
            
            priority_colors = {"P0": "red", "P1": "orange", "P2": "blue", "P3": "green"}
            
            for item in schedule:
                p = item.get("priority", "?")
                task = item.get("task", "Unknown task")
                est = item.get("estimated_minutes", 0)
                cat = item.get("category", "")
                why = item.get("reasoning", "")
                
                color = priority_colors.get(p, "gray")
                hrs_str = f" ({est // 60}h {est % 60}m)" if est >= 60 else ""
                
                with st.expander(f"**[{p}]** {task} - {est} min"):
                    st.markdown(f"**Category:** :{color}[{cat}]")
                    st.markdown(f"**Why:** {why}")
                    
        except json.JSONDecodeError:
            st.error("Error: Agent did not return valid JSON. Raw output:")
            st.code(raw_output)
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
