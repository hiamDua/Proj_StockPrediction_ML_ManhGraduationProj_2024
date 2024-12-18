import pandas as pd
import os

class StockDataLoader:
    def __init__(self):
        self.base_path = r"C:\Users\manhm\Downloads\MiniProj_StockPrediction_ML_SpManhGraduationProj_2024\data\raw20192024"
        self.data_cache = {}

    def load_historical_data(self, stock_code: str) -> pd.DataFrame:
        """Load historical data for a given stock"""
        if stock_code in self.data_cache:
            return self.data_cache[stock_code]

        file_path = os.path.join(self.base_path, f"{stock_code}_stock_data.csv")
        
        try:
            # Read and process data
            data = pd.read_csv(file_path)
            data['time'] = pd.to_datetime(data['time'])
            data.sort_values('time', inplace=True)
            
            # Cache the data
            self.data_cache[stock_code] = data
            
            return data
        except Exception as e:
            raise Exception(f"Error loading data for {stock_code}: {str(e)}")

    def get_recent_data(self, stock_code: str, days: int = 100) -> pd.DataFrame:
        """Get recent days of data for a stock"""
        data = self.load_historical_data(stock_code)
        return data.tail(days) 