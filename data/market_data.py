# data/market_data.py 
import random
from datetime import datetime, timedelta
from core.data_models import MarketData, TechnicalIndicators

class MarketDataProvider:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)
    
    def get_market_data(self, symbol: str) -> MarketData:
        # Simula dados de mercado (em produção, use APIs reais)
        if symbol in self.cache:
            cached_data, cached_time = self.cache[symbol]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data
        
        # Simula dados de mercado
        price = random.uniform(50, 500)
        volume = random.randint(1000000, 10000000)
        change_percent = random.uniform(-5, 5)
        market_cap = random.uniform(1e9, 1e12)
        pe_ratio = random.uniform(10, 30)
        
        data = MarketData(
            symbol=symbol,
            price=price,
            volume=volume,
            change_percent=change_percent,
            market_cap=market_cap,
            pe_ratio=pe_ratio,
            timestamp=datetime.now()
        )
        
        self.cache[symbol] = (data, datetime.now())
        return data
    
    def get_technical_indicators(self, symbol: str) -> TechnicalIndicators:
        # Simula indicadores técnicos
        return TechnicalIndicators(
            symbol=symbol,
            rsi=random.uniform(20, 80),
            macd=random.uniform(-2, 2),
            moving_avg_20=random.uniform(45, 55),
            moving_avg_50=random.uniform(40, 60),
            bollinger_upper=random.uniform(55, 65),
            bollinger_lower=random.uniform(35, 45),
            volume_sma=random.randint(500000, 2000000),
            timestamp=datetime.now()
        ) 