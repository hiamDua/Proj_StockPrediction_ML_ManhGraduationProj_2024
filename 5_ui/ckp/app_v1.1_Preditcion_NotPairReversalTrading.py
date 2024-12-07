import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from typing import Tuple, Optional

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

class StockPriceUI:
    def __init__(self):
        """Initialize the UI components"""
        self.predictor = StockPricePredictor(
            "D:/OneDrive - Hanoi University of Science and Technology/GIT/MiniProj_StockPrediction_ML_SpManhGraduationProj_2024/2_code_notebooks_TrainingModel/pkl_save_model_results"
        )
        self.setup_page()

    def setup_page(self):
        """Setup the main page configuration"""
        st.title("Stock Price Prediction System")
        st.sidebar.header("Options")

    def create_input_form(self) -> Tuple[float, float, float, float]:
        """Create input form for stock data"""
        col1, col2 = st.columns(2)
        with col1:
            open_price = st.number_input("Opening Price (VND)", value=85000.0, step=1000.0)
            high_price = st.number_input("High Price (VND)", value=86000.0, step=1000.0)
        with col2:
            low_price = st.number_input("Low Price (VND)", value=84000.0, step=1000.0)
            volume = st.number_input("Trading Volume", value=1000000, step=100000)
        return open_price, high_price, low_price, volume

    def plot_price_visualization(self, values: list, title: str):
        """Create price visualization plot"""
        fig, ax = plt.subplots(figsize=(10, 6))
        prices = ['Low', 'Open', 'Predicted Close', 'High']
        colors = ['red' if v > values[1] else 'green' for v in values]
        
        bars = ax.bar(prices, values, color=colors, alpha=0.6)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:,.0f}',
                   ha='center', va='bottom')
        
        ax.set_ylabel("Price (VND)")
        ax.set_title(title)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)

    def display_analysis(self, open_price: float, prediction: float, price_range: float):
        """Display price analysis"""
        pred_vs_open = prediction - open_price
        
        st.write("### Analysis")
        st.write(f"Day's Trading Range: {price_range:,.2f} VND")
        st.write(f"Predicted Change from Open: {pred_vs_open:,.2f} VND ({(pred_vs_open/open_price)*100:.2f}%)")

    def run(self):
        """Run the main application"""
        # Model selection
        model_list = ["FPT", "CMG", "VGI", "VTL"]
        selected_model = st.sidebar.selectbox("Select Stock", model_list)

        # Load model
        if self.predictor.load_model(selected_model):
            st.success(f"Model {selected_model} loaded successfully!")

            # Get input values
            open_price, high_price, low_price, volume = self.create_input_form()

            # Make prediction
            if st.button("Predict Closing Price"):
                input_features = pd.DataFrame([[open_price, high_price, low_price, volume]], 
                                           columns=['open', 'high', 'low', 'volume'])
                
                prediction = self.predictor.predict(input_features)
                
                if prediction is not None:
                    # Display results
                    st.write("### Prediction Results")
                    st.write(f"**Predicted Closing Price:** {prediction:,.2f} VND")
                    
                    # Display analysis
                    self.display_analysis(open_price, prediction, high_price - low_price)
                    
                    # Create visualization
                    values = [low_price, open_price, prediction, high_price]
                    self.plot_price_visualization(values, f"{selected_model} Stock Price Analysis")

def main():
    app = StockPriceUI()
    app.run()

if __name__ == "__main__":
    main()