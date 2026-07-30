import os
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

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
    
    # Deep purple and neon accent colors
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

# Page configuration - Wide layout for SaaS Landing Page & Dashboard aesthetic
st.set_page_config(
    page_title="CardioCare AI | Agentic Clinical Decision Support",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for SaaS Dark-Grey + Crisp White + Neon Mint Green Aesthetic (MediClaim AI style)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Main app background - Dark Matte Charcoal with subtle radial glow */
    .stApp {
        background: radial-gradient(circle at 80% 20%, #0f1c18 0%, #090d14 60%, #05080e 100%);
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Remove default padding & Streamlit header */
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
        letter-spacing: -0.5px;
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

    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
        font-size: 0.95rem;
        color: #94a3b8;
        font-weight: 500;
    }

    .nav-badge {
        background: linear-gradient(135deg, rgba(0, 230, 118, 0.2) 0%, rgba(0, 176, 255, 0.2) 100%);
        border: 1px solid rgba(0, 230, 118, 0.5);
        color: #00e676;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
        letter-spacing: 0.5px;
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
        font-size: 3.4rem;
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
        font-size: 1.1rem;
        color: #94a3b8;
        line-height: 1.6;
        margin-bottom: 2rem;
        max-width: 540px;
        font-weight: 400;
    }

    /* Pumping Blood Heart Animation Container */
    .hero-animation-box {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2rem 1.6rem;
        margin-bottom: 2rem;
        max-width: 500px;
    }

    .heart-pulse-container {
        position: relative;
        width: 60px;
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .heart-pulse-icon {
        font-size: 2.5rem;
        z-index: 2;
        animation: heartPump 1.2s infinite ease-in-out;
        filter: drop-shadow(0 0 15px rgba(0, 230, 118, 0.6));
    }

    .pulse-ring {
        position: absolute;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: rgba(0, 230, 118, 0.3);
        animation: pulseRipple 1.8s infinite cubic-bezier(0.215, 0.61, 0.355, 1);
        z-index: 1;
    }

    .pulse-ring-delay {
        animation-delay: 0.6s;
    }

    @keyframes heartPump {
        0% { transform: scale(1); }
        14% { transform: scale(1.2); }
        28% { transform: scale(1); }
        42% { transform: scale(1.15); }
        70% { transform: scale(1); }
        100% { transform: scale(1); }
    }

    @keyframes pulseRipple {
        0% { transform: scale(0.8); opacity: 0.8; }
        80%, 100% { transform: scale(2.2); opacity: 0; }
    }

    .animation-text-main {
        font-weight: 700;
        color: #ffffff;
        font-size: 1rem;
    }

    .animation-text-sub {
        font-size: 0.85rem;
        color: #00e676;
        font-weight: 500;
    }

    /* Feature Checkmarks */
    .feature-list {
        display: flex;
        gap: 1.8rem;
        margin-bottom: 2rem;
    }

    .feature-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
        color: #cbd5e1;
        font-weight: 500;
    }

    .check-icon {
        color: #00e676;
        font-weight: 800;
    }

    /* Right Column - SaaS Dashboard Card */
    .dashboard-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 230, 118, 0.25);
        border-radius: 24px;
        padding: 2.2rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 
                    0 0 30px rgba(0, 230, 118, 0.1);
    }

    .card-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
    }

    .status-pill {
        background: rgba(0, 230, 118, 0.12);
        color: #00e676;
        border: 1px solid rgba(0, 230, 118, 0.3);
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* White & Green Input Control Boxes */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #00e676 !important;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.3) !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }

    .stNumberInput label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Refined Compact Button Styling - Synchronized & Theme Aligned */
    div[data-testid="stButton"] > button,
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"],
    div.stButton > button {
        height: 44px !important;
        min-height: 44px !important;
        max-height: 44px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.25s ease-in-out !important;
        margin-top: 0.6rem !important;
        box-sizing: border-box !important;
    }

    /* Primary Action Button: Run Clinical Analysis (Vibrant Neon Mint Gradient) */
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

    /* Secondary Action Button: View Assessment Report (Active State - Cloned Mint Gradient) */
    div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stButton"] > button:not([disabled]),
    div[data-testid="stColumn"]:last-child div[data-testid="stButton"] > button:not([disabled]) {
        background: linear-gradient(135deg, #00e676 0%, #00b0ff 100%) !important;
        color: #061510 !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.4) !important;
        cursor: pointer !important;
    }

    div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stButton"] > button:not([disabled]):hover,
    div[data-testid="stColumn"]:last-child div[data-testid="stButton"] > button:not([disabled]):hover {
        background: linear-gradient(135deg, #00f080 0%, #00e5ff 100%) !important;
        box-shadow: 0 8px 25px rgba(0, 230, 118, 0.6) !important;
        transform: translateY(-1px) !important;
    }

    /* Secondary Action Button: View Assessment Report (Disabled / Initial State) */
    div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stButton"] > button[disabled],
    div[data-testid="stColumn"]:last-child div[data-testid="stButton"] > button[disabled] {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #64748b !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        opacity: 0.65 !important;
    }

    /* Result Metric Display Card (White & Dark Glass) */
    .result-box {
        background: #ffffff;
        color: #0f172a;
        border-radius: 18px;
        padding: 1.8rem;
        margin-top: 1.5rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        border: 2px solid #00e676;
    }

    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 0.8rem;
    }

    .result-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #059669;
    }

    .result-tag {
        background: #ecfdf5;
        color: #047857;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        border: 1px solid #a7f3d0;
    }

    .result-body {
        font-size: 1.02rem;
        line-height: 1.65;
        color: #334155;
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

# Load environment keys
load_dotenv()

# Split Hero & Dashboard Layout
col_left, col_right = st.columns([1.15, 1], gap="large")

with col_left:
    st.markdown("""
    <div class="hero-pill">⚡ AI-Powered Clinical Decision System</div>
    <div class="hero-title">
        Accurate Heart Risk Analysis with <span class="hero-highlight">Agentic AI</span>
    </div>
    <div class="hero-description">
        Advanced AI-powered cardiovascular intelligence designed to assist clinical decision-making. Our system evaluates key patient vitals against verified medical guidelines to deliver accurate, empathetic, and physician-grade heart health assessments.
    </div>
    """, unsafe_allow_html=True)

with col_right:
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        chol = st.number_input(
            "Total Cholesterol (mg/dL)",
            min_value=50.0,
            max_value=600.0,
            value=245.0,
            step=1.0,
            help="Normal is below 200 mg/dL. High risk is classified above 240 mg/dL."
        )
    with input_col2:
        thalach = st.number_input(
            "Max Heart Rate (bpm)",
            min_value=50.0,
            max_value=250.0,
            value=142.0,
            step=1.0,
            help="Expected range during exercise testing is 60 to 200 bpm."
        )
    
    # Action buttons arranged side-by-side
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        run_analysis = st.button("Run Clinical Analysis  →", key="run_analysis_btn")
        
    with btn_col2:
        reopen_analysis = st.button("📋 View Assessment Report", key="reopen_report_btn")
            
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
                    
                    # Execute Diagnostic prediction directly for instant visual gauge chart
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

    if reopen_analysis:
        if st.session_state.get("last_report") is not None:
            last = st.session_state["last_report"]
            show_report_modal(last["chol"], last["thalach"], last["diag_prediction"], last["report_output"])
        else:
            st.info("ℹ️ Please click **'Run Clinical Analysis  →'** first to generate your heart assessment report!")
