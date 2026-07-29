from crewai import Task, Crew, Process

# Import agents
from agents import diagnostic_agent, reporting_agent, critique_agent

# 1. Diagnostic Task
diagnostic_task = Task(
    description=(
        "Analyze the patient's cholesterol level ({chol} mg/dL) and maximum heart rate achieved ({thalach} bpm) "
        "using the 'Heart Disease Predictor' tool. Provide an objective risk assessment stating whether the patient "
        "is classified as High Risk or Low Risk based on the machine learning model's output."
    ),
    expected_output="A clear, objective risk assessment indicating the risk level (High Risk or Low Risk).",
    agent=diagnostic_agent
)

# 2. Reporting Task
reporting_task = Task(
    description=(
        "Using the patient's clinical inputs (Cholesterol: {chol} mg/dL, Max Heart Rate: {thalach} bpm) and "
        "the diagnostic risk assessment from the Diagnostic Agent, retrieve relevant clinical guidelines "
        "using the 'Medical Guidelines Retriever' tool. Synthesize these inputs into a structured, highly professional, "
        "and patient-friendly medical report.\n\n"
        "Format the report clearly using markdown with the following structure:\n"
        "### 🏥 Executive Summary\n"
        "A warm, empathetic opening stating the overall risk assessment and reassurance.\n\n"
        "### 📊 Vitals & Diagnostic Analysis\n"
        "Explain what {chol} mg/dL cholesterol and {thalach} bpm max heart rate mean in plain English without confusing jargon.\n\n"
        "### 💡 Evidence-Based Lifestyle & Health Guidance\n"
        "Provide 3-4 bulleted, actionable lifestyle, dietary, and exercise recommendations derived directly from the retrieved guidelines.\n\n"
        "### 🩺 Recommended Next Steps\n"
        "Clear, supportive advice on routine monitoring and consulting their physician."
    ),
    expected_output="A beautifully structured markdown clinical report with clear headings, bullet points, and plain English explanations.",
    agent=reporting_agent
)

# 3. Critique Task (Self-Critique/Reflection Pattern)
critique_task = Task(
    description=(
        "Review the drafted medical report. Ensure that:\n"
        "1. It follows the 4 structured markdown sections (Executive Summary, Vitals & Diagnostic Analysis, Evidence-Based Guidance, Recommended Next Steps).\n"
        "2. All medical jargon is translated into simple, compassionate English that any layperson can easily understand.\n"
        "3. The tone is highly professional, non-alarmist, and supportive.\n"
        "4. The recommendations strictly match the retrieved guidelines.\n\n"
        "Refine and format the final text cleanly."
    ),
    expected_output="The finalized, beautifully formatted markdown clinical report.",
    agent=critique_agent
)

# Assemble the Crew
clinical_crew = Crew(
    agents=[diagnostic_agent, reporting_agent, critique_agent],
    tasks=[diagnostic_task, reporting_task, critique_task],
    process=Process.sequential,
    verbose=True
)

def run_clinical_analysis(chol: float, thalach: float) -> str:
    """Kicks off the clinical decision support crew with patient inputs."""
    inputs = {
        "chol": chol,
        "thalach": thalach
    }
    result = clinical_crew.kickoff(inputs=inputs)
    return str(result)
