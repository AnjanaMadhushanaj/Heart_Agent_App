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
        "using the 'Medical Guidelines Retriever' tool. Synthesize these inputs into a drafted medical report. "
        "The report must be exactly two paragraphs, written in simple, empathetic English, translating the raw risk "
        "into patient-friendly explanations, reassurance, and actionable lifestyle recommendations."
    ),
    expected_output="A 2-paragraph draft medical report that combines the diagnostic result with clinical guidelines in an empathetic tone.",
    agent=reporting_agent
)

# 3. Critique Task (Self-Critique/Reflection Pattern)
critique_task = Task(
    description=(
        "Review the drafted medical report. Ensure that it is highly compassionate, medically safe, easy to "
        "understand for a layperson, and contains actionable next steps. Check that it translates all statistics "
        "into plain English and adheres to a supportive clinical communication style. Revise the text if necessary. "
        "The final output must be exactly two paragraphs."
    ),
    expected_output="The finalized 2-paragraph empathetic clinical report.",
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
