import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

class StockPricePredictor:
    def __init__(self, model_base_path: str):
        """Initialize the predictor with model path"""
        self.model_base_path = model_base_path
        self.models = {}

    def load_model(self, stock_name: str) -> bool:
        """Load model and scalers for a given stock"""
        try:
            model_path = os.path.join(self.model_base_path, f"{stock_name}_ridge_model.pkl")
            scaler_x_path = os.path.join(self.model_base_path, f"{stock_name}_scaler_x.pkl")
            scaler_y_path = os.path.join(self.model_base_path, f"{stock_name}_scaler_y.pkl")

            self.models[stock_name] = {
                "model": joblib.load(model_path),
                "scaler_x": joblib.load(scaler_x_path),
                "scaler_y": joblib.load(scaler_y_path),
            }
            return True
        except Exception as e:
            st.error(f"Error loading model for {stock_name}: {str(e)}")
            return False

    def predict(self, stock_name: str, input_data: pd.DataFrame) -> float:
        """Make prediction using loaded model"""
        try:
            model_info = self.models[stock_name]
            scaled_features = model_info["scaler_x"].transform(input_data)
            prediction = model_info["model"].predict(scaled_features)
            return model_info["scaler_y"].inverse_transform(prediction.reshape(-1, 1))[0][0]
        except Exception as e:
            st.error(f"Error making prediction for {stock_name}: {str(e)}")
            return None

class TradingStrategy:
    @staticmethod
    def calculate_spread(pred1: float, pred2: float) -> float:
        return pred1 - pred2

    @staticmethod
    def calculate_z_score(series: pd.Series, window: int = 30) -> pd.Series:
        rolling_mean = series.rolling(window).mean()
        rolling_std = series.rolling(window).std()
        z_score = (series - rolling_mean) / rolling_std
        return z_score

    @staticmethod
    def pair_trading_decision(spread: float, threshold: float) -> str:
        if spread > threshold:
            return "Short Spread: Sell Stock1, Buy Stock2"
        elif spread < -threshold:
            return "Long Spread: Buy Stock1, Sell Stock2"
        else:
            return "No Action"

    @staticmethod
    def reversal_trading_decision(z_score: float, upper: float, lower: float) -> str:
        if z_score > upper:
            return "Short Position: Expect Price to Drop"
        elif z_score < lower:
            return "Long Position: Expect Price to Rise"
        else:
            return "No Action"

class StockPriceUI:
    def __init__(self):
        """Initialize the UI components"""
        self.predictor = StockPricePredictor(
            "D:/OneDrive - Hanoi University of Science and Technology/GIT/MiniProj_StockPrediction_ML_SpManhGraduationProj_2024/2_code_notebooks_TrainingModel/pkl_save_model_results"
        )
        self.setup_page()

    def setup_page(self):
        """Setup the main page configuration"""
        st.title("Stock Price Prediction and Trading System")
        st.sidebar.header("Options")

    def create_input_form(self) -> pd.DataFrame:
        """Create input form for stock data"""
        open_price = st.number_input("Opening Price (VND)", value=85000.0, step=1000.0)
        high_price = st.number_input("High Price (VND)", value=86000.0, step=1000.0)
        low_price = st.number_input("Low Price (VND)", value=84000.0, step=1000.0)
        volume = st.number_input("Trading Volume", value=1000000, step=100000)

        return pd.DataFrame([[open_price, high_price, low_price, volume]],
                            columns=['open', 'high', 'low', 'volume'])

    def plot_visualization(self, series: pd.Series, title: str):
        """Create a visualization plot"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(series.index, series.values, label=title, color="blue")
        ax.axhline(y=2, color="red", linestyle="--", label="Upper Threshold")
        ax.axhline(y=-2, color="green", linestyle="--", label="Lower Threshold")
        ax.legend()
        st.pyplot(fig)

    def run(self):
        """Run the main application"""
        # Model selection
        model_list = ["FPT", "CMG", "VGI", "VTL"]
        strategy = st.sidebar.radio("Select Trading Strategy", ["Price Prediction", "Pair Trading", "Reversal Trading"])

        if strategy == "Price Prediction":
            selected_model = st.sidebar.selectbox("Select Stock", model_list)
            if self.predictor.load_model(selected_model):
                input_data = self.create_input_form()

                if st.button("Predict Closing Price"):
                    prediction = self.predictor.predict(selected_model, input_data)
                    if prediction is not None:
                        st.write(f"Predicted Closing Price: {prediction:,.2f} VND")

        elif strategy == "Pair Trading":
            stock1, stock2 = st.sidebar.selectbox("Stock 1", model_list), st.sidebar.selectbox("Stock 2", model_list)

            if self.predictor.load_model(stock1) and self.predictor.load_model(stock2):
                input_data = self.create_input_form()

                if st.button("Calculate Pair Trading Decision"):
                    pred1 = self.predictor.predict(stock1, input_data)
                    pred2 = self.predictor.predict(stock2, input_data)

                    if pred1 is not None and pred2 is not None:
                        spread = TradingStrategy.calculate_spread(pred1, pred2)
                        decision = TradingStrategy.pair_trading_decision(spread, threshold=2.0)

                        st.write(f"Spread: {spread:.2f}")
                        st.write(f"Decision: {decision}")

        elif strategy == "Reversal Trading":
            selected_model = st.sidebar.selectbox("Select Stock", model_list)

            if self.predictor.load_model(selected_model):
                historical_data = pd.Series(
                    np.random.randn(100),  # Simulate historical data
                    index=pd.date_range(start="2023-01-01", periods=100)
                )

                if st.button("Calculate Reversal Decision"):
                    z_scores = TradingStrategy.calculate_z_score(historical_data)
                    z_score = z_scores.iloc[-1]
                    decision = TradingStrategy.reversal_trading_decision(z_score, upper=2.0, lower=-2.0)

                    st.write(f"Current Z-score: {z_score:.2f}")
                    st.write(f"Decision: {decision}")
                    self.plot_visualization(z_scores, f"Z-score for {selected_model}")

def main():
    app = StockPriceUI()
    app.run()

if __name__ == "__main__":
    main()
