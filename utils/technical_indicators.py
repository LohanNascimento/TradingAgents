# utils/technical_indicators.py
import numpy as np
import pandas as pd
from typing import List, Tuple, Optional
from config.settings import settings

class TechnicalIndicatorCalculator:
    """Calculadora otimizada de indicadores técnicos"""
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: Optional[int] = None) -> float:
        """Calcula RSI (Relative Strength Index)"""
        period = period or settings.technical.rsi_period
        
        if len(prices) < period + 1:
            return 50.0
        
        # Converte para numpy para melhor performance
        prices_array = np.array(prices)
        deltas = np.diff(prices_array)
        
        # Separa ganhos e perdas
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        # Calcula médias móveis exponenciais
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return float(rsi)
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> float:
        """Calcula EMA (Exponential Moving Average)"""
        if len(prices) < period:
            return float(np.mean(prices))
        
        prices_array = np.array(prices)
        alpha = 2.0 / (period + 1)
        
        # Inicializa com SMA
        ema = np.mean(prices_array[:period])
        
        # Calcula EMA
        for price in prices_array[period:]:
            ema = alpha * price + (1 - alpha) * ema
        
        return float(ema)
    
    @staticmethod
    def calculate_macd(prices: List[float], 
                      fast: Optional[int] = None,
                      slow: Optional[int] = None,
                      signal: Optional[int] = None) -> Tuple[float, float, float]:
        """Calcula MACD (Moving Average Convergence Divergence)"""
        fast = fast or settings.technical.macd_fast
        slow = slow or settings.technical.macd_slow
        signal = signal or settings.technical.macd_signal
        
        if len(prices) < slow + signal:
            return 0.0, 0.0, 0.0
        
        # Calcula EMAs
        ema_fast = TechnicalIndicatorCalculator.calculate_ema(prices, fast)
        ema_slow = TechnicalIndicatorCalculator.calculate_ema(prices, slow)
        
        # MACD line
        macd_line = ema_fast - ema_slow
        
        # Para simplificar, retorna apenas a linha MACD
        # Em implementação completa, calcularia signal line e histogram
        return float(macd_line), 0.0, 0.0
    
    @staticmethod
    def calculate_bollinger_bands(prices: List[float], 
                                 period: Optional[int] = None,
                                 std_dev: Optional[float] = None) -> Tuple[float, float, float]:
        """Calcula Bollinger Bands"""
        period = period or settings.technical.bollinger_period
        std_dev = std_dev or settings.technical.bollinger_std
        
        if len(prices) < period:
            avg = float(np.mean(prices))
            return avg, avg, avg
        
        # Calcula SMA e desvio padrão
        recent_prices = prices[-period:]
        sma = float(np.mean(recent_prices))
        std = float(np.std(recent_prices))
        
        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)
        
        return upper_band, sma, lower_band
    
    @staticmethod
    def calculate_moving_averages(prices: List[float]) -> Tuple[float, float]:
        """Calcula médias móveis de 20 e 50 períodos"""
        ma20_period = settings.technical.ma_short_period
        ma50_period = settings.technical.ma_long_period
        
        ma20 = float(np.mean(prices[-ma20_period:])) if len(prices) >= ma20_period else float(np.mean(prices))
        ma50 = float(np.mean(prices[-ma50_period:])) if len(prices) >= ma50_period else float(np.mean(prices))
        
        return ma20, ma50
    
    @staticmethod
    def calculate_volume_sma(volumes: List[int], period: Optional[int] = None) -> float:
        """Calcula SMA do volume"""
        period = period or settings.technical.volume_sma_period
        
        if len(volumes) < period:
            return float(np.mean(volumes))
        
        return float(np.mean(volumes[-period:]))
    
    @staticmethod
    def calculate_all_indicators(df: pd.DataFrame) -> dict:
        """Calcula todos os indicadores de uma vez para melhor performance"""
        if df.empty:
            return {}
        
        closes = df['Close'].tolist()
        volumes = df['Volume'].tolist()
        
        # Calcula todos os indicadores
        rsi = TechnicalIndicatorCalculator.calculate_rsi(closes)
        macd_line, _, _ = TechnicalIndicatorCalculator.calculate_macd(closes)
        ma20, ma50 = TechnicalIndicatorCalculator.calculate_moving_averages(closes)
        bollinger_upper, bollinger_middle, bollinger_lower = TechnicalIndicatorCalculator.calculate_bollinger_bands(closes)
        volume_sma = TechnicalIndicatorCalculator.calculate_volume_sma(volumes)
        
        return {
            'rsi': rsi,
            'macd': macd_line,
            'moving_avg_20': ma20,
            'moving_avg_50': ma50,
            'bollinger_upper': bollinger_upper,
            'bollinger_lower': bollinger_lower,
            'volume_sma': volume_sma
        }