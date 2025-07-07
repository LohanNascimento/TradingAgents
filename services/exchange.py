# services/exchange.py 
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)

class SimulatedExchange:
    def __init__(self):
        self.orders = []
        self.executed_trades = []
    
    def submit_order(self, decision):
        order_id = f"ORD_{len(self.orders) + 1:06d}"
        execution_price = decision.price * random.uniform(0.995, 1.005)
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