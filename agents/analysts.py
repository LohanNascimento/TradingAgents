# agents/analysts.py 
import random
from datetime import datetime
from core.base_agent import BaseAgent
from core.data_models import MarketData, TechnicalIndicators
from core.enums import DecisionType

class FundamentalAnalyst(BaseAgent):
    def __init__(self, llm, db):
        super().__init__("Analista Fundamentalista", llm, db)
        self.system_prompt = """
        Você é um analista fundamentalista experiente. Analise dados financeiros,
        métricas de desempenho e valor intrínseco das empresas. Foque em:
        - Análise de balanços patrimoniais
        - Fluxo de caixa e lucratividade
        - Posição competitiva
        - Crescimento sustentável
        """
    
    async def analyze(self, data):
        market_data = data.get('market_data')
        if not market_data:
            return {}
        
        prompt = f"""
        Analise os dados fundamentais da empresa {market_data.symbol}:
        
        Preço atual: ${market_data.price:.2f}
        Market Cap: ${market_data.market_cap/1e9:.2f}B
        P/E Ratio: {market_data.pe_ratio:.2f}
        Mudança %: {market_data.change_percent:.2f}%
        
        Forneça uma análise fundamentalista incluindo:
        1. Avaliação do valor intrínseco
        2. Principais riscos e oportunidades
        3. Recomendação (comprar/vender/manter)
        4. Confiança na análise (0-100%)
        """
        
        analysis = await self.llm.generate_response(prompt, self.system_prompt)
        confidence = random.uniform(60, 90)
        recommendation = random.choice([DecisionType.BUY, DecisionType.HOLD, DecisionType.SELL])
        result = {
            'agent': self.name,
            'analysis': analysis,
            'confidence': confidence,
            'recommendation': recommendation,
            'timestamp': datetime.now()
        }
        self.analysis_history.append(result)
        return result

class SentimentAnalyst(BaseAgent):
    def __init__(self, llm, db):
        super().__init__("Analista de Sentimentos", llm, db)
        self.system_prompt = """
        Você é um analista de sentimentos especializado em mercados financeiros.
        Analise sentimentos de mídias sociais, notícias e opinião pública sobre ativos.
        Foque em:
        - Sentiment scoring (-1 a 1)
        - Tendências de opinião
        - Influenciadores e formadores de opinião
        - Impacto no comportamento do mercado
        """
    
    async def analyze(self, data):
        market_data = data.get('market_data')
        news_data = data.get('news_data', [])
        sentiment_score = random.uniform(-0.8, 0.8)
        prompt = f"""
        Analise o sentimento do mercado para {market_data.symbol}:
        
        Sentiment Score: {sentiment_score:.2f} (-1 negativo, +1 positivo)
        Notícias recentes: {len(news_data)} artigos
        
        Forneça análise de sentimento incluindo:
        1. Interpretação do score de sentimento
        2. Tendências de opinião pública
        3. Impacto provável no preço
        4. Recomendação baseada em sentimento
        """
        analysis = await self.llm.generate_response(prompt, self.system_prompt)
        confidence = random.uniform(70, 95)
        recommendation = DecisionType.BUY if sentiment_score > 0.3 else DecisionType.SELL if sentiment_score < -0.3 else DecisionType.HOLD
        result = {
            'agent': self.name,
            'analysis': analysis,
            'sentiment_score': sentiment_score,
            'confidence': confidence,
            'recommendation': recommendation,
            'timestamp': datetime.now()
        }
        self.analysis_history.append(result)
        return result

class NewsAnalyst(BaseAgent):
    def __init__(self, llm, db):
        super().__init__("Analista de Notícias", llm, db)
        self.system_prompt = """
        Você é um analista de notícias especializado em impactos macroeconômicos.
        Analise notícias globais, indicadores econômicos e eventos geopolíticos.
        Foque em:
        - Impacto de políticas monetárias
        - Eventos geopolíticos
        - Indicadores econômicos
        - Tendências setoriais
        """
    
    async def analyze(self, data):
        market_data = data.get('market_data')
        news_impact = random.uniform(-0.5, 0.5)
        prompt = f"""
        Analise o impacto das notícias para {market_data.symbol}:
        
        Impacto das notícias: {news_impact:.2f}
        Contexto macroeconômico atual
        
        Forneça análise de notícias incluindo:
        1. Principais eventos que afetam o ativo
        2. Impacto macroeconômico
        3. Tendências setoriais
        4. Recomendação baseada em notícias
        """
        analysis = await self.llm.generate_response(prompt, self.system_prompt)
        confidence = random.uniform(65, 85)
        recommendation = DecisionType.BUY if news_impact > 0.2 else DecisionType.SELL if news_impact < -0.2 else DecisionType.HOLD
        result = {
            'agent': self.name,
            'analysis': analysis,
            'news_impact': news_impact,
            'confidence': confidence,
            'recommendation': recommendation,
            'timestamp': datetime.now()
        }
        self.analysis_history.append(result)
        return result

class TechnicalAnalyst(BaseAgent):
    def __init__(self, llm, db):
        super().__init__("Analista Técnico", llm, db)
        self.system_prompt = """
        Você é um analista técnico especializado em indicadores e padrões de preço.
        Analise indicadores técnicos, padrões gráficos e momentum.
        Foque em:
        - RSI, MACD, Bollinger Bands
        - Médias móveis e tendências
        - Padrões de candlestick
        - Suporte e resistência
        """
    
    async def analyze(self, data):
        market_data = data.get('market_data')
        technical_data = data.get('technical_data')
        if not technical_data:
            return {}
        prompt = f"""
        Analise os indicadores técnicos para {market_data.symbol}:
        
        RSI: {technical_data.rsi:.2f}
        MACD: {technical_data.macd:.2f}
        Média Móvel 20: ${technical_data.moving_avg_20:.2f}
        Média Móvel 50: ${technical_data.moving_avg_50:.2f}
        Bollinger Superior: ${technical_data.bollinger_upper:.2f}
        Bollinger Inferior: ${technical_data.bollinger_lower:.2f}
        
        Forneça análise técnica incluindo:
        1. Interpretação dos indicadores
        2. Sinais de compra/venda
        3. Níveis de suporte e resistência
        4. Recomendação técnica
        """
        analysis = await self.llm.generate_response(prompt, self.system_prompt)
        if technical_data.rsi < 30:
            recommendation = DecisionType.BUY
        elif technical_data.rsi > 70:
            recommendation = DecisionType.SELL
        else:
            recommendation = DecisionType.HOLD
        confidence = random.uniform(75, 95)
        result = {
            'agent': self.name,
            'analysis': analysis,
            'technical_signals': {
                'rsi_signal': 'oversold' if technical_data.rsi < 30 else 'overbought' if technical_data.rsi > 70 else 'neutral',
                'macd_signal': 'bullish' if technical_data.macd > 0 else 'bearish',
                'ma_signal': 'bullish' if technical_data.moving_avg_20 > technical_data.moving_avg_50 else 'bearish'
            },
            'confidence': confidence,
            'recommendation': recommendation,
            'timestamp': datetime.now()
        }
        self.analysis_history.append(result)
        return result 