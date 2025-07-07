# services/monitoring.py 
import threading
import asyncio
import time
import logging
from services.orchestrator import TradingAgentsSystem

logger = logging.getLogger(__name__)

class RealTimeMonitor:
    def __init__(self, system: TradingAgentsSystem):
        self.system = system
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self, symbols, interval=300):
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(symbols, interval)
        )
        self.monitor_thread.start()
        logger.info(f"Monitoramento iniciado para {symbols} (intervalo: {interval}s)")
    
    def stop_monitoring(self):
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        logger.info("Monitoramento parado")
    
    def _monitor_loop(self, symbols, interval):
        while self.monitoring:
            try:
                asyncio.run(self._quick_analysis(symbols))
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                time.sleep(60)
    
    async def _quick_analysis(self, symbols):
        for symbol in symbols:
            try:
                market_data = self.system.market_data_provider.get_market_data(symbol)
                technical_data = self.system.market_data_provider.get_technical_indicators(symbol)
                if abs(market_data.change_percent) > 2:
                    logger.info(f"🚨 {symbol}: {market_data.change_percent:+.2f}% - Preço: ${market_data.price:.2f}")
                if technical_data.rsi < 25 or technical_data.rsi > 75:
                    logger.info(f"⚠️ {symbol}: RSI extremo {technical_data.rsi:.1f}")
            except Exception as e:
                logger.error(f"Erro na análise rápida de {symbol}: {e}") 