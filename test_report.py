import sys
sys.stdout.reconfigure(encoding='utf-8')

from crew_logic import run_lab_analysis

print("="*60)
print("TESTING CLEARLAB AI 4-AGENT RAG WORKFLOW")
print("="*60)

sample_lab_text = """
CENTRAL DIAGNOSTIC LABORATORY - PATIENT LAB REPORT
Patient Name: Kamal Jayasinghe | Date: 2026-08-01

TEST PARAMETERS:
- Total Cholesterol: 245.0 mg/dL (Reference: < 200 mg/dL)
- Maximum Heart Rate: 142.0 bpm (Exercise Stress Test)
- Fasting Blood Glucose: 115.0 mg/dL (Reference: 70-99 mg/dL)
- Hemoglobin A1c: 6.1% (Reference: < 5.7%)
"""

print(f"Running 4-Agent Analysis for sample lab report...\n")
try:
    report_output = run_lab_analysis(lab_text=sample_lab_text)
    print("\n--- FINAL AUDITED PATIENT GUIDANCE REPORT ---")
    print(report_output)
    print("="*60)
    print("SUCCESS: 4-Agent Execution Completed Cleanly!")
except Exception as e:
    print(f"4-Agent execution failed: {e}")
