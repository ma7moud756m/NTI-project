import pickle
import joblib

def load_model(path):

    try:
        model = joblib.load(path)
        print("Loaded with joblib")
        return model

    except Exception as e:
        print("Joblib Error:", e)
        raise