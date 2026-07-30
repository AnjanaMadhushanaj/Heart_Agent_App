import os
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

# Page configuration - Deep Purple Glassmorphism Aesthetic
st.set_page_config(
    page_title="CardioCare AI | Clinical Decision Support System",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment keys
load_dotenv()

# 1. Comprehensive CSS Injection for Deep Purple Glassmorphism Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Force Pure Dark Deep Purple App Background */
    .stApp {
        background-color: #050110 !important;
        background-image: radial-gradient(circle at 50% 15%, #1e1038 0%, #050110 75%) !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Hide default Streamlit top header bar */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Container constraints */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 3rem !important;
        max-width: 1050px !important;
    }

    /* Top Navigation Bar */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.9rem 1.6rem;
        margin-bottom: 2.2rem;
        background: rgba(25, 14, 45, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(138, 43, 226, 0.3);
        border-radius: 18px;
    }

    .nav-logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.45rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
    }

    .nav-logo-icon {
        background: rgba(138, 43, 226, 0.25);
        border: 1px solid rgba(167, 139, 250, 0.4);
        border-radius: 10px;
        padding: 0.35rem 0.6rem;
        font-size: 1.25rem;
    }

    .nav-tag {
        background: rgba(167, 139, 250, 0.12);
        border: 1px solid rgba(167, 139, 250, 0.35);
        color: #c084fc;
        font-size: 0.82rem;
        font-weight: 700;
        padding: 0.35rem 0.95rem;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }

    /* Hero Section */
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }

    .hero-highlight {
        background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2.2rem;
        max-width: 750px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
        font-weight: 400;
    }

    /* Glass Container Class for Inputs */
    .glass-container {
        background: rgba(30, 20, 50, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(138, 43, 226, 0.3) !important;
        border-radius: 20px !important;
        padding: 2.2rem !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37),
                    0 0 25px 0 rgba(138, 43, 226, 0.15) !important;
        margin-bottom: 2rem !important;
    }

    /* Input Controls Styling */
    div[data-baseweb="input"] {
        background-color: rgba(15, 10, 30, 0.65) !important;
        border: 1px solid rgba(138, 43, 226, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #a78bfa !important;
        box-shadow: 0 0 18px rgba(167, 139, 250, 0.45) !important;
    }

    .stNumberInput label {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Centered Button Row Layout & Custom CSS Button Styling */
    div[data-testid="stButton"] > button,
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"],
    div.stButton > button {
        height: 50px !important;
        min-height: 50px !important;
        max-height: 50px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.6rem !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        box-sizing: border-box !important;
    }

    /* Primary CTA Button: Run Clinical Analysis (.primary-btn) */
    div[data-testid="stColumn"]:nth-of-type(1) div[data-testid="stButton"] > button,
    div[data-testid="stColumn"]:first-child div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(167, 139, 250, 0.5) !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.45) !important;
        cursor: pointer !important;
    }

    div[data-testid="stColumn"]:nth-of-type(1) div[data-testid="stButton"] > button:hover,
    div[data-testid="stColumn"]:first-child div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #5b21b6 100%) !important;
        box-shadow: 0 6px 28px rgba(139, 92, 246, 0.65) !important;
        transform: translateY(-2px) !important;
    }

    /* Secondary Action Button: View Assessment Report (.secondary-btn) */
    div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stButton"] > button,
    div[data-testid="stColumn"]:last-child div[data-testid="stButton"] > button {
        background: rgba(124, 58, 237, 0.18) !important;
        color: #c084fc !important;
        border: 1.5px solid rgba(192, 132, 252, 0.45) !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.25) !important;
        cursor: pointer !important;
    }

    div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stButton"] > button:hover,
    div[data-testid="stColumn"]:last-child div[data-testid="stButton"] > button:hover {
        background: rgba(124, 58, 237, 0.32) !important;
        border-color: #c084fc !important;
        box-shadow: 0 6px 24px rgba(192, 132, 252, 0.45) !important;
        transform: translateY(-2px) !important;
    }

    div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stButton"] > button:disabled,
    div[data-testid="stColumn"]:last-child div[data-testid="stButton"] > button:disabled {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #64748b !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        opacity: 0.65 !important;
    }

    /* Dedicated Glassmorphism Report Box */
    .report-glass-box {
        background: rgba(22, 14, 42, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(167, 139, 250, 0.35) !important;
        border-radius: 20px !important;
        padding: 2.2rem !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5),
                    0 0 30px rgba(138, 43, 226, 0.2) !important;
        color: #f1f5f9 !important;
        margin-top: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function for Plotly Gauge Chart inside modal popup
def create_risk_gauge_chart(risk_level: str):
    """
    Creates a Plotly Gauge Chart for Cardiovascular Risk Score.
    HIGH RISK -> value 85, Deep Purple & Neon Red accents
    LOW RISK -> value 15, Deep Purple & Emerald Green accents
    """
    is_high_risk = "HIGH" in str(risk_level).upper()
    gauge_val = 85 if is_high_risk else 15
    
    gauge_bar_color = "#9333ea" if is_high_risk else "#10b981"
    accent_glow_color = "#c084fc" if is_high_risk else "#34d399"
    status_label = "HIGH RISK DETECTED" if is_high_risk else "LOW RISK ASSESSMENT"
    
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

# Centered Popup Modal
@st.dialog("💜 Patient Clinical Assessment Report", width="large")
def show_report_modal(chol: float, thalach: float, diag_prediction: str, report_output: str):
    """Centered popup modal displaying the diagnostic gauge chart and full clinical report."""
    gauge_fig = create_risk_gauge_chart(diag_prediction)
    st.plotly_chart(gauge_fig, use_container_width=True)
    
    st.markdown(f"""
    <div style="background: rgba(30, 18, 55, 0.9); border-left: 6px solid #a78bfa; border-top: 1px solid rgba(167, 139, 250, 0.3); border-right: 1px solid rgba(167, 139, 250, 0.3); border-bottom: 1px solid rgba(167, 139, 250, 0.3); border-radius: 14px; padding: 1.2rem 1.5rem; margin-bottom: 1.2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 800; font-size: 1.2rem; color: #ffffff;">💜 Physician-Grade Clinical Assessment</span>
            <span style="background: rgba(167, 139, 250, 0.15); color: #c084fc; border: 1px solid rgba(167, 139, 250, 0.4); padding: 0.35rem 0.85rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
                Cholesterol: {int(chol)} mg/dL | Max HR: {int(thalach)} bpm
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display full report text cleanly
    st.markdown(report_output)

# 2. Top Navigation Bar
st.markdown("""
<div class="navbar">
    <div class="nav-logo">
        <div class="nav-logo-icon">❤️</div>
        CardioCare AI
    </div>
    <div class="nav-tag">CLINICAL DECISION SUPPORT SYSTEM</div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-title">
    Cardiovascular Risk Assessment with <span class="hero-highlight">Agentic AI</span>
</div>
<div class="hero-subtitle">
    Advanced AI-powered cardiovascular intelligence designed to assist clinical decision-making. Our multi-agent system evaluates key patient vitals against verified medical guidelines to deliver accurate, empathetic, and physician-grade heart health assessments.
</div>
""", unsafe_allow_html=True)

# 3. Layout Refactor: Single Styled Glass Container for Inputs
st.markdown('<div class="glass-container">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    chol = st.number_input(
        "Total Cholesterol (mg/dL)",
        min_value=50.0,
        max_value=600.0,
        value=245.0,
        step=1.0,
        help="Normal is below 200 mg/dL. High risk is classified above 240 mg/dL."
    )

with col2:
    thalach = st.number_input(
        "Maximum Heart Rate Achieved (bpm)",
        min_value=50.0,
        max_value=250.0,
        value=142.0,
        step=1.0,
        help="Expected range during exercise stress testing is 60 to 200 bpm."
    )

st.markdown('</div>', unsafe_allow_html=True)

# 4. Buttons Row: Outside Container & Centrally Aligned
btn_space_left, btn_col1, btn_col2, btn_space_right = st.columns([0.5, 2, 2, 0.5])

with btn_col1:
    run_analysis = st.button("Run Clinical Analysis  →", key="run_analysis_btn")

with btn_col2:
    reopen_analysis = False
    if st.session_state.get("last_report") is not None:
        reopen_analysis = st.button("View Assessment Report", key="reopen_report_btn")
    else:
        st.button("View Assessment Report", key="disabled_report_btn", disabled=True, help="Run Clinical Analysis first to generate the report.")

# Execution Trigger
if run_analysis:
    g_key = os.environ.get("GROQ_API_KEY", "")
    or_key = os.environ.get("OPENROUTER_API_KEY", "")
    
    if not g_key or g_key == "your_groq_api_key_here" or not or_key or or_key == "your_openrouter_api_key_here":
        st.error("⚠️ **API Keys Missing!** Please ensure GROQ_API_KEY and OPENROUTER_API_KEY are configured in your `.env` file or Streamlit Secrets.")
    else:
        with st.status("🧬 Analyzing patient parameters with AI agents...", expanded=True) as status:
            try:
                status.write("🧠 Diagnostic Agent: Executing ML Classifier...")
                from tools import predict_heart_disease
                from crew_logic import run_clinical_analysis
                
                # Execute Diagnostic prediction
                diag_prediction = predict_heart_disease.func(chol, thalach)
                
                status.write("📚 Reporting Agent: Querying ChromaDB RAG Guidelines...")
                status.write("✍️ Synthesizing Empathetic Clinical Report...")
                status.write("🔍 Critique Agent: Auditing Report for Safety & Empathy...")
                
                report_output = run_clinical_analysis(chol=chol, thalach=thalach)
                
                # Store in session state
                st.session_state["last_report"] = {
                    "chol": chol,
                    "thalach": thalach,
                    "diag_prediction": diag_prediction,
                    "report_output": report_output
                }
                
                status.update(label="✅ Analysis Complete! Opening Report Modal...", state="complete", expanded=False)
                
                # Show centered modal popup
                show_report_modal(chol, thalach, diag_prediction, report_output)
                
            except Exception as e:
                status.update(label="❌ Analysis Encountered an Error", state="error")
                st.error(f"An error occurred during agent execution: {str(e)}")

if reopen_analysis:
    last = st.session_state["last_report"]
    show_report_modal(last["chol"], last["thalach"], last["diag_prediction"], last["report_output"])

# 5. Fix Report Text Display: Clean Glassmorphism Container Below Buttons
if st.session_state.get("last_report") is not None:
    last = st.session_state["last_report"]
    st.markdown('<div class="report-glass-box">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; border-bottom: 1px solid rgba(167, 139, 250, 0.2); padding-bottom: 0.8rem;">
        <span style="font-weight: 800; font-size: 1.25rem; color: #a78bfa;">💜 Patient Assessment Summary Report</span>
        <span style="background: rgba(167, 139, 250, 0.15); color: #c084fc; border: 1px solid rgba(167, 139, 250, 0.4); padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;">
            Cholesterol: {int(last['chol'])} mg/dL | Max HR: {int(last['thalach'])} bpm
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Display full report text clearly without truncation or ellipses
    st.markdown(last['report_output'])
    st.markdown('</div>', unsafe_allow_html=True)
