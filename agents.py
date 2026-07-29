import os
import crewai.llms.cache as _crewai_cache
# Disable CrewAI's automatic injection of cache_breakpoint to avoid Groq validation errors
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

from dotenv import load_dotenv
from crewai import Agent, LLM

# Import tools
from tools import predict_heart_disease
from rag_setup import get_rag_tool

# Load environment variables
load_dotenv()

# Define LLMs
groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

openrouter_llm = LLM(
    model=os.getenv("OPENROUTER_MODEL", "openrouter/google/gemma-4-26b-a4b-it:free"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# 1. Diagnostic Agent (Tool-use pattern)
# This agent handles running the Random Forest classifier on tabular patient inputs.
diagnostic_agent: Agent = Agent(
    role="Medical Data Analyzer",
    goal="Analyze tabular patient data using the Heart Disease Predictor tool to determine the risk of heart disease.",
    backstory="You are a precise and analytical clinical data scientist. You process patient vitals and lab results "
              "using trained machine learning models to provide objective diagnostic risk assessments.",
    tools=[predict_heart_disease],
    llm=groq_llm,
    verbose=True
)

# 2. Reporting Agent (RAG / Synthesis pattern)
# This agent translates clinical data and ChromaDB guidelines into a cohesive, structured report.
reporting_agent: Agent = Agent(
    role="Clinical Communicator",
    goal="Synthesize the diagnostic risk assessment with relevant medical guidelines from the RAG store to write a structured, highly professional, patient-friendly medical report.",
    backstory="You are an expert clinical communicator and physician advocate. Your strength lies in translating complex clinical metrics "
              "and evidence-based guidelines into clear, empathetic, beautifully structured medical reports that any patient can easily understand.",
    tools=[get_rag_tool()],
    llm=openrouter_llm,
    verbose=True
)

# 3. Critique Agent (Reflection/Self-Critique pattern)
# This agent ensures the report is medically accurate, empathetic, and safe (satisfying the 3rd agentic design pattern).
critique_agent: Agent = Agent(
    role="Clinical Reviewer",
    goal="Critique the drafted clinical report for medical accuracy, empathy, clear structure, and readability, and output the polished final report.",
    backstory="You are a senior medical reviewer and clinical quality assurance expert. You audit clinical communications "
              "to ensure they are structured with clear headings, scientifically accurate, easy to understand for patients, and contain supportive next steps.",
    llm=groq_llm,
    verbose=True
)
