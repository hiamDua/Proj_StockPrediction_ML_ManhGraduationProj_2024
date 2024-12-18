import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Debug information ---
st.write("Current working directory:", os.getcwd())
model_dir = "D:/OneDrive - Hanoi University of Science and Technology/GIT/MiniProj_StockPrediction_ML_SpManhGraduationProj_2024/2_code_notebooks_TrainingModel/pkl_save_model_results"
st.write("Model directory exists:", os.path.exists(model_dir))

# --- Load model and scaler ---
def load_model_and_scaler(model_name):
    try:
        model_output_dir = "D:/OneDrive - Hanoi University of Science and Technology/GIT/MiniProj_StockPrediction_ML_SpManhGraduationProj_2024/2_code_notebooks_TrainingModel/pkl_save_model_results"
        
        # Debug information
        st.write("Attempting to load files from:", model_output_dir)
        
        model_path = os.path.join(model_output_dir, f"{model_name}_ridge_model.pkl")
        scaler_x_path = os.path.join(model_output_dir, f"{model_name}_scaler_x.pkl")
        scaler_y_path = os.path.join(model_output_dir, f"{model_name}_scaler_y.pkl")
        
        # Load files using joblib
        try:
            model = joblib.load(model_path)
            scaler_x = joblib.load(scaler_x_path)
            scaler_y = joblib.load(scaler_y_path)
            return model, scaler_x, scaler_y
        except Exception as e:
            st.error(f"Error loading files: {str(e)}")
            return None, None, None
            
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None, None, None

# --- Interface ---
st.title("Stock Price Prediction System")
st.sidebar.header("Options")

# Model selection
model_list = ["FPT", "CMG", "VGI", "VTL"]
selected_model = st.sidebar.selectbox("Select Stock", model_list)

# Load model
model, scaler_x, scaler_y = load_model_and_scaler(selected_model)

if model and scaler_x and scaler_y:
    st.success(f"Model {selected_model} loaded successfully!")

    # Input data
    st.header("Input Stock Data")
    col1, col2 = st.columns(2)
    with col1:
        open_price = st.number_input("Opening Price (VND)", value=85000.0, step=1000.0)
        high_price = st.number_input("High Price (VND)", value=86000.0, step=1000.0)
    with col2:
        low_price = st.number_input("Low Price (VND)", value=84000.0, step=1000.0)
        volume = st.number_input("Trading Volume", value=1000000, step=100000)

    # Normalize and predict
    if st.button("Predict Closing Price"):
        # Create input DataFrame with correct feature names
        input_features = pd.DataFrame([[open_price, high_price, low_price, volume]], 
                                    columns=['open', 'high', 'low', 'volume'])
        
        # Scale and predict
        scaled_features = scaler_x.transform(input_features)
        prediction = model.predict(scaled_features)
        real_prediction = scaler_y.inverse_transform(prediction.reshape(-1, 1))

        # Display results
        st.write("### Prediction Results")
        st.write(f"**Predicted Closing Price:** {real_prediction[0][0]:,.2f} VND")
        
        # Price range analysis
        price_range = high_price - low_price
        pred_vs_open = real_prediction[0][0] - open_price
        
        st.write("\n### Analysis")
        st.write(f"Day's Trading Range: {price_range:,.2f} VND")
        st.write(f"Predicted Change from Open: {pred_vs_open:,.2f} VND ({(pred_vs_open/open_price)*100:.2f}%)")

        # Prediction visualization
        st.header("Price Visualization")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot price range
        prices = ['Low', 'Open', 'Predicted Close', 'High']
        values = [low_price, open_price, real_prediction[0][0], high_price]
        colors = ['red' if v > open_price else 'green' for v in values]
        
        # Create bar plot
        bars = ax.bar(prices, values, color=colors, alpha=0.6)
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:,.0f}',
                    ha='center', va='bottom')
        
        ax.set_ylabel("Price (VND)")
        ax.set_title(f"{selected_model} Stock Price Analysis")
        
        # Format y-axis labels to show thousands with comma
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        st.pyplot(fig)
