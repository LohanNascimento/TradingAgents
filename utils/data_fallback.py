# utils/data_fallback.py
import random
from datetime import datetime
from typing import Dict, Any
from core.data_models import MarketData, TechnicalIndicators

class FallbackDataGenerator:
    """Gerador de dados simulados para fallback"""
    
    def __init__(self):
        self._base_prices = {}
        self._price_trend = {}
    
    def generate_market_data(self, symbol: str) -> MarketData:
        """Gera dados de mercado simulados"""
        # Mantém consistência usando preço base
        if symbol not in self._base_prices:
            self._base_prices[symbol] = random.uniform(50, 500)
            self._price_trend[symbol] = random.uniform(-0.02, 0.02)
        
        # Simula movimento de preço com tendência
        base_price = self._base_prices[symbol]
        trend = self._price_trend[symbol]
        
        # Aplica tendência e volatilidade
        price_change = base_price * (trend + random.uniform(-0.05, 0.05))
        current_price = max(1.0, base_price + price_change)
        
        # Atualiza preço base para próxima iteração
        self._base_prices[symbol] = current_price
        
        # Calcula outros parâmetros
        previous_close = base_price
        change_percent = ((current_price - previous_close) / previous_close * 100)
        
        return MarketData(
            symbol=symbol,
            price=round(current_price, 2),
            volume=random.randint(1000000, 10000000),
            change_percent=round(change_percent, 2),
            market_cap=random.uniform(1e9, 1e12),
            pe_ratio=random.uniform(10, 30),
            timestamp=datetime.now()
        )
    
    def generate_technical_indicators(self, symbol: str) -> TechnicalIndicators:
        """Gera indicadores técnicos simulados"""
        # Obtém preço atual para indicadores consistentes
        current_price = self._base_prices.get(symbol, random.uniform(50, 500))
        
        # Gera indicadores com base no preço atual
        ma20 = current_price * random.uniform(0.98, 1.02)
        ma50 = current_price * random.uniform(0.95, 1.05)
        
        # Bollinger Bands baseadas na MA20
        volatility = current_price * 0.02
        bollinger_upper = ma20 + (2 * volatility)
        bollinger_lower = ma20 - (2 * volatility)
        
        # RSI com distribuição mais realista
        rsi_base = 50
        if current_price > ma20:
            rsi_base += random.uniform(0, 20)
        else:
            rsi_base -= random.uniform(0, 20)
        
        rsi = max(0, min(100, rsi_base + random.uniform(-10, 10)))
        
        return TechnicalIndicators(
            symbol=symbol,
            rsi=round(rsi, 2),
            macd=round(random.uniform(-2, 2), 3),
            moving_avg_20=round(ma20, 2),
            moving_avg_50=round(ma50, 2),
            bollinger_upper=round(bollinger_upper, 2),
            bollinger_lower=round(bollinger_lower, 2),
            volume_sma=random.randint(500000, 2000000),
            timestamp=datetime.now()
        )
    
    def reset_symbol(self, symbol: str) -> None:
        """Reseta dados simulados para um símbolo"""
        self._base_prices.pop(symbol, None)
        self._price_trend.pop(symbol, None)
    
    def reset_all(self) -> None:
        """Reseta todos os dados simulados"""
        self._base_prices.clear()
        self._price_trend.clear()

# Instância global do gerador de fallback
fallback_generator = FallbackDataGenerator()