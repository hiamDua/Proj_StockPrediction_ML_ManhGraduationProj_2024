import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Tuple

class ReversalTradingAnalysis:
    def __init__(self):
        self.window_size = 20  # Mặc định cho MA và độ biến động

    def calculate_metrics(self, stock_data: pd.DataFrame) -> pd.DataFrame:
        """Tính toán các chỉ báo kỹ thuật cho giao dịch đảo chiều"""
        data = stock_data.copy()
        
        # Tính Moving Averages
        data['MA20'] = data['close'].rolling(window=20).mean()
        data['MA50'] = data['close'].rolling(window=50).mean()
        
        # Tính RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        
        # Tính Bollinger Bands
        data['BB_middle'] = data['close'].rolling(window=20).mean()
        std = data['close'].rolling(window=20).std()
        data['BB_upper'] = data['BB_middle'] + (std * 2)
        data['BB_lower'] = data['BB_middle'] - (std * 2)
        
        # Tính Z-score cho giá
        data['price_mean'] = data['close'].rolling(window=self.window_size).mean()
        data['price_std'] = data['close'].rolling(window=self.window_size).std()
        data['z_score'] = (data['close'] - data['price_mean']) / data['price_std']
        
        return data.dropna()

    def get_trading_signals(self, current_data: pd.Series, params: Dict) -> Tuple[str, str]:
        """Sinh tín hiệu giao dịch dựa trên các chỉ báo"""
        z_score = current_data['z_score']
        rsi = current_data['RSI']
        price = current_data['close']
        bb_upper = current_data['BB_upper']
        bb_lower = current_data['BB_lower']
        
        # Logic tín hiệu
        if z_score > params['z_threshold'] and rsi > 70:
            return "Bán", "inverse"  # Quá mua
        elif z_score < -params['z_threshold'] and rsi < 30:
            return "Mua", "normal"   # Quá bán
        elif price > bb_upper and rsi > 65:
            return "Cân Nhắc Bán", "inverse"
        elif price < bb_lower and rsi < 35:
            return "Cân Nhắc Mua", "normal"
        return "Giữ Nguyên", "off"

    def plot_reversal_analysis(self, stock_code: str, historical_data: pd.DataFrame, 
                             current_data: pd.Series, params: Dict):
        """Tạo biểu đồ phân tích đảo chiều"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### Phân Tích Kỹ Thuật")
            fig = plt.figure(figsize=(12, 8))
            
            # Subplot cho giá và BB
            ax1 = plt.subplot2grid((2, 1), (0, 0))
            ax1.plot(historical_data.index, historical_data['close'], label='Giá')
            ax1.plot(historical_data.index, historical_data['BB_middle'], 'g--', label='BB Mid')
            ax1.plot(historical_data.index, historical_data['BB_upper'], 'r--', label='BB Upper')
            ax1.plot(historical_data.index, historical_data['BB_lower'], 'r--', label='BB Lower')
            ax1.fill_between(historical_data.index, 
                           historical_data['BB_upper'],
                           historical_data['BB_lower'],
                           alpha=0.1)
            ax1.set_title(f"Biểu Đồ Giá {stock_code}")
            ax1.legend()
            
            # Subplot cho RSI
            ax2 = plt.subplot2grid((2, 1), (1, 0))
            ax2.plot(historical_data.index, historical_data['RSI'], label='RSI')
            ax2.axhline(y=70, color='r', linestyle='--')
            ax2.axhline(y=30, color='g', linestyle='--')
            ax2.fill_between(historical_data.index, 70, 30, alpha=0.1, color='gray')
            ax2.set_title("Chỉ Báo RSI")
            ax2.legend()
            
            plt.tight_layout()
            st.pyplot(fig)

            # Chú thích đặt ngay dưới biểu đồ
            col_explain1, col_explain2 = st.columns(2)
            
            with col_explain1:
                st.info("""
                📊 **Biểu đồ trên (Giá & Bollinger Bands):**
                - **Đường xanh đậm**: Giá hiện tại
                - **Đường xanh đứt**: Trung bình 20 ngày
                - **Đường đỏ đứt**: Dải Bollinger trên/dưới
                """)
                
            with col_explain2:
                st.info("""
                📈 **Biểu đồ dưới (RSI):**
                - **Vùng trên 70**: Vùng quá mua
                - **Vùng dưới 30**: Vùng quá bán
                - **Vùng 30-70**: Vùng trung tính
                """)
        
        with col2:
            st.write("### Trạng Thái Hiện Tại")
            signal, delta_color = self.get_trading_signals(current_data, params)
            
            # Hiển thị các chỉ số quan trọng
            st.metric(
                label="Giá Hiện Tại",
                value=f"{current_data['close']:,.0f} VNĐ",
                delta=f"{(current_data['close'] - current_data['MA20']):,.0f} vs MA20",
                delta_color=delta_color
            )
            
            st.metric(
                label="RSI",
                value=f"{current_data['RSI']:.1f}",
                delta="Quá mua" if current_data['RSI'] > 70 else "Quá bán" if current_data['RSI'] < 30 else "Trung tính"
            )
            
            # Tín hiệu giao dịch
            st.write("### Tín Hiệu Giao Dịch")
            if signal == "Bán":
                st.error(f"🔻 Tín hiệu bán mạnh")
            elif signal == "Mua":
                st.success(f"🔺 Tín hiệu mua mạnh")
            elif signal == "Cân Nhắc Bán":
                st.warning(f"⚠️ Cân nhắc chốt lời")
            elif signal == "Cân Nhắc Mua":
                st.warning(f"⚠️ Cân nhắc mua vào")
            else:
                st.info("⏸️ Giữ nguyên vị thế")
            
            # Thông số kỹ thuật
            st.write("### Thông Số Kỹ Thuật")
            st.write(f"""
            - BB Width: {((current_data['BB_upper'] - current_data['BB_lower'])/current_data['BB_middle']*100):.1f}%
            - Khoảng cách đến BB trên: {((current_data['BB_upper'] - current_data['close'])/current_data['close']*100):.1f}%
            - Khoảng cách đến BB dưới: {((current_data['close'] - current_data['BB_lower'])/current_data['close']*100):.1f}%
            - MA20: {current_data['MA20']:,.0f} VNĐ
            - MA50: {current_data['MA50']:,.0f} VNĐ
            """) 