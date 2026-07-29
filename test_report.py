import os
from dotenv import load_dotenv
from crew_logic import run_clinical_analysis

load_dotenv()

def test_clinical_report_generation():
    print("==================================================")
    print("TESTING STRUCTURED CLINICAL REPORT GENERATION")
    print("==================================================")
    
    # Patient test metrics: High Risk
    chol = 245.0
    thalach = 142.0
    
    print(f"Running analysis for Cholesterol={chol} mg/dL, Max Heart Rate={thalach} bpm...")
    try:
        report = run_clinical_analysis(chol=chol, thalach=thalach)
        print("\n--- GENERATED REPORT OUTPUT ---")
        print(report)
        print("-------------------------------")
        print("Test Report Generation Completed Successfully!")
    except Exception as e:
        print(f"Report generation test failed: {e}")

if __name__ == "__main__":
    test_clinical_report_generation()
