import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple

class TradingStrategy:
    @staticmethod
    def create_input_form() -> pd.DataFrame:
        """Create input form for stock data"""
        col1, col2 = st.columns(2)
        with col1:
            open_price = st.number_input("Opening Price (VND)", value=85000.0, step=1000.0)
            high_price = st.number_input("High Price (VND)", value=86000.0, step=1000.0)
        with col2:
            low_price = st.number_input("Low Price (VND)", value=84000.0, step=1000.0)
            volume = st.number_input("Trading Volume", value=1000000, step=100000)
            
        return pd.DataFrame([[open_price, high_price, low_price, volume]], 
                          columns=['open', 'high', 'low', 'volume'])

    @staticmethod
    def calculate_spread(pred1: float, pred2: float) -> float:
        """Calculate spread between two stocks"""
        return pred1 - pred2

    @staticmethod
    def calculate_z_score(series: pd.Series, window: int = 30) -> pd.Series:
        """Calculate z-score for mean reversion"""
        rolling_mean = series.rolling(window=window).mean()
        rolling_std = series.rolling(window=window).std()
        return (series - rolling_mean) / rolling_std

    def pair_trading_decision(self, spread: float, threshold: float = 2.0) -> str:
        """Make pair trading decision based on spread"""
        if spread > threshold:
            return "Short Spread (Sell Stock1, Buy Stock2)"
        elif spread < -threshold:
            return "Long Spread (Buy Stock1, Sell Stock2)"
        return "No Action"

    def reversal_trading_decision(self, z_score: float, upper: float = 2.0, lower: float = -2.0) -> str:
        """Make reversal trading decision based on z-score"""
        if z_score > upper:
            return "Short Position (Price likely to fall)"
        elif z_score < lower:
            return "Long Position (Price likely to rise)"
        return "No Action"

    @staticmethod
    def display_analysis(open_price: float, prediction: float, price_range: float):
        """Display price analysis"""
        pred_vs_open = prediction - open_price
        
        st.write("### Analysis")
        st.write(f"Day's Trading Range: {price_range:,.2f} VND")
        st.write(f"Predicted Change from Open: {pred_vs_open:,.2f} VND ({(pred_vs_open/open_price)*100:.2f}%)")

