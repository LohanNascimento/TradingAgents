# agents/risk_manager.py 
import random
from datetime import datetime
from core.base_agent import BaseAgent
from core.data_models import TradingDecision, MarketData, RiskAssessment

class RiskManager(BaseAgent):
    def __init__(self, llm, db):
        super().__init__("Gestor de Risco", llm, db)
        self.system_prompt = """
        Você é um gestor de risco experiente. Avalie riscos de portfólio incluindo:
        - Volatilidade e correlação
        - Liquidez e concentração
        - Exposição setorial
        - Risco de mercado e crédito
        """
    
    async def assess_risk(self, symbol: str, decision: TradingDecision, market_data: MarketData) -> RiskAssessment:
        prompt = f"""
        Avalie o risco da seguinte decisão de trading:
        
        Símbolo: {symbol}
        Ação: {decision.action.value}
        Quantidade: {decision.quantity}
        Preço: ${decision.price:.2f}
        
        Dados de mercado:
        - Volatilidade implícita: {market_data.change_percent:.2f}%
        - Volume: {market_data.volume:,}
        - Market Cap: ${market_data.market_cap/1e9:.2f}B
        
        Forneça avaliação de risco incluindo:
        1. Score de risco (0-100)
        2. Principais fatores de risco
        3. Recomendações de mitigação
        4. Aprovação/rejeição da operação
        """
        risk_analysis = await self.llm.generate_response(prompt, self.system_prompt)
        volatility = abs(market_data.change_percent) / 100
        liquidity_score = min(market_data.volume / 1000000, 10) / 10
        risk_score = (volatility * 50 + (1 - liquidity_score) * 30 + random.uniform(0, 20))
        assessment = RiskAssessment(
            symbol=symbol,
            risk_score=min(risk_score, 100),
            volatility=volatility,
            liquidity_score=liquidity_score,
            correlation_risk=random.uniform(0.1, 0.8),
            recommendation=risk_analysis,
            timestamp=datetime.now()
        )
        await self.db.save_risk_assessment(assessment)
        return assessment 