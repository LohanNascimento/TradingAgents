# config/settings.py 
# config/settings.py
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Dict, Any

@dataclass
class CacheConfig:
    """Configurações do sistema de cache"""
    market_data_ttl: timedelta = timedelta(minutes=5)
    technical_indicators_ttl: timedelta = timedelta(minutes=10)
    max_cache_size: int = 1000
    cleanup_interval: timedelta = timedelta(minutes=30)

@dataclass
class MarketDataConfig:
    """Configurações para obtenção de dados de mercado"""
    yfinance_timeout: int = 10
    max_retries: int = 3
    retry_delay: float = 1.0
    historical_period: str = "6mo"
    historical_interval: str = "1d"

@dataclass
class TechnicalIndicatorsConfig:
    """Configurações para cálculo de indicadores técnicos"""
    rsi_period: int = 14
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    ma_short_period: int = 20
    ma_long_period: int = 50
    bollinger_period: int = 20
    bollinger_std: float = 2.0
    volume_sma_period: int = 20

@dataclass
class AppSettings:
    """Configurações gerais da aplicação"""
    cache: CacheConfig = field(default_factory=CacheConfig)
    market_data: MarketDataConfig = field(default_factory=MarketDataConfig)
    technical: TechnicalIndicatorsConfig = field(default_factory=TechnicalIndicatorsConfig)
    enable_fallback: bool = True
    enable_logging: bool = True

# Instância global das configurações
settings = AppSettings()