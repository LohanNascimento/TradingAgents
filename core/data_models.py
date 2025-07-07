# core/data_models.py 
from dataclasses import dataclass
from datetime import datetime
from typing import List
from .enums import DecisionType, RiskLevel

@dataclass
class MarketData:
    """Dados de mercado para um ativo."""
    symbol: str
    price: float
    volume: int
    change_percent: float
    market_cap: float
    pe_ratio: float
    timestamp: datetime

@dataclass
class SentimentData:
    """Dados de sentimento de mercado."""
    symbol: str
    sentiment_score: float  # -1 a 1
    confidence: float
    sources: List[str]
    timestamp: datetime

@dataclass
class NewsData:
    """Dados de notícias relevantes para o ativo."""
    title: str
    content: str
    source: str
    relevance_score: float
    timestamp: datetime

@dataclass
class TechnicalIndicators:
    """Indicadores técnicos calculados para o ativo."""
    symbol: str
    rsi: float
    macd: float
    moving_avg_20: float
    moving_avg_50: float
    bollinger_upper: float
    bollinger_lower: float
    volume_sma: float
    timestamp: datetime

@dataclass
class TradingDecision:
    """Decisão de trading tomada por um agente."""
    symbol: str
    action: DecisionType
    quantity: int
    price: float
    confidence: float
    reasoning: str
    risk_level: RiskLevel
    timestamp: datetime

@dataclass
class RiskAssessment:
    """Avaliação de risco de uma decisão de trading."""
    symbol: str
    risk_score: float  # 0-100
    volatility: float
    liquidity_score: float
    correlation_risk: float
    recommendation: str
    timestamp: datetime 