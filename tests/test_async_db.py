import pytest
import asyncio
from data.database import AsyncDatabaseManager
from core.data_models import TradingDecision, RiskAssessment
from core.enums import DecisionType, RiskLevel
from datetime import datetime
import os

@pytest.mark.asyncio
async def test_async_database_manager(tmp_path):
    db_path = tmp_path / "test_trading_agents.db"
    db = AsyncDatabaseManager(str(db_path))
    await db.connect()

    # Testa inserção de decisão
    decision = TradingDecision(
        symbol="TEST",
        action=DecisionType.BUY,
        quantity=10,
        price=100.0,
        confidence=95.0,
        reasoning="Teste de decisão",
        risk_level=RiskLevel.LOW,
        timestamp=datetime.now()
    )
    await db.save_decision(decision, "TestAgent")

    # Testa inserção de avaliação de risco
    assessment = RiskAssessment(
        symbol="TEST",
        risk_score=10.0,
        volatility=0.1,
        liquidity_score=0.9,
        correlation_risk=0.2,
        recommendation="Baixo risco",
        timestamp=datetime.now()
    )
    await db.save_risk_assessment(assessment)

    # Testa inserção de discussão
    await db.save_discussion("sessao1", "AgenteTeste", "Mensagem de teste")

    await db.close()
    # Se chegou até aqui sem exceção, passou no teste 