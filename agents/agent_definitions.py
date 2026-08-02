import os
import crewai.llms.cache as _crewai_cache
# Disable CrewAI's automatic injection of cache_breakpoint to avoid Groq validation errors
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

from dotenv import load_dotenv
from crewai import Agent, LLM
from rag_setup import get_rag_tool

# Load environment keys
load_dotenv()

# Use OpenRouter LLMs for high token throughput and zero TPM rate limit errors
openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
groq_api_key = os.getenv("GROQ_API_KEY", "")

primary_llm = LLM(
    model=os.getenv("OPENROUTER_MODEL", "openrouter/google/gemma-4-26b-a4b-it:free"),
    api_key=openrouter_api_key if openrouter_api_key else groq_api_key,
    base_url="https://openrouter.ai/api/v1" if openrouter_api_key else None
)

fast_llm = LLM(
    model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
    api_key=openrouter_api_key if openrouter_api_key else groq_api_key,
    base_url="https://openrouter.ai/api/v1" if openrouter_api_key else None
)

# 1. Extraction Agent
extraction_agent: Agent = Agent(
    role="Lab Data Extraction Specialist",
    goal="Extract and structure raw text content, lab parameter names, and measured numerical values from uploaded lab reports.",
    backstory="You are a meticulous clinical data extraction specialist. You parse raw lab report text, extract key health parameters (lipid, glucose, CBC, kidney/liver markers), and prepare structured data for clinical reference analysis.",
    llm=fast_llm,
    verbose=True
)

# 2. Medical Analyzer Agent (RAG)
analyzer_agent: Agent = Agent(
    role="Medical Reference Analyzer",
    goal="Evaluate extracted lab parameters against ChromaDB standard medical reference ranges to identify out-of-range values and health flags.",
    backstory="You are an expert clinical pathologist and data analyst. You use the Medical Guidelines Retriever tool to search verified reference ranges in ChromaDB and categorize measured lab values into normal, borderline, or elevated flags.",
    tools=[get_rag_tool()],
    llm=primary_llm,
    verbose=True
)

# 3. Plain-English Translator Agent
translator_agent: Agent = Agent(
    role="Plain-English Medical Translator",
    goal="Translate out-of-bounds lab findings and medical jargon into compassionate, easy-to-understand patient health guidance.",
    backstory="You are a compassionate patient health educator. Your strength lies in breaking down complex lab terminology into clear, reassuring, and practical explanations that any patient can easily understand.",
    llm=primary_llm,
    verbose=True
)

# 4. Clinical Guardrail Agent (Reviewer)
guardrail_agent: Agent = Agent(
    role="Clinical Safety & Guardrail Reviewer",
    goal="Audit the drafted patient guidance report to strictly enforce safety constraints: ensure NO medical diagnosis is made and direct the patient to consult a qualified physician.",
    backstory="You are a rigorous clinical compliance officer and safety auditor. You review patient communications to ensure they are 100% educational, non-diagnostic, compassionate, and contain proper physician disclaimers.",
    llm=fast_llm,
    verbose=True
)
