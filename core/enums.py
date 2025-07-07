# core/enums.py 
from enum import Enum

class DecisionType(Enum):
    """Tipo de decisão de trading."""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"

class RiskLevel(Enum):
    """Níveis de risco para decisões de trading."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high" 