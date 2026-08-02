import os
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv
from pdf_generator import generate_clinical_pdf
from tools import predict_heart_disease, extract_text_from_file, extract_vitals_from_text

def create_risk_gauge_chart(risk_level: str):
    """
    Creates a visual Gauge Chart using plotly.graph_objects (go.Indicator).
    - HIGH RISK -> value 85
    - LOW RISK -> value 15
    - Transparent background (paper_bgcolor & plot_bgcolor = rgba(0,0,0,0))
    - Deep purple and subtle neon-lit accents matching the glassmorphism dark aesthetic.
    """
    is_high_risk = "HIGH" in str(risk_level).upper()
    gauge_val = 85 if is_high_risk else 15
    
    gauge_bar_color = "#9333ea" if is_high_risk else "#10b981"
    accent_glow_color = "#c084fc" if is_high_risk else "#34d399"
    status_label = "HIGH RISK" if is_high_risk else "LOW RISK"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_val,
        number={
            'suffix': "%", 
            'font': {'size': 42, 'color': '#ffffff', 'family': 'Plus Jakarta Sans, sans-serif'}
        },
        title={
            'text': f"<b>DIAGNOSTIC RISK SCORE: {status_label}</b>", 
            'font': {'size': 16, 'color': accent_glow_color, 'family': 'Plus Jakarta Sans, sans-serif'}
        },
        gauge={
            'axis': {
                'range': [0, 100], 
                'tickwidth': 1, 
                'tickcolor': "#64748b", 
                'tickfont': {'color': '#94a3b8', 'size': 11}
            },
            'bar': {
                'color': gauge_bar_color, 
                'thickness': 0.35
            },
            'bgcolor': "rgba(15, 23, 42, 0.6)",
            'borderwidth': 1.5,
            'bordercolor': "rgba(168, 85, 247, 0.3)",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(16, 185, 129, 0.18)'},
                {'range': [30, 70], 'color': 'rgba(168, 85, 247, 0.15)'},
                {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.18)'}
            ],
            'threshold': {
                'line': {'color': accent_glow_color, 'width': 4},
                'thickness': 0.75,
                'value': gauge_val
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#f8fafc", 'family': "Plus Jakarta Sans, sans-serif"},
        height=240,
        margin=dict(l=20, r=20, t=40, b=10)
    )
    return fig

