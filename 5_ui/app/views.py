import streamlit as st
import pandas as pd
import numpy as np
from prediction import StockPricePredictor
from pair_trading_strategy import TradingStrategy, TradingVisualization, PairTradingAnalysis
from typing import List
from data_loader import StockDataLoader
from reversal_trading_strategy import ReversalTradingAnalysis

class StockPriceView:
    def __init__(self):
        self.predictor = StockPricePredictor(
            "D:/OneDrive - Hanoi University of Science and Technology/GIT/MiniProj_StockPrediction_ML_SpManhGraduationProj_2024/2_code_notebooks_TrainingModel/pkl_save_model_results"
        )
        self.pair_trading_strategy = TradingStrategy()
        self.visualization = TradingVisualization()
        self.data_loader = StockDataLoader()
        self.pair_analysis = PairTradingAnalysis()
        self.reversal_analysis = ReversalTradingAnalysis()

    def setup_page(self):
        st.title("Stock Price Prediction and Trading System")
        st.sidebar.header("Trading Options")
        
        strategy = st.sidebar.radio(
            "Select Trading Strategy",
            ["Price Prediction", "Pair Trading", "Reversal Trading"],
            help="""
            Price Prediction: Predict closing price
            Pair Trading: Trade the spread between two stocks
            Reversal Trading: Trade based on price reversals
            """
        )
        return strategy

    def run(self):
        strategy = self.setup_page()
        
        if strategy == "Price Prediction":
            self.run_price_prediction()
        elif strategy == "Pair Trading":
            self.run_pair_trading()
        elif strategy == "Reversal Trading":
            self.run_reversal_trading()

    def run_price_prediction(self):
        model_list = ["FPT", "CMG", "VGI", "VTL"]
        selected_model = st.sidebar.selectbox("Select Stock", model_list)

        if self.predictor.load_model(selected_model):
            st.success(f"Model {selected_model} loaded successfully!")
            input_data = self.pair_trading_strategy.create_input_form()

            if st.button("Predict Closing Price"):
                prediction = self.predictor.predict(input_data)
                if prediction is not None:
                    self.display_prediction_results(selected_model, input_data, prediction)

    def run_pair_trading(self):
        st.sidebar.subheader("Pair Trading Parameters")
        
        # Strategy selection
        strategy_params = {
            "Conservative": {
                "z_open_threshold": 2.0,
                "z_close_threshold": 0.0,
                "profit_target": float('inf'),
                "loss_limit": float('-inf'),
            },
            "Aggressive": {
                "z_open_threshold": 2.5,
                "z_close_threshold": 0.5,
                "profit_target": 5000000,
                "loss_limit": -3000000,
            }
        }
        
        selected_strategy = st.sidebar.selectbox(
            "Select Strategy",
            ["Conservative", "Aggressive"]
        )
        
        # Stock selection
        model_list = ["FPT", "CMG", "VGI", "VTL"]
        stock1 = st.sidebar.selectbox("Select Stock 1", model_list)
        stock2 = st.sidebar.selectbox("Select Stock 2", model_list, index=1)
        
        # Parameters
        window_size = st.sidebar.slider("Rolling Window (days)", 10, 50, 30)
        lookback_days = st.sidebar.slider("Analysis Period (days)", 30, 500, 100)
        
        if stock1 != stock2:
            if st.button("Analyze Pair Trading"):
                try:
                    # Load historical data
                    stock1_data = self.data_loader.get_recent_data(stock1, lookback_days)
                    stock2_data = self.data_loader.get_recent_data(stock2, lookback_days)
                    
                    # Set window size
                    self.pair_analysis.window_size = window_size
                    
                    # Calculate metrics
                    historical_data = self.pair_analysis.calculate_metrics(stock1_data, stock2_data)
                    current_z = historical_data['z_score'].iloc[-1]
                    
                    # Display analysis
                    self.pair_analysis.plot_pair_trading_analysis(
                        stock1, stock2, historical_data, 
                        current_z, strategy_params[selected_strategy]
                    )
                    
                except Exception as e:
                    st.error(f"Error analyzing pair trading: {str(e)}")
        else:
            st.warning("⚠ Please select different stocks for pair trading")

    def run_reversal_trading(self):
        """Chạy phân tích giao dịch đảo chiều"""
        st.sidebar.subheader("Tham Số Giao Dịch Đảo Chiều")
        
        # Giải thích chiến lược
        st.sidebar.info("""
        ℹ️ **Giao dịch đảo chiều là gì?**
        - Chiến lược tìm điểm đảo chiều của giá
        - Kết hợp nhiều chỉ báo kỹ thuật
        - Mục tiêu: Mua đáy, bán đỉnh
        """)
        
        # Chọn cổ phiếu
        stock_list = ["FPT", "CMG", "VGI", "VTL"]
        selected_stock = st.sidebar.selectbox("Chọn Cổ Phiếu", stock_list)
        
        # Chọn preset hoặc tùy ch�nh
        strategy_mode = st.sidebar.radio(
            "Chế độ cài đặt",
            ["Preset", "Tùy chỉnh"]
        )
        
        if strategy_mode == "Preset":
            selected_preset = st.sidebar.selectbox(
                "Chọn Chiến Lược",
                ["Conservative", "Aggressive"]
            )
            
            # Giải thích chi tiết v� mỗi preset
            if selected_preset == "Conservative":
                strategy_params = {
                    "z_threshold": 2.0,
                    "rsi_upper": 70,
                    "rsi_lower": 30,
                    "bb_period": 20
                }
                st.sidebar.info("""
                📊 **Chiến lược An toàn (Conservative):**
                
                Các ngưỡng giao dịch:
                - Z-score: ±2.0 (Độ lệch chuẩn cao)
                - RSI > 70: Vùng quá mua mạnh
                - RSI < 30: Vùng quá bán mạnh
                - BB 20 ngày: Độ bi�n động trung bình
                
                👉 *Phù hợp cho giao d�ch dài hạn, ít rủi ro*
                """)
            else:  # Aggressive
                strategy_params = {
                    "z_threshold": 1.5,
                    "rsi_upper": 65,
                    "rsi_lower": 35,
                    "bb_period": 20
                }
                st.sidebar.info("""
                📊 **Chiến lược Tích cực (Aggressive):**
                
                Các ngưỡng giao dịch:
                - Z-score: ±1.5 (Độ lệch chuẩn vừa phải)
                - RSI > 65: Vùng quá mua sớm
                - RSI < 35: Vùng quá bán sớm
                - BB 20 ngày: Độ bi�n động trung bình
                
                👉 *Phù hợp cho giao d�ch ngắn hạn, nhiều tín hiệu hơn*
                """)
        
        else:  # Tùy chỉnh
            st.sidebar.subheader("Tùy chỉnh tham số")
            
            # Giải thích các chỉ báo
            st.sidebar.info("""
            📈 **Hướng dẫn các chỉ báo:**
            
            1. **Z-score:**
            - Đo lường độ l�ch giá so với trung bình
            - Càng cao càng quá mua/bán
            - Thông thường: 1.5-2.5
            
            2. **RSI (Relative Strength Index):**
            - Đo lường động lượng tăng/giảm
            - >70: Quá mua | <30: Quá bán
            - Vùng trung tính: 30-70
            
            3. **Bollinger Bands (BB):**
            - Dải biến động c�a giá
            - Chu kỳ ngắn: Nhạy hơn
            - Chu kỳ dài: Ổn đ�nh hơn
            """)
            
            # Z-score
            z_threshold = st.sidebar.slider(
                "Ngưỡng Z-score (±)",
                1.0, 3.0, 2.0, 0.1,
                help="Độ lệch chuẩn để xác định điểm cực trị. Càng cao càng an toàn"
            )
            
            # RSI
            col1, col2 = st.sidebar.columns(2)
            with col1:
                rsi_upper = st.number_input(
                    "RSI Quá Mua",
                    50, 90, 70,
                    help="Ngưỡng RSI xác đ�nh vùng quá mua. Thường dùng 70-80"
                )
            with col2:
                rsi_lower = st.number_input(
                    "RSI Quá Bán",
                    10, 50, 30,
                    help="Ngưỡng RSI xác đ�nh vùng quá bán. Thường dùng 20-30"
                )
            
            # Bollinger Bands
            bb_period = st.sidebar.slider(
                "Chu kỳ Bollinger Bands",
                10, 50, 20,
                help="Số ngày để tính BB. 20 ngày là phổ biến nhất"
            )
            
            strategy_params = {
                "z_threshold": z_threshold,
                "rsi_upper": rsi_upper,
                "rsi_lower": rsi_lower,
                "bb_period": bb_period
            }
        
        # Tham số thời gian
        lookback_days = st.sidebar.slider(
            "Số Ngày Phân Tích", 
            30, 500, 100,
            help="Số ngày dữ liệu quá khứ để phân tích. Càng nhiều càng ổn định"
        )
        
        # Giải thích tổng quan về chiến lược
        st.sidebar.success("""
        🎯 **Cách đọc tín hiệu:**
        
        1. **Tín hiệu BÁN m�nh khi:**
        - Z-score > ngưỡng
        - RSI > vùng quá mua
        - Giá chạm/vượt BB trên
        
        2. **Tín hiệu MUA mạnh khi:**
        - Z-score < -ngưỡng
        - RSI < vùng quá bán
        - Giá chạm/vượt BB dưới
        
        3. **Độ tin cậy tín hiệu:**
        - Càng nhiều điều kiện thỏa mãn càng tốt
        - Khối lượng giao d�ch lớn
        - Nến đảo chiều rõ ràng
        """)
        
        # Buttons
        col1, col2 = st.sidebar.columns([2,1])
        with col1:
            analyze_button = st.button("Phân Tích�ảo Chiều", use_container_width=True)
        with col2:
            if st.button("🔄", help="Làm mới dữ liệu"):
                st.experimental_rerun()
        
        if analyze_button:
            try:
                # Load dữ liệu
                stock_data = self.data_loader.get_recent_data(
                    selected_stock, 
                    lookback_days
                )
                
                # Tính toán các chỉ báo
                analysis_data = self.reversal_analysis.calculate_metrics(stock_data)
                
                # Lấy dữ liệu hiện tại
                current_data = analysis_data.iloc[-1]
                
                # Hiển thị phân tích
                self.reversal_analysis.plot_reversal_analysis(
                    selected_stock,
                    analysis_data,
                    current_data,
                    strategy_params
                )
                
                # Hiển thị tham số đang sử dụng
                st.sidebar.write("### Tham Số Đang Dùng")
                st.sidebar.write(f"""
                - Z-score threshold: ±{strategy_params['z_threshold']}
                - RSI quá mua: {strategy_params['rsi_upper']}
                - RSI quá bán: {strategy_params['rsi_lower']}
                - Chu kỳ BB: {strategy_params['bb_period']} ngày
                - Số ngày phân tích: {lookback_days} ngày
                """)
                
            except Exception as e:
                st.error(f"Lỗi khi phân tích đảo chiều: {str(e)}")

    def display_prediction_results(self, selected_model: str, input_data: pd.DataFrame, prediction: float):
        st.write("### Prediction Results")
        st.write(f"**Predicted Closing Price:** {prediction:,.2f} VND")
        
        # Display analysis
        self.pair_trading_strategy.display_analysis(
            input_data['open'].values[0],
            prediction,
            input_data['high'].values[0] - input_data['low'].values[0]
        )
        
        # Create visualization
        values = [
            input_data['low'].values[0],
            input_data['open'].values[0],
            prediction,
            input_data['high'].values[0]
        ]
        self.visualization.plot_price_visualization(
            values,
            f"{selected_model} Stock Price Analysis"
        )