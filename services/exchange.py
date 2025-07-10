# services/exchange.py 
from datetime import datetime
import random
import logging
from data.market_data import market_data_provider

logger = logging.getLogger(__name__)

class SimulatedExchange:
    def __init__(self):
        self.orders = []
        self.executed_trades = []
    
    def submit_order(self, decision):
        order_id = f"ORD_{len(self.orders) + 1:06d}"
        # Busca preço real de mercado no momento da execução
        market_data = market_data_provider.get_market_data(decision.symbol)
        execution_price = market_data.price if market_data else decision.price
        executed_trade = {
            'order_id': order_id,
            'symbol': decision.symbol,
            'action': decision.action.value,
            'quantity': decision.quantity,
            'requested_price': decision.price,
            'executed_price': execution_price,
            'timestamp': datetime.now(),
            'status': 'EXECUTED'
        }
        self.executed_trades.append(executed_trade)
        logger.info(f"Ordem executada: {order_id} - {decision.action.value} {decision.quantity} {decision.symbol} @ ${execution_price:.2f}")
        return executed_trade 