import os
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv
from pdf_generator import generate_clinical_pdf
from tools import extract_text_from_file

@st.dialog("Health Guidance Assessment", width="large")
def show_report_modal(report_text_name: str, report_output: str, language: str):
    """Centered popup modal displaying the structured lab analysis report."""
    st.markdown(f"""
    <div style="background: #ffffff; color: #0f172a; border-radius: 14px; padding: 1.2rem 1.5rem; margin-bottom: 1.2rem; border-left: 6px solid #10b981; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 800; font-size: 1.2rem; color: #047857;">Physician-Grade Health Guidance ({language})</span>
            <span style="background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 0.35rem 0.85rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
                Source: {report_text_name}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render structured markdown report
    st.markdown(report_output)
    
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.15); margin: 1.5rem 0 1rem 0;'>", unsafe_allow_html=True)
    
    # Generate & Download PDF Report
    pdf_bytes = generate_clinical_pdf(0.0, 0.0, f"LAB REPORT GUIDANCE ({language})", report_output)
    st.download_button(
        label="Download Official Assessment Report (PDF)",
        data=pdf_bytes,
        file_name=f"Health_care_AI_Guidance_Report_{language.split()[0]}.pdf",
        mime="application/pdf",
        key="modal_pdf_download_btn"
    )

# Page configuration - Health care AI Branding
st.set_page_config(
    page_title="Health care AI | Universal Multi-Lingual Lab Report Interpreter",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment keys
load_dotenv()

# Custom CSS for SaaS Dark-Grey + Crisp White + Neon Mint Green & Cyan Gradient Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 80% 20%, #0f1c18 0%, #090d14 60%, #05080e 100%);
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
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .nav-logo {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.4rem;
        font-weight: 800;
        color: #ffffff;
    }

    .nav-logo-icon {
        background: rgba(0, 230, 118, 0.15);
        border: 1px solid rgba(0, 230, 118, 0.4);
        border-radius: 10px;
        padding: 0.4rem 0.6rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Left Hero Column Styling */
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(0, 230, 118, 0.08);
        border: 1px solid rgba(0, 230, 118, 0.3);
        color: #00e676;
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
        color: #00e676;
        background: linear-gradient(135deg, #00e676 0%, #38ef7d 100%);
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

    /* Radio Language Selector Label */
    div[data-testid="stRadio"] label {
        color: #00e676 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }

    /* File Uploader Label Styling */
    .stFileUploader label {
        color: #f8fafc !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Refined Button Styling - Synchronized & Theme Aligned */
    div[data-testid="stButton"] > button,
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"],
    div.stButton > button {
        height: 46px !important;
        min-height: 46px !important;
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

    /* Primary Action CTA Button: Cyan/Blue & Neon Mint Gradient */
    div[data-testid="stColumn"] div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #00e676 0%, #00b0ff 100%) !important;
        color: #061510 !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.4) !important;
        cursor: pointer !important;
    }

    div[data-testid="stColumn"] div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #00f080 0%, #00e5ff 100%) !important;
        box-shadow: 0 8px 25px rgba(0, 230, 118, 0.6) !important;
        transform: translateY(-1px) !important;
    }

    /* Download PDF Button Styling */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35) !important;
        transition: all 0.25s ease-in-out !important;
        cursor: pointer !important;
        margin-top: 0.5rem !important;
    }

    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Navigation Bar
st.markdown("""
<div class="navbar">
    <div class="nav-logo">
        <div class="nav-logo-icon">❤️</div>
        Health care AI
    </div>
</div>
""", unsafe_allow_html=True)

# Split Hero & Dashboard Layout
col_left, col_right = st.columns([1.15, 1], gap="large")

with col_left:
    st.markdown("""
    <div class="hero-pill">⚡ Multi-Lingual Patient Health Intelligence</div>
    <div class="hero-title">
        Decode Your Medical <span class="hero-highlight">Lab Reports</span> Instantly
    </div>
    <div class="hero-description">
        Upload your medical lab report (PDF or TXT) to decode complex clinical findings. Receive physician-grade health guidance and standard reference range analysis translated into <b>English</b>, <b>සිංහල (Sinhala)</b>, or <b>தமிழ் (Tamil)</b>.
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # File Uploader for PDF / TXT / Image (PNG, JPG, JPEG)
    uploaded_file = st.file_uploader(
        "Upload Patient Lab Report (PDF / TXT / Image)",
        type=["pdf", "txt", "png", "jpg", "jpeg"],
        help="Upload a PDF, TXT, or Image (PNG/JPG) lab report photo to extract and interpret findings via OCR."
    )

    extracted_text = ""
    file_name = "Uploaded File"

    if uploaded_file is not None:
        file_name = uploaded_file.name
        extracted_text = extract_text_from_file(uploaded_file)
        if extracted_text and not extracted_text.startswith("Error"):
            st.success(f"Report Loaded Successfully! ({len(extracted_text)} characters extracted)")
        else:
            st.warning("Could not extract text from file. Please ensure it is a valid PDF, TXT, or legible Image file.")

    # Multi-Lingual Guidance Language Selector
    selected_lang = st.radio(
        "Select Guidance Language / භාෂාව තෝරන්න / மொழியைத் தேர்ந்தெடுக்கவும்:",
        ["English", "සිංහල (Sinhala)", "தமிழ் (Tamil)"],
        horizontal=True,
        help="Choose the language for your personalized clinical guidance report."
    )

    st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        run_analysis = st.button("Analyze Lab Report →", key="run_analysis_btn")
    with btn_col2:
        reopen_analysis = st.button("View Saved Report", key="reopen_report_btn")

    if run_analysis:
        if not extracted_text:
            st.error("No Lab Report Uploaded! Please upload a PDF or TXT lab report file first.")
        else:
            g_key = os.environ.get("GROQ_API_KEY", "")
            or_key = os.environ.get("OPENROUTER_API_KEY", "")
            
            if not g_key or g_key == "your_groq_api_key_here" or not or_key or or_key == "your_openrouter_api_key_here":
                st.error("API Keys Missing! Please ensure GROQ_API_KEY and OPENROUTER_API_KEY are configured in your `.env` file or Streamlit Secrets.")
            else:
                with st.status(f"Executing 4-Agent RAG Flow ({selected_lang})...", expanded=True) as status:
                    try:
                        status.write("1. Extraction Agent: Extracting raw text from lab report...")
                        status.write("2. Medical Analyzer Agent: Querying ChromaDB reference ranges for out-of-bounds metrics...")
                        from crew_logic import run_lab_analysis
                        
                        status.write(f"3. Translator Agent: Translating medical jargon into {selected_lang}...")
                        status.write("4. Clinical Guardrail Agent: Auditing report to enforce non-diagnostic safety rules...")
                        
                        report_output = run_lab_analysis(lab_text=extracted_text, language=selected_lang)
                        
                        st.session_state["last_report"] = {
                            "file_name": file_name,
                            "report_output": report_output,
                            "language": selected_lang
                        }
                        
                        status.update(label=f"4-Agent Analysis Complete ({selected_lang})! Opening Guidance Modal...", state="complete", expanded=False)
                        
                        # Open centered popup modal
                        show_report_modal(file_name, report_output, selected_lang)
                        
                    except Exception as e:
                        status.update(label="Analysis Encountered an Error", state="error")
                        st.error(f"An error occurred during agent execution: {str(e)}")

    if reopen_analysis:
        last = st.session_state.get("last_report")
        if last and isinstance(last, dict) and last.get("report_output"):
            show_report_modal(last.get("file_name", "Uploaded File"), last.get("report_output", ""), last.get("language", "English"))
        else:
            st.info("Please click **'Analyze Lab Report →'** first to generate your guidance report!")