@st.dialog("💚 Patient Clinical Assessment Report", width="large")
def show_report_modal(chol: float, thalach: float, diag_prediction: str, report_output: str):
    """Centered popup modal displaying the diagnostic gauge chart and clinical report."""
    # Render Plotly Gauge Chart inside centered popup
    gauge_fig = create_risk_gauge_chart(diag_prediction)
    st.plotly_chart(gauge_fig, use_container_width=True)
    
    # Display Result Header & Badge
    st.markdown(f"""
    <div style="background: #ffffff; color: #0f172a; border-radius: 14px; padding: 1.2rem 1.5rem; margin-bottom: 1.2rem; border-left: 6px solid #10b981; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 800; font-size: 1.2rem; color: #047857;">💚 Physician-Grade Clinical Assessment</span>
            <span style="background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 0.35rem 0.85rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
                Cholesterol: {int(chol)} mg/dL | Max HR: {int(thalach)} bpm
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render structured markdown report
    st.markdown(report_output)
    
    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.15); margin: 1.5rem 0 1rem 0;'>", unsafe_allow_html=True)
    
    # Generate & Download PDF Report
    pdf_bytes = generate_clinical_pdf(chol, thalach, diag_prediction, report_output)
    st.download_button(
        label="📥 Download Official Assessment Report (PDF)",
        data=pdf_bytes,
        file_name=f"CardioCare_Report_{int(chol)}mgdl_{int(thalach)}bpm.pdf",
        mime="application/pdf",
        key="modal_pdf_download_btn"
    )

# Page configuration
st.set_page_config(
    page_title="CardioCare AI | Patient Lab Report Interpreter",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment keys
load_dotenv()

# Clean, Modern CSS for SaaS Lab Report Interpreter Interface
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

    /* Left Hero Column */
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
        height: 46px !important;
        min-height: 46px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.25s ease-in-out !important;
        margin-top: 0.6rem !important;
        box-sizing: border-box !important;
    }

    /* Primary Action CTA Button */
    div[data-testid="stColumn"]:nth-of-type(1) div[data-testid="stButton"] > button,
    div[data-testid="stColumn"]:first-child div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #00e676 0%, #00b0ff 100%) !important;
        color: #061510 !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.4) !important;
        cursor: pointer !important;
    }

    div[data-testid="stColumn"]:nth-of-type(1) div[data-testid="stButton"] > button:hover,
    div[data-testid="stColumn"]:first-child div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #00f080 0%, #00e5ff 100%) !important;
        box-shadow: 0 8px 25px rgba(0, 230, 118, 0.6) !important;
        transform: translateY(-1px) !important;
    }

    /* Download PDF Button */
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
        CardioCare AI
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize Session State Values for Vitals
if "chol_val" not in st.session_state:
    st.session_state["chol_val"] = 245.0
if "thalach_val" not in st.session_state:
    st.session_state["thalach_val"] = 142.0

# Split Hero & Dashboard Layout
col_left, col_right = st.columns([1.15, 1], gap="large")

with col_left:
    st.markdown("""
    <div class="hero-pill">⚡ Patient-Friendly Lab Report Interpreter</div>
    <div class="hero-title">
        Understand Your Lab Reports with <span class="hero-highlight">Agentic AI</span>
    </div>
    <div class="hero-description">
        Upload your medical lab report (PDF/TXT) to receive instant, physician-grade guidance. Our multi-agent AI system evaluates cardiac vitals, assesses health risk flags, and translates complex clinical jargon into plain-English health insights.
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # File Uploader
    uploaded_file = st.file_uploader(
        "Upload Patient Lab Report (PDF / TXT)",
        type=["pdf", "txt"],
        help="Upload a PDF or TXT lab report file to automatically extract patient vitals."
    )

    chol = float(st.session_state.get("chol_val", 245.0))
    thalach = float(st.session_state.get("thalach_val", 142.0))

    if uploaded_file is not None:
        file_text = extract_text_from_file(uploaded_file)
        if file_text:
            extracted = extract_vitals_from_text(file_text)
            chol = extracted["chol"]
            thalach = extracted["thalach"]
            st.session_state["chol_val"] = chol
            st.session_state["thalach_val"] = thalach
            st.success(f"📄 Report Parsed Successfully! Cholesterol: {int(chol)} mg/dL, Max HR: {int(thalach)} bpm")
    else:
        st.markdown(f"""
        <div style="background: rgba(0, 230, 118, 0.08); border: 1px solid rgba(0, 230, 118, 0.3); border-radius: 12px; padding: 0.85rem 1.2rem; margin-bottom: 1.2rem;">
            <div style="font-size: 0.82rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Active Patient Lab Vitals:</div>
            <div style="font-size: 1.05rem; color: #00e676; font-weight: 700; margin-top: 0.2rem;">
                Total Cholesterol: {int(chol)} mg/dL &nbsp;|&nbsp; Max Heart Rate: {int(thalach)} bpm
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #a78bfa; margin-bottom: 0.4rem;'>📋 Or Try A Quick Sample Lab Report:</div>", unsafe_allow_html=True)
    sample_col1, sample_col2 = st.columns(2)
    with sample_col1:
        if st.button("⚠️ High Risk Sample", key="sample_high_btn"):
            st.session_state["chol_val"] = 265.0
            st.session_state["thalach_val"] = 130.0
            st.toast("Loaded High Risk Sample: Cholesterol=265 mg/dL, Max HR=130 bpm")
            st.rerun()

    with sample_col2:
        if st.button("✅ Normal Vitals Sample", key="sample_normal_btn"):
            st.session_state["chol_val"] = 185.0
            st.session_state["thalach_val"] = 165.0
            st.toast("Loaded Normal Vitals Sample: Cholesterol=185 mg/dL, Max HR=165 bpm")
            st.rerun()

    st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
    run_analysis = st.button("🔍 Analyze Lab Report & Generate Guidance →", key="run_analysis_btn")

    if run_analysis:
        g_key = os.environ.get("GROQ_API_KEY", "")
        or_key = os.environ.get("OPENROUTER_API_KEY", "")
        
        if not g_key or g_key == "your_groq_api_key_here" or not or_key or or_key == "your_openrouter_api_key_here":
            st.error("⚠️ **API Keys Missing!** Please ensure GROQ_API_KEY and OPENROUTER_API_KEY are configured in your `.env` file or Streamlit Secrets.")
        else:
            with st.status("🧬 Analyzing patient parameters with AI agents...", expanded=True) as status:
                try:
                    status.write("🧠 Diagnostic Agent: Executing ML Classifier...")
                    from crew_logic import run_clinical_analysis
                    
                    diag_prediction = predict_heart_disease.func(chol, thalach)
                    
                    status.write("📚 Reporting Agent: Querying ChromaDB RAG Guidelines...")
                    status.write("✍️ Synthesizing Empathetic Clinical Report...")
                    status.write("🔍 Critique Agent: Auditing Report for Safety & Empathy...")
                    
                    report_output = run_clinical_analysis(chol=chol, thalach=thalach)
                    
                    # Store generated report in session state
                    st.session_state["last_report"] = {
                        "chol": chol,
                        "thalach": thalach,
                        "diag_prediction": diag_prediction,
                        "report_output": report_output
                    }
                    
                    status.update(label="✅ Analysis Complete! Opening Report Modal...", state="complete", expanded=False)
                    
                    # Open centered popup modal with Gauge Chart & Report
                    show_report_modal(chol, thalach, diag_prediction, report_output)
                    
                except Exception as e:
                    status.update(label="❌ Analysis Encountered an Error", state="error")
                    st.error(f"An error occurred during agent execution: {str(e)}")
