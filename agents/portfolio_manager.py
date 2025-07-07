# agents/portfolio_manager.py 
from core.base_agent import BaseAgent
from core.data_models import TradingDecision, RiskAssessment

class PortfolioManager(BaseAgent):
    def __init__(self, llm, db):
        super().__init__("Gestor de Portfólio", llm, db)
        self.system_prompt = """
        Você é um gestor de portfólio sênior. Tome decisões finais sobre:
        - Aprovação/rejeição de trades
        - Alocação de capital
        - Diversificação de portfólio
        - Objetivos de retorno vs risco
        """
    
    async def approve_trade(self, decision: TradingDecision, risk_assessment: RiskAssessment):
        prompt = f"""
        Avalie para aprovação a seguinte decisão de trading:
        
        Decisão: {decision.action.value.upper()} {decision.quantity} {decision.symbol}
        Preço: ${decision.price:.2f}
        Confiança: {decision.confidence:.1f}%
        
        Avaliação de Risco:
        - Score de risco: {risk_assessment.risk_score:.1f}/100
        - Volatilidade: {risk_assessment.volatility:.2f}
        - Liquidez: {risk_assessment.liquidity_score:.2f}
        
        Decisão: APROVAR ou REJEITAR
        Justificativa: [sua justificativa]
        """
        approval_analysis = await self.llm.generate_response(prompt, self.system_prompt)
        approve = (risk_assessment.risk_score < 70 and 
                  decision.confidence > 60 and 
                  risk_assessment.liquidity_score > 0.3)
        return approve, approval_analysis 