class TradingVisualization:
    def plot_price_visualization(self, values: List[float], title: str):
        """Create price visualization plot"""
        fig, ax = plt.subplots(figsize=(10, 6))
        prices = ['Low', 'Open', 'Predicted Close', 'High']
        colors = ['red' if v > values[1] else 'green' for v in values]
        
        bars = ax.bar(prices, values, color=colors, alpha=0.6)
        
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

    def plot_pair_trading(self, stock1: str, stock2: str, pred1: float, pred2: float, spread: float):
        """Plot pair trading analysis"""
        # Create two columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Price Predictions
            st.write("### Price Predictions")
            st.metric(
                label=f"{stock1} Price",
                value=f"{pred1:,.2f} VND",
                delta=f"{pred1 - pred2:,.2f} VND vs {stock2}"
            )
            st.metric(
                label=f"{stock2} Price",
                value=f"{pred2:,.2f} VND"
            )
            
            # Spread Analysis
            st.write("### Spread Analysis")
            st.metric(
                label="Current Spread",
                value=f"{spread:,.2f}",
                delta="Above threshold" if abs(spread) > 2.0 else "Within normal range"
            )
        
        with col2:
            # Visualization
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
            
            # Price comparison bar chart
            bars = ax1.bar([stock1, stock2], [pred1, pred2])
            ax1.set_title("Price Comparison")
            ax1.set_ylabel("Price (VND)")
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:,.0f}',
                        ha='center', va='bottom')
            
            # Spread visualization
            ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
            ax2.axhline(y=2.0, color='red', linestyle='--', label='Upper Threshold')
            ax2.axhline(y=-2.0, color='green', linestyle='--', label='Lower Threshold')
            ax2.scatter(['Current'], [spread], color='blue', s=100, zorder=5)
            ax2.set_title("Spread Analysis")
            ax2.set_ylabel("Spread Value")
            ax2.legend()
            
            plt.tight_layout()
            st.pyplot(fig)

        # Trading Recommendation
        st.write("### Trading Recommendation")
        if abs(spread) > 2.0:
            if spread > 2.0:
                st.error(f"💹 Short Spread: Sell {stock1}, Buy {stock2}")
            else:
                st.success(f"💰 Long Spread: Buy {stock1}, Sell {stock2}")
        else:
            st.info("⏸️ No Action Recommended")
            
        # Additional Analysis
        st.write("### Statistical Analysis")
        st.write(f"""
        - **Price Difference:** {abs(pred1 - pred2):,.2f} VND
        - **Percentage Difference:** {abs((pred1 - pred2)/pred1)*100:.2f}%
        - **Correlation Status:** {'High' if abs(spread) < 1.0 else 'Moderate' if abs(spread) < 2.0 else 'Low'}
        """)

    def plot_reversal_analysis(self, prices: pd.Series, z_scores: pd.Series):
        """Plot reversal trading analysis"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        
        # Price history
        ax1.plot(prices.index, prices.values, label='Price')
        ax1.set_title("Price History")
        ax1.set_ylabel("Price (VND)")
        ax1.legend()
        
        # Z-score analysis
        ax2.plot(z_scores.index, z_scores.values, label='Z-score')
        ax2.axhline(y=2.0, color='r', linestyle='--', label='Upper Threshold')
        ax2.axhline(y=-2.0, color='r', linestyle='--', label='Lower Threshold')
        ax2.set_title("Z-score Analysis")
        ax2.legend()
        
        plt.tight_layout()
        st.pyplot(fig)

class PairTradingAnalysis:
    def __init__(self):
        self.window_size = 30  # Default rolling window size

    def calculate_metrics(self, stock1_data: pd.DataFrame, stock2_data: pd.DataFrame) -> pd.DataFrame:
        """Calculate spread and z-score for pair trading"""
        # Use only required columns
        data = pd.merge(
            stock1_data[['time', 'close']].rename(columns={'close': 'close_1'}),
            stock2_data[['time', 'close']].rename(columns={'close': 'close_2'}),
            on='time'
        )
        data.set_index('time', inplace=True)
        
        # Calculate metrics
        data['spread'] = data['close_1'] - data['close_2']
        data['mean_spread'] = data['spread'].rolling(window=self.window_size).mean()
        data['std_spread'] = data['spread'].rolling(window=self.window_size).std()
        data['z_score'] = (data['spread'] - data['mean_spread']) / data['std_spread']
        
        return data.dropna()  # Remove NaN values

    def get_trading_signals(self, z_score: float, params: dict) -> tuple:
        """Generate trading signals based on z-score"""
        if z_score > params['z_open_threshold']:
            return "Short Spread", "inverse"
        elif z_score < -params['z_open_threshold']:
            return "Long Spread", "normal"
        return "No Action", "off"

    def plot_pair_trading_analysis(self, stock1: str, stock2: str, historical_data: pd.DataFrame, 
                                 current_z: float, params: dict):
        """Create comprehensive pair trading visualization"""
        # Create two columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### Phân Tích Lịch Sử")
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            
            # Plot spread
            ax1.plot(historical_data.index, historical_data['spread'], label='Chênh lệch giá')
            ax1.plot(historical_data.index, historical_data['mean_spread'], 
                    label='Trung bình', linestyle='--')
            ax1.fill_between(historical_data.index, 
                           historical_data['mean_spread'] - 2*historical_data['std_spread'],
                           historical_data['mean_spread'] + 2*historical_data['std_spread'],
                           alpha=0.2, label='Dải dao động 2σ')
            ax1.set_title(f"Chênh lệch giá giữa {stock1} và {stock2}")
            ax1.legend()
            
            # Plot z-score
            ax2.plot(historical_data.index, historical_data['z_score'], label='Chỉ số Z')
            ax2.axhline(y=params['z_open_threshold'], color='r', linestyle='--', 
                       label='Ngưỡng mở lệnh')
            ax2.axhline(y=-params['z_open_threshold'], color='r', linestyle='--')
            ax2.axhline(y=params['z_close_threshold'], color='g', linestyle=':', 
                       label='Ngưỡng đóng lệnh')
            ax2.axhline(y=-params['z_close_threshold'], color='g', linestyle=':')
            ax2.set_title("Diễn biến chỉ số Z")
            ax2.legend()
            
            plt.tight_layout()
            st.pyplot(fig)

            # Chú thích đặt ngay dưới biểu đồ
            col_explain1, col_explain2 = st.columns(2)
            
            with col_explain1:
                st.info("""
                📊 **Biểu đồ trên (Spread):**
                - **Đường xanh**: Chênh lệch giá hiện tại
                - **Đường cam**: Mức chênh lệch trung bình
                - **Vùng xanh nhạt**: Dải dao động bình thường (2σ)
                """)
            
            with col_explain2:
                st.info("""
                📈 **Biểu đồ dưới (Z-score):**
                - **Đường xanh**: Ch� số Z hiện tại
                - **Đường đỏ đứt**: Ngưỡng mở lệnh (±2σ)
                - **Đường xanh chấm**: Ngưỡng đóng lệnh
                """)
        
        with col2:
            st.write("### Trạng Thái Hiện Tại")
            signal, delta_color = self.get_trading_signals(current_z, params)
            
            # Chuyển đổi tín hi�u sang tiếng Việt
            signal_vn = {
                "Short Spread": "Bán Spread",
                "Long Spread": "Mua Spread",
                "No Action": "Giữ Nguyên"
            }
            
            # Display metrics
            st.metric(
                label="Chỉ số Z hiện t�i",
                value=f"{current_z:.2f}",
                delta=signal_vn[signal],
                delta_color=delta_color
            )
            
            # Trading recommendation
            st.write("### Tín Hiệu Giao Dịch")
            if signal == "Short Spread":
                st.error(f"🔻 Bán {stock1}, Mua {stock2}")
            elif signal == "Long Spread":
                st.success(f"🔺 Mua {stock1}, Bán {stock2}")
            else:
                st.info("⏸️ Giữ Nguyên Vị Thế")
            
            # Strategy Parameters
            st.write("### Thông Số Chiến Lược")
            st.write(f"""
            - Ngưỡng mở lệnh: ±{params['z_open_threshold']}σ
            - Ngưỡng đóng lệnh: ±{params['z_close_threshold']}σ
            - Mục tiêu lợi nhu�n: {params['profit_target']:,.0f} VNĐ
            - Cắt lỗ: {params['loss_limit']:,.0f} VNĐ
            """)
            
            # Performance Metrics
            if len(historical_data) > 0:
                st.write("### Chỉ Số Hiệu Suất")
                st.write(f"""
                - Độ biến động Spread: {historical_data['spread'].std():,.2f}
                - Tốc độ hồi mean: {1/historical_data['z_score'].autocorr():,.2f} ngày
                - Spread hiện tại: {historical_data['spread'].iloc[-1]:,.2f}
                """)