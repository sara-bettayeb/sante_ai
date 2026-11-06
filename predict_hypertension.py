import sys
import json
import warnings
warnings.filterwarnings("ignore")

import joblib
import pandas as pd

def predict():
    try:
        input_data = json.loads(sys.argv[1])
        model = joblib.load('model_joblib_hypertension.joblib')
        features = [
            'male', 'age', 'currentSmoker', 'cigsPerDay', 'BPMeds',
            'diabetes', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose'
        ]
        df = pd.DataFrame([input_data], columns=features)
        prediction = int(model.predict(df)[0])
        probability = float(model.predict_proba(df)[0][1]) if hasattr(model, 'predict_proba') else None
        
        result = {
            "prediction": prediction,
            "risk": "High Risk" if prediction == 1 else "Normal / Low Risk",
            "probability": round(probability * 100, 2) if probability is not None else None
        }
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == '__main__':
    predict()