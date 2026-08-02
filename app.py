import os
import streamlit as st
from dotenv import load_dotenv
from pdf_generator import generate_clinical_pdf
from tools import extract_text_from_file

@st.dialog("🧪 ClearLab AI — Patient Health Guidance Report", width="large")
def show_report_modal(report_text_name: str, report_output: str):
    """Centered popup modal displaying the structured lab analysis report."""
    st.markdown(f"""
    <div style="background: rgba(30, 20, 50, 0.95); color: #ffffff; border-radius: 14px; padding: 1.2rem 1.5rem; margin-bottom: 1.2rem; border-left: 6px solid #a78bfa; border: 1px solid rgba(167, 139, 250, 0.3); box-shadow: 0 8px 25px rgba(0,0,0,0.4);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 800; font-size: 1.2rem; color: #a78bfa;">🧪 ClearLab AI — Patient Educational Guidance</span>
            <span style="background: rgba(167, 139, 250, 0.15); color: #c084fc; border: 1px solid rgba(167, 139, 250, 0.4); padding: 0.35rem 0.85rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
                Source: {report_text_name}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render structured markdown report
    st.markdown(report_output)
    
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.15); margin: 1.5rem 0 1rem 0;'>", unsafe_allow_html=True)
    
    # Generate & Download PDF Report
    pdf_bytes = generate_clinical_pdf(0.0, 0.0, "LAB REPORT GUIDANCE", report_output)
    st.download_button(
        label="📥 Download Patient Guidance Report (PDF)",
        data=pdf_bytes,
        file_name="ClearLab_AI_Patient_Guidance_Report.pdf",
        mime="application/pdf",
        key="modal_pdf_download_btn"
    )

# Page configuration - ClearLab AI Branding
st.set_page_config(
    page_title="ClearLab AI | General Lab Report Interpreter & Educator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment keys
load_dotenv()

# Modern Deep Purple & Neon Glassmorphism Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 80% 20%, #1e1038 0%, #0c071a 60%, #050110 100%);
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px !important;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Top Navigation Bar */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(138, 43, 226, 0.2);
    }

    .nav-logo {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.45rem;
        font-weight: 800;
        color: #ffffff;
    }

    .nav-logo-icon {
        background: rgba(138, 43, 226, 0.25);
        border: 1px solid rgba(167, 139, 250, 0.4);
        border-radius: 10px;
        padding: 0.4rem 0.6rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Left Hero Column */
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(167, 139, 250, 0.12);
        border: 1px solid rgba(167, 139, 250, 0.35);
        color: #c084fc;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1.15;
        color: #ffffff;
        margin-bottom: 1.2rem;
        letter-spacing: -1px;
    }

    .hero-highlight {
        background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        font-size: 1.05rem;
        color: #94a3b8;
        line-height: 1.65;
        margin-bottom: 1.8rem;
        max-width: 540px;
        font-weight: 400;
    }

    /* Glass Workspace Card Container */
    .glass-card {
        background: rgba(30, 20, 50, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(138, 43, 226, 0.3);
        border-radius: 20px;
        padding: 2.2rem;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), 0 0 25px rgba(138, 43, 226, 0.15);
        margin-bottom: 1.5rem;
    }

    /* File Uploader Container */
    .stFileUploader label {
        color: #f8fafc !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Buttons Styling */
    div[data-testid="stButton"] > button,
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"],
    div.stButton > button {
        height: 48px !important;
        min-height: 48px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.4rem !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.25s ease-in-out !important;
        margin-top: 0.8rem !important;
        box-sizing: border-box !important;
    }

    /* Primary Action CTA Button */
    div[data-testid="stColumn"] div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(167, 139, 250, 0.5) !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.45) !important;
        cursor: pointer !important;
    }

    div[data-testid="stColumn"] div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #5b21b6 100%) !important;
        box-shadow: 0 6px 28px rgba(139, 92, 246, 0.65) !important;
        transform: translateY(-2px) !important;
    }

    /* Download PDF Button */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border: 1px solid rgba(167, 139, 250, 0.4) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.35) !important;
        transition: all 0.25s ease-in-out !important;
        cursor: pointer !important;
        margin-top: 0.5rem !important;
    }

    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #5b21b6 100%) !important;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5) !important;
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Navigation Bar
st.markdown("""
<div class="navbar">
    <div class="nav-logo">
        <div class="nav-logo-icon">🧪</div>
        ClearLab AI
    </div>
</div>
""", unsafe_allow_html=True)

# Split Hero & Dashboard Layout
col_left, col_right = st.columns([1.15, 1], gap="large")

with col_left:
    st.markdown("""
    <div class="hero-pill">⚡ Multi-Agent RAG Medical Guidance</div>
    <div class="hero-title">
        ClearLab AI: General Lab Report <span class="hero-highlight">Interpreter & Educator</span>
    </div>
    <div class="hero-description">
        Upload any medical lab report (PDF or TXT) to receive clear, patient-friendly guidance. Our 4-agent AI system extracts lab data, queries reference guidelines, translates complex jargon, and strictly ensures safe, educational insights without making medical diagnoses.
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # File Uploader for PDF / TXT
    uploaded_file = st.file_uploader(
        "Upload Patient Lab Report (PDF / TXT)",
        type=["pdf", "txt"],
        help="Upload a PDF or TXT lab report file to extract and interpret findings."
    )

    extracted_text = ""
    file_name = "Uploaded File"

    if uploaded_file is not None:
        file_name = uploaded_file.name
        extracted_text = extract_text_from_file(uploaded_file)
        if extracted_text and not extracted_text.startswith("Error"):
            st.success(f"📄 **Report Loaded Successfully!** ({len(extracted_text)} characters extracted)")
        else:
            st.warning("⚠️ Could not extract text from file. Please ensure it is a valid PDF or TXT file.")

    st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)
    run_analysis = st.button("🔍 Analyze Lab Report & Generate Guidance →", key="run_analysis_btn")
    
    st.markdown('</div>', unsafe_allow_html=True)

    if run_analysis:
        if not extracted_text:
            st.error("⚠️ **No Lab Report Uploaded!** Please upload a PDF or TXT lab report file first.")
        else:
            g_key = os.environ.get("GROQ_API_KEY", "")
            or_key = os.environ.get("OPENROUTER_API_KEY", "")
            
            if not g_key or g_key == "your_groq_api_key_here" or not or_key or or_key == "your_openrouter_api_key_here":
                st.error("⚠️ **API Keys Missing!** Please ensure GROQ_API_KEY and OPENROUTER_API_KEY are configured in your `.env` file or Streamlit Secrets.")
            else:
                with st.status("🧬 Executing 4-Agent RAG Orchestration Flow...", expanded=True) as status:
                    try:
                        status.write("📄 1. Extraction Agent: Extracting raw text from lab report...")
                        status.write("📚 2. Medical Analyzer Agent: Querying ChromaDB reference ranges for out-of-bounds metrics...")
                        from crew_logic import run_lab_analysis
                        
                        status.write("✍️ 3. Plain-English Translator Agent: Translating medical jargon into patient guidance...")
                        status.write("🛡️ 4. Clinical Guardrail Agent: Auditing report to enforce non-diagnostic safety rules...")
                        
                        report_output = run_lab_analysis(lab_text=extracted_text)
                        
                        st.session_state["last_report"] = {
                            "file_name": file_name,
                            "report_output": report_output
                        }
                        
                        status.update(label="✅ 4-Agent Analysis Complete! Opening Guidance Modal...", state="complete", expanded=False)
                        
                        # Open centered popup modal
                        show_report_modal(file_name, report_output)
                        
                    except Exception as e:
                        status.update(label="❌ Analysis Encountered an Error", state="error")
                        st.error(f"An error occurred during agent execution: {str(e)}")
