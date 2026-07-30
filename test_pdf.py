from pdf_generator import generate_clinical_pdf

sample_report = """### 🏥 Executive Summary
Based on the patient's vitals (Total Cholesterol: 245.0 mg/dL, Max Heart Rate: 142.0 bpm), the AI system indicates a **HIGH RISK** profile for cardiovascular disease.

### 📊 Vitals & Diagnostic Analysis
- **Total Cholesterol**: 245.0 mg/dL (Elevated, >200 mg/dL threshold).
- **Maximum Heart Rate**: 142.0 bpm (Reduced exercise tolerance).

### 💡 Evidence-Based Lifestyle & Health Guidance
- Adopt a heart-healthy Mediterranean diet rich in soluble fiber.
- Engage in 150 minutes of moderate aerobic exercise per week.

### 🩺 Recommended Next Steps
- Schedule a follow-up consultation with a physician.
- Perform a lipid panel audit within 30 days.
"""

try:
    pdf_bytes = generate_clinical_pdf(chol=245.0, thalach=142.0, diag_prediction="HIGH RISK", report_text=sample_report)
    print(f"SUCCESS: Generated PDF report of length {len(pdf_bytes)} bytes.")
    with open("test_output.pdf", "wb") as f:
        f.write(pdf_bytes)
    print("PDF saved to test_output.pdf successfully!")
except Exception as e:
    print(f"ERROR: PDF generation failed: {e}")
