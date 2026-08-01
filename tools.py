import re
import io
import pypdf
import joblib
import pandas as pd
from crewai.tools import tool

@tool("Heart Disease Predictor")
def predict_heart_disease(chol: float, thalach: float) -> str:
    """
    Predicts the risk of heart disease based on cholesterol levels (chol) and maximum heart rate achieved (thalach).
    
    Parameters:
    - chol: Cholesterol level in mg/dl.
    - thalach: Maximum heart rate achieved.
    
    Returns:
    - A string representing the risk assessment ("High Risk" or "Low Risk") and the model's prediction details.
    """
    try:
        # Load the model using joblib
        model = joblib.load('heart_disease_optimized_model.pkl')
        
        # Create input DataFrame
        input_data = pd.DataFrame([[chol, thalach]], columns=['chol', 'thalach'])
        
        # Predict
        prediction = model.predict(input_data)[0]
        
        # Based on model evaluation, 0 is High Risk (unhealthy), 1 is Low Risk (healthy)
        if prediction == 0 or str(prediction) == '0' or str(prediction).lower() == 'high':
            return "High Risk"
        else:
            return "Low Risk"
    except Exception as e:
        return f"Error running prediction: {str(e)}"

def extract_text_from_file(uploaded_file) -> str:
    """Extracts text from an uploaded PDF or TXT file."""
    try:
        if uploaded_file.name.lower().endswith(".pdf"):
            reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        else:
            return uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return ""

def extract_vitals_from_text(text: str) -> dict:
    """
    Extracts Total Cholesterol and Max Heart Rate from unstructured lab report text using regex pattern matching.
    """
    results = {"chol": 245.0, "thalach": 142.0}
    
    if not text:
        return results
        
    # Search for cholesterol patterns: e.g., "Cholesterol: 260 mg/dL" or "Chol: 245"
    chol_match = re.search(r'(?:cholesterol|chol)\D*(\d{2,3}(?:\.\d+)?)', text, re.IGNORECASE)
    if chol_match:
        try:
            val = float(chol_match.group(1))
            if 50.0 <= val <= 600.0:
                results["chol"] = val
        except ValueError:
            pass

    # Search for max heart rate patterns: e.g., "Max Heart Rate: 135 bpm" or "Thalach: 140"
    hr_match = re.search(r'(?:max\s*heart\s*rate|thalach|heart\s*rate|hr)\D*(\d{2,3}(?:\.\d+)?)', text, re.IGNORECASE)
    if hr_match:
        try:
            val = float(hr_match.group(1))
            if 50.0 <= val <= 250.0:
                results["thalach"] = val
        except ValueError:
            pass

    return results
