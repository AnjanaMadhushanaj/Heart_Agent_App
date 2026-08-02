from crewai import Task, Crew, Process
from agents import (
    extraction_agent,
    analyzer_agent,
    translator_agent,
    guardrail_agent
)

# 1. Extraction Task
extraction_task = Task(
    description=(
        "Parse the provided lab report content:\n"
        "'''\n{lab_text}\n'''\n"
        "Extract all measured lab parameters, numerical values, units of measurement, and patient indicators. "
        "Output a clean, structured summary of the raw lab data."
    ),
    expected_output="A structured summary listing extracted lab parameters, measured values, and units.",
    agent=extraction_agent
)

# 2. Medical Analyzer Task (RAG)
analyzer_task = Task(
    description=(
        "Using the extracted lab data from the Extraction Agent, query the 'Medical Guidelines Retriever' tool "
        "in ChromaDB to find standard reference ranges for each measured parameter (e.g. cholesterol, glucose, CBC, liver/kidney markers). "
        "Identify parameters that are normal, borderline, or out-of-bounds (elevated or low)."
    ),
    expected_output="An analysis detailing which lab parameters fall outside standard reference ranges with their associated clinical guidelines.",
    agent=analyzer_agent
)

# 3. Plain-Language Translator Task (Multi-Lingual: English, Sinhala, Tamil)
translator_task = Task(
    description=(
        "Take the lab findings and out-of-bounds metrics from the Medical Analyzer Agent and translate them "
        "into a structured, highly compassionate, patient-friendly guidance report in the specified target language: '{language}'.\n\n"
        "IMPORTANT MULTI-LINGUAL INSTRUCTIONS:\n"
        "- If target language is 'සිංහල (Sinhala)', write the entire response in clear, compassionate, natural Sinhala (සිංහල).\n"
        "- If target language is 'தமிழ் (Tamil)', write the entire response in clear, compassionate, natural Tamil (தமிழ்).\n"
        "- If target language is 'English', write the entire response in clear English.\n\n"
        "Format using clear markdown with the following structure:\n"
        "### 🏥 Executive Summary / සාරාංශය / විධායක සාරාංශය\n"
        "A warm, supportive opening summarizing overall lab findings and reassuring the patient.\n\n"
        "### 📊 Lab Vitals & Reference Analysis / පරීක්ෂණ වාර්තා විශ්ලේෂණය\n"
        "Explain what each measured value means in plain language compared to standard reference ranges.\n\n"
        "### 💡 Lifestyle & Health Guidance / සෞඛ්‍ය උපදෙස් හා ජීවන රටාව\n"
        "3-4 actionable dietary, exercise, and wellness recommendations based on guidelines.\n\n"
        "### 🩺 Recommended Next Steps / ඊළඟට ගත යුතු පියවර\n"
        "Encouraging guidance on discussing results with their primary care physician."
    ),
    expected_output="A compassionate, beautifully formatted markdown patient educational report written in the chosen language ({language}).",
    agent=translator_agent
)

# 4. Clinical Guardrail Task (Reviewer / Safety Auditor)
guardrail_task = Task(
    description=(
        "Review the drafted patient report written in '{language}' to strictly enforce clinical safety and non-diagnostic guardrails:\n"
        "1. Ensure NO definitive medical diagnosis is rendered (do NOT state 'you have disease X').\n"
        "2. Confirm all medical jargon is translated into simple, accessible language ({language}).\n"
        "3. Verify that the report explicitly reminds the patient that this guidance is educational and directs them to consult a qualified physician for clinical diagnosis.\n\n"
        "Output the audited, final guidance report in '{language}'."
    ),
    expected_output="The finalized, audited markdown patient educational report written in {language} that strictly complies with non-diagnostic safety guardrails.",
    agent=guardrail_agent
)

# Assemble 4-Agent Sequential Crew
clearlab_crew = Crew(
    agents=[extraction_agent, analyzer_agent, translator_agent, guardrail_agent],
    tasks=[extraction_task, analyzer_task, translator_task, guardrail_task],
    process=Process.sequential,
    verbose=True
)

def run_lab_analysis(lab_text: str, language: str = "English") -> str:
    """Executes 4-agent RAG workflow on lab report text input in the chosen language."""
    # Truncate lab_text if too long to prevent TPM rate limits
    safe_text = lab_text[:2500] if lab_text else ""
    inputs = {
        "lab_text": safe_text,
        "language": language
    }
    result = clearlab_crew.kickoff(inputs=inputs)
    return str(result.raw) if hasattr(result, 'raw') else str(result)
