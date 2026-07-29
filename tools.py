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
