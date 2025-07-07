# agents/trading_agent.py 
import random
from datetime import datetime
from core.base_agent import BaseAgent
from core.enums import DecisionType, RiskLevel
from core.data_models import TradingDecision

class TradingAgent(BaseAgent):
    def __init__(self, llm, db):
        super().__init__("Agente de Negociação", llm, db)
        self.system_prompt = """
        Você é um trader experiente responsável por tomar decisões finais de negociação.
        Considere todas as análises e pesquisas para tomar decisões informadas sobre:
        - Timing de entrada e saída
        - Tamanho da posição
        - Gestão de risco
        - Execução de ordens
        """
    
    async def make_trading_decision(self, symbol: str, all_analyses):
        analysis_summary = "\n".join([
            f"{a['agent']}: Recomendação {a.get('recommendation', 'N/A').value if hasattr(a.get('recommendation'), 'value') else a.get('recommendation', 'N/A')}, "
            f"Confiança: {a.get('confidence', 0):.1f}%"
            for a in all_analyses
        ])
        prompt = f"""
        Tome uma decisão de trading para {symbol} baseada nas seguintes análises:
        
        {analysis_summary}
        
        Forneça sua decisão final incluindo:
        1. Ação (comprar/vender/manter)
        2. Quantidade sugerida
        3. Preço alvo
        4. Justificativa da decisão
        5. Nível de confiança
        """
        decision_analysis = await self.llm.generate_response(prompt, self.system_prompt)
        buy_weight = sum(a.get('confidence', 0) for a in all_analyses 
                        if a.get('recommendation') == DecisionType.BUY)
        sell_weight = sum(a.get('confidence', 0) for a in all_analyses 
                         if a.get('recommendation') == DecisionType.SELL)
        hold_weight = sum(a.get('confidence', 0) for a in all_analyses 
                         if a.get('recommendation') == DecisionType.HOLD)
        if buy_weight > sell_weight and buy_weight > hold_weight:
            final_action = DecisionType.BUY
        elif sell_weight > buy_weight and sell_weight > hold_weight:
            final_action = DecisionType.SELL
        else:
            final_action = DecisionType.HOLD
        avg_confidence = sum(a.get('confidence', 0) for a in all_analyses) / len(all_analyses)
        decision = TradingDecision(
            symbol=symbol,
            action=final_action,
            quantity=random.randint(100, 1000),
            price=random.uniform(45, 55),
            confidence=avg_confidence,
            reasoning=decision_analysis,
            risk_level=RiskLevel.MEDIUM,
            timestamp=datetime.now()
        )
        self.db.save_decision(decision, "TradingAgent")
        return decision 