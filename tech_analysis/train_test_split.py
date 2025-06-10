import yfinance as yf


class TrainTestSets:

    def __init__(self):
        pass

    def train_test_split(self, ticker, interval):

        if interval in ["1m", "5m", "15m", "30m"]:
            start = "2025-05-31"
            end = "2025-06-06"
        elif interval in ["1h", "90m", "4h"]:
            start = "2025-04-28"
            end = "2025-06-06"
        elif interval in ["1d", "5d", "1wk"]:
            start = "2024-01-01"
            end = "2025-06-06"
        elif interval in ["1mo", "3mo"]:
            start = "2023-01-01"
            end = "2025-06-06"
            
        data = yf.download(tickers=ticker, start=start, end=end, interval=interval)
        data.columns = data.columns.droplevel(1)
        # Calculamos el punto de corte
        split_idx = int(len(data)*0.70)
        # Particiones respetando la secuencia temporal
        train = data.iloc[:split_idx]
        test = data.iloc[split_idx:]
        return (train, test)
    
    def interval_train_test_split(self, ticker, intervals):
        all_data = {}
        intervals = ["1m", "5m", "15m", "30m", "1h", "90m", "4h", "1d", "5d", "1wk", "1mo", "3mo"]
        #           ["1m", "5m", "15m", "30m", "1h", "90m", "4h", "1d", "5d", "1wk", "1mo", "3mo", "6mo"]
        for interval in intervals:
            data_from_split = self.train_test_split(ticker, interval)
            all_data[f"{interval}_train"] = data_from_split[0]
            all_data[f"{interval}_test"] = data_from_split[1]
        
        return all_data
