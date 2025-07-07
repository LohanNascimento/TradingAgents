# agents/researchers.py 
import random
from datetime import datetime
from core.base_agent import BaseAgent
from core.enums import DecisionType

class Researcher(BaseAgent):
    def __init__(self, name: str, bias: str, llm, db):
        super().__init__(name, llm, db)
        self.bias = bias  # 'bullish' or 'bearish'
        self.system_prompt = f"""
        Você é um pesquisador {bias} experiente. Avalie criticamente as análises apresentadas
        com uma perspectiva {bias}. Questione premissas, identifique riscos ou oportunidades
        que podem ter sido negligenciados.
        """
    
    async def research_analysis(self, analyses):
        analysis_summary = "\n".join([
            f"{a['agent']}: {a.get('analysis', 'N/A')}" for a in analyses
        ])
        prompt = f"""
        Avalie criticamente as seguintes análises com uma perspectiva {self.bias}:
        
        {analysis_summary}
        
        Como pesquisador {self.bias}, forneça:
        1. Pontos fortes e fracos das análises
        2. Riscos ou oportunidades negligenciados
        3. Questionamentos sobre premissas
        4. Sua recomendação final
        """
        research = await self.llm.generate_response(prompt, self.system_prompt)
        confidence = random.uniform(60, 85)
        if self.bias == 'bullish':
            recommendation = DecisionType.BUY if random.random() > 0.3 else DecisionType.HOLD
        else:
            recommendation = DecisionType.SELL if random.random() > 0.3 else DecisionType.HOLD
        result = {
            'agent': self.name,
            'research': research,
            'bias': self.bias,
            'confidence': confidence,
            'recommendation': recommendation,
            'timestamp': datetime.now()
        }
        return result 