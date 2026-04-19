import ollama
import json

# ─────────────────────────────────────────────
# 1. Agent Persona & Rules (tailored to Hanshika)
# ─────────────────────────────────────────────

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

# ─────────────────────────────────────────────
# 2. Example Unstructured Input (your brain-dump)
# ─────────────────────────────────────────────

messy_brain_dump = """
SageMaker batch transform job is failing on the churn model pipeline — need to check logs.
Sarah raised a PR for the new dbt model, she's waiting on my review to merge.
Got a Slack message from the marketing team asking about the Tableau churn dashboard numbers.
Model drift alert came in for the sentiment classifier — AUC dropped below threshold.
Want to read the new LLaMA 3 fine-tuning paper that dropped yesterday.
Should update the MLflow experiment tags for last week's XGBoost run.
Prep notes for 3 PM standup with the product manager about the GenAI reporting pipeline.
Deploy the updated FastAPI endpoint for the NLP sentiment API to staging.
"""

# ─────────────────────────────────────────────
# 3. Call Ollama (local LLM)
# ─────────────────────────────────────────────

def generate_schedule(user_input: str) -> None:
    print("\n Agent is thinking... (running locally via Ollama)\n")

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_input}
        ],
        options={"temperature": 0.1}   # low temp = strict JSON, no creativity
    )

    raw_output = response["message"]["content"].strip()

    # ─────────────────────────────────────────
    # 4. Parse JSON & Display Structured Schedule
    # ─────────────────────────────────────────

    try:
        # Strip accidental markdown fences if model adds them
        clean = raw_output.replace("```json", "").replace("```", "").strip()
        plan  = json.loads(clean)

        schedule = plan.get("schedule", [])

        # Sort by priority (P0 → P3)
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        schedule.sort(key=lambda x: priority_order.get(x.get("priority", "P3"), 4))

        # ── Summary stats ──
        total_mins = sum(item.get("estimated_minutes", 0) for item in schedule)
        hours, mins = divmod(total_mins, 60)
        counts = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        for item in schedule:
            counts[item.get("priority", "P3")] += 1

        print("=" * 55)
        print("  HANSHIKA'S OPTIMIZED DAILY SCHEDULE")
        print("=" * 55)
        print(f"  Total tasks : {len(schedule)}")
        print(f"  Total time  : {hours}h {mins}m")
        print(f"  P0 Critical : {counts['P0']}  |  P1 High : {counts['P1']}")
        print(f"  P2 Medium   : {counts['P2']}  |  P3 Low  : {counts['P3']}")
        print("=" * 55 + "\n")

        # ── Task list ──
        priority_icons = {"P0": "🔴", "P1": "🟠", "P2": "🔵", "P3": "🟢"}

        for i, item in enumerate(schedule, 1):
            p    = item.get("priority", "?")
            icon = priority_icons.get(p, "⚪")
            task = item.get("task", "Unknown task")
            est  = item.get("estimated_minutes", 0)
            cat  = item.get("category", "")
            why  = item.get("reasoning", "")

            hrs_str = f" ({est // 60}h {est % 60}m)" if est >= 60 else ""

            print(f"{i:>2}. {icon} [{p}] {task}")
            print(f"      Time     : {est} min{hrs_str}")
            print(f"      Category : {cat}")
            print(f"      Why      : {why}\n")

    except json.JSONDecodeError:
        print("Error: Agent did not return valid JSON. Raw output:\n")
        print(raw_output)


# ─────────────────────────────────────────────
# 5. Run  (swap brain-dump for input() to type live)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # To type tasks interactively, replace messy_brain_dump with:
    # user_tasks = input("Brain-dump your tasks:\n> ")
    generate_schedule(messy_brain_dump)
