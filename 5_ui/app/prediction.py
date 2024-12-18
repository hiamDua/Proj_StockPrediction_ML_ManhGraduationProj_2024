import streamlit as st
import joblib
import pandas as pd
import os
from typing import Optional

class StockPricePredictor:
    def __init__(self, model_base_path: str):
        """Initialize the predictor with model path"""
        self.model_base_path = model_base_path
        self.model = None
        self.scaler_x = None
        self.scaler_y = None

    def load_model(self, stock_name: str) -> bool:
        """Load model and scalers for a given stock"""
        try:
            model_path = os.path.join(self.model_base_path, f"{stock_name}_ridge_model.pkl")
            scaler_x_path = os.path.join(self.model_base_path, f"{stock_name}_scaler_x.pkl")
            scaler_y_path = os.path.join(self.model_base_path, f"{stock_name}_scaler_y.pkl")

            self.model = joblib.load(model_path)
            self.scaler_x = joblib.load(scaler_x_path)
            self.scaler_y = joblib.load(scaler_y_path)
            return True
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return False

    def predict(self, input_data: pd.DataFrame) -> Optional[float]:
        """Make prediction using loaded model"""
        try:
            scaled_features = self.scaler_x.transform(input_data)
            prediction = self.model.predict(scaled_features)
            return self.scaler_y.inverse_transform(prediction.reshape(-1, 1))[0][0]
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            return None

