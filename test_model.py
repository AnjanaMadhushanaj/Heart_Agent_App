import joblib
import pandas as pd

def test_model_prediction():
    print("Testing ML model load and predict...")
    try:
        model = joblib.load('heart_disease_optimized_model.pkl')
        print("Model loaded successfully!")
        
        # Test case 1: Normal values
        test_data_low = pd.DataFrame([[180.0, 150.0]], columns=['chol', 'thalach'])
        pred_low = model.predict(test_data_low)[0]
        print(f"Test Low (chol=180, thalach=150) -> Raw Prediction: {pred_low}")
        
        # Test case 2: Abnormal/High-risk values
        test_data_high = pd.DataFrame([[300.0, 85.0]], columns=['chol', 'thalach'])
        pred_high = model.predict(test_data_high)[0]
        print(f"Test High (chol=300, thalach=85) -> Raw Prediction: {pred_high}")
        
        print("Model tests executed successfully.")
    except Exception as e:
        print(f"Model test failed: {e}")

if __name__ == "__main__":
    test_model_prediction()
