import sys
sys.stdout.reconfigure(encoding='utf-8')

from crew_logic import run_clinical_analysis

print("="*50)
print("TESTING STRUCTURED CLINICAL REPORT GENERATION")
print("="*50)

chol = 245.0
thalach = 142.0

print(f"Running analysis for Cholesterol={chol} mg/dL, Max Heart Rate={thalach} bpm...")
try:
    report_output = run_clinical_analysis(chol=chol, thalach=thalach)
    print("\n--- GENERATED REPORT OUTPUT ---")
    print(report_output)
    print("="*50)
    print("SUCCESS: Clinical Report Generated Cleanly!")
except Exception as e:
    print(f"Report generation test failed: {e}")
