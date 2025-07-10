# services/orchestrator.py 
import time
from datetime import datetime
from core.enums import DecisionType
from core.data_models import TradingDecision
from data.llm_interface import LLMInterface
from data.database import AsyncDatabaseManager
from data.market_data import market_data_provider
from services.exchange import SimulatedExchange
from agents.analysts import FundamentalAnalyst, SentimentAnalyst, NewsAnalyst, TechnicalAnalyst
from agents.researchers import Researcher
from agents.trading_agent import TradingAgent
from agents.risk_manager import RiskManager
from agents.portfolio_manager import PortfolioManager
import asyncio
from dataclasses import asdict
import logging
from utils.helpers import batcher

logger = logging.getLogger(__name__)

class TradingAgentsSystem:
    def __init__(self, model_name: str = "llama3.2"):
        self.llm = LLMInterface(model_name)
        self.db = AsyncDatabaseManager()
        self.market_data_provider = market_data_provider
        self.exchange = SimulatedExchange()
        self.fundamental_analyst = FundamentalAnalyst(self.llm, self.db)
        self.sentiment_analyst = SentimentAnalyst(self.llm, self.db)
        self.news_analyst = NewsAnalyst(self.llm, self.db)
        self.technical_analyst = TechnicalAnalyst(self.llm, self.db)
        self.bullish_researcher = Researcher("Pesquisador Otimista", "bullish", self.llm, self.db)
        self.bearish_researcher = Researcher("Pesquisador Pessimista", "bearish", self.llm, self.db)
        self.trading_agent = TradingAgent(self.llm, self.db)
        self.risk_manager = RiskManager(self.llm, self.db)
        self.portfolio_manager = PortfolioManager(self.llm, self.db)
        self.all_agents = [
            self.fundamental_analyst, self.sentiment_analyst, self.news_analyst,
            self.technical_analyst, self.bullish_researcher, self.bearish_researcher,
            self.trading_agent, self.risk_manager, self.portfolio_manager
        ]

    async def connect_db(self):
        await self.db.connect()

    async def close_db(self):
        await self.db.close()

    async def conduct_team_discussion(self, session_id: str, topic: str, context: str, rounds: int = 2):
        discussion_messages = []
        for round_num in range(rounds):
            logger.info(f"Rodada de discussão {round_num + 1}/{rounds}")
            round_messages = []
            for agent in self.all_agents:
                discussion_context = context
                if discussion_messages:
                    discussion_context += "\n\nDiscussão anterior:\n"
                    discussion_context += "\n".join(discussion_messages[-5:])
                message = await agent.participate_in_discussion(session_id, topic, discussion_context)
                formatted_message = f"{agent.name}: {message}"
                round_messages.append(formatted_message)
                discussion_messages.append(formatted_message)
                await asyncio.sleep(0.1)
            logger.info(f"Rodada {round_num + 1} concluída com {len(round_messages)} contribuições")
        return discussion_messages

    async def analyze_symbol(self, symbol: str):
        logger.info(f"Iniciando análise completa de {symbol}")
        market_data = self.market_data_provider.get_market_data(symbol)
        technical_data = self.market_data_provider.get_technical_indicators(symbol)
        data_package = {
            'market_data': market_data,
            'technical_data': technical_data,
            'news_data': [],
            'sentiment_data': None
        }
        analyses = await asyncio.gather(
            self.fundamental_analyst.analyze(data_package),
            self.sentiment_analyst.analyze(data_package),
            self.news_analyst.analyze(data_package),
            self.technical_analyst.analyze(data_package)
        )
        analyses = [a for a in analyses if a]
        research_results = await asyncio.gather(
            self.bullish_researcher.research_analysis(analyses),
            self.bearish_researcher.research_analysis(analyses)
        )
        session_id = f"session_{symbol}_{int(time.time())}"
        discussion_context = f"""
        Análise de {symbol}:
        Preço atual: ${market_data.price:.2f}
        Mudança: {market_data.change_percent:.2f}%
        Volume: {market_data.volume:,}
        Análises dos especialistas:
        {chr(10).join([f"- {a['agent']}: {a.get('recommendation', 'N/A')}" for a in analyses])}
        Pesquisa:
        - Otimista: {research_results[0].get('recommendation', 'N/A')}
        - Pessimista: {research_results[1].get('recommendation', 'N/A')}
        """
        discussion_messages = await self.conduct_team_discussion(
            session_id, f"Estratégia de trading para {symbol}", discussion_context
        )
        all_analyses = analyses + research_results
        trading_decision = await self.trading_agent.make_trading_decision(
            symbol, all_analyses, market_data
        )
        risk_assessment = await self.risk_manager.assess_risk(
            symbol, trading_decision, market_data
        )
        approval, approval_reasoning = await self.portfolio_manager.approve_trade(
            trading_decision, risk_assessment
        )
        executed_trade = None
        if approval:
            executed_trade = self.exchange.submit_order(trading_decision)
        return {
            'symbol': symbol,
            'market_data': asdict(market_data),
            'technical_data': asdict(technical_data),
            'analyses': analyses,
            'research': research_results,
            'discussion_messages': discussion_messages,
            'trading_decision': asdict(trading_decision),
            'risk_assessment': asdict(risk_assessment),
            'approval': approval,
            'approval_reasoning': approval_reasoning,
            'executed_trade': executed_trade,
            'timestamp': datetime.now()
        }

    async def run_trading_session(self, symbols: list, session_duration: int = 3600, max_parallel: int = 4, batch_size: int = 4):
        await self.connect_db()
        logger.info(f"Iniciando sessão de trading para {len(symbols)} símbolos")
        session_results = {
            'session_id': f"session_{int(time.time())}",
            'symbols': symbols,
            'start_time': datetime.now(),
            'results': {},
            'summary': {}
        }
        for batch in batcher(symbols, batch_size):
            sem = asyncio.Semaphore(max_parallel)
            async def analyze_with_limit(symbol):
                async with sem:
                    try:
                        result = await self.analyze_symbol(symbol)
                        session_results['results'][symbol] = result
                        logger.info(f"Análise de {symbol} concluída - "
                                    f"Decisão: {result['trading_decision']['action']}, "
                                    f"Aprovado: {result['approval']}")
                    except Exception as e:
                        logger.error(f"Erro ao analisar {symbol}: {e}")
                        session_results['results'][symbol] = {'error': str(e)}
            await asyncio.gather(*(analyze_with_limit(symbol) for symbol in batch))

        session_results['end_time'] = datetime.now()
        session_results['duration'] = (
            session_results['end_time'] - session_results['start_time']
        ).total_seconds()
        total_analyses = len([r for r in session_results['results'].values() if 'error' not in r])
        approved_trades = len([r for r in session_results['results'].values() if r.get('approval', False)])
        executed_trades = len([r for r in session_results['results'].values() if r.get('executed_trade') is not None])
        session_results['summary'] = {
            'total_symbols': len(symbols),
            'successful_analyses': total_analyses,
            'approved_trades': approved_trades,
            'executed_trades': executed_trades,
            'approval_rate': approved_trades / total_analyses if total_analyses > 0 else 0,
            'execution_rate': executed_trades / approved_trades if approved_trades > 0 else 0
        }
        logger.info(f"Sessão concluída: {total_analyses} análises, "
                   f"{approved_trades} aprovações, {executed_trades} execuções")
        await self.close_db()
        return session_results

    def get_portfolio_performance(self):
        executed_trades = self.exchange.executed_trades
        if not executed_trades:
            return {'message': 'Nenhuma operação executada ainda'}
        total_trades = len(executed_trades)
        buy_trades = [t for t in executed_trades if t['action'] == 'buy']
        sell_trades = [t for t in executed_trades if t['action'] == 'sell']
        total_volume = sum(t['executed_price'] * t['quantity'] for t in executed_trades)
        return {
            'total_trades': total_trades,
            'buy_trades': len(buy_trades),
            'sell_trades': len(sell_trades),
            'total_volume': total_volume,
            'average_trade_size': total_volume / total_trades if total_trades > 0 else 0,
            'recent_trades': executed_trades[-5:] if executed_trades else []
        }

    def get_agent_performance(self):
        performance = {}
        for agent in self.all_agents:
            if hasattr(agent, 'analysis_history') and agent.analysis_history:
                analyses = agent.analysis_history
                avg_confidence = sum(a.get('confidence', 0) for a in analyses) / len(analyses)
                recommendations = [a.get('recommendation') for a in analyses if a.get('recommendation')]
                recommendation_counts = {
                    'buy': sum(1 for r in recommendations if r == DecisionType.BUY),
                    'sell': sum(1 for r in recommendations if r == DecisionType.SELL),
                    'hold': sum(1 for r in recommendations if r == DecisionType.HOLD)
                }
                performance[agent.name] = {
                    'total_analyses': len(analyses),
                    'average_confidence': avg_confidence,
                    'recommendations': recommendation_counts,
                    'last_analysis': analyses[-1]['timestamp'].isoformat() if analyses else None
                }
        return performance 