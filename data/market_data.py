# data/market_data.py
import logging
import time
from datetime import datetime
from typing import Optional
import yfinance as yf
import pandas as pd

from core.data_models import MarketData, TechnicalIndicators
from config.settings import settings
from utils.cache_manager import cache_manager
from utils.technical_indicators import TechnicalIndicatorCalculator
from utils.data_fallback import fallback_generator

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketDataProvider:
    """Provedor otimizado de dados de mercado com cache avançado"""
    
    def __init__(self):
        # Inicializa caches especializados
        self._market_cache = cache_manager.get_cache(
            'market_data', 
            settings.cache.market_data_ttl,
            settings.cache.max_cache_size
        )
        self._technical_cache = cache_manager.get_cache(
            'technical_indicators', 
            settings.cache.technical_indicators_ttl,
            settings.cache.max_cache_size
        )
        self._calculator = TechnicalIndicatorCalculator()
    
    def get_market_data(self, symbol: str) -> MarketData:
        """Obtém dados de mercado com cache otimizado"""
        # Verifica cache primeiro
        cached_data = self._market_cache.get(symbol)
        if cached_data:
            logger.debug(f"Cache hit for market data: {symbol}")
            return cached_data
        
        # Busca dados reais
        market_data = self._fetch_real_market_data(symbol)
        
        # Fallback se necessário
        if not market_data and settings.enable_fallback:
            logger.warning(f"Using fallback data for market: {symbol}")
            market_data = fallback_generator.generate_market_data(symbol)
        
        # Armazena no cache se obtido com sucesso
        if market_data:
            self._market_cache.set(symbol, market_data)
            logger.debug(f"Cached market data for: {symbol}")
        
        return market_data
    
    def get_technical_indicators(self, symbol: str) -> TechnicalIndicators:
        """Obtém indicadores técnicos com cache otimizado"""
        # Verifica cache primeiro
        cached_data = self._technical_cache.get(symbol)
        if cached_data:
            logger.debug(f"Cache hit for technical indicators: {symbol}")
            return cached_data
        
        # Calcula indicadores reais
        technical_data = self._calculate_real_technical_indicators(symbol)
        
        # Fallback se necessário
        if not technical_data and settings.enable_fallback:
            logger.warning(f"Using fallback data for technical indicators: {symbol}")
            technical_data = fallback_generator.generate_technical_indicators(symbol)
        
        # Armazena no cache se obtido com sucesso
        if technical_data:
            self._technical_cache.set(symbol, technical_data)
            logger.debug(f"Cached technical indicators for: {symbol}")
        
        return technical_data
    
    def _fetch_real_market_data(self, symbol: str) -> Optional[MarketData]:
        """Busca dados reais de mercado com retry e timeout"""
        for attempt in range(settings.market_data.max_retries):
            try:
                logger.info(f"Fetching market data for {symbol} (attempt {attempt + 1})")
                
                # Cria ticker com timeout
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                # Extrai dados principais
                price = info.get('regularMarketPrice') or info.get('currentPrice')
                volume = info.get('volume') or info.get('regularMarketVolume')
                previous_close = info.get('regularMarketPreviousClose') or info.get('previousClose')
                
                # Validação básica
                if not price or not isinstance(price, (int, float)):
                    raise ValueError(f"Invalid price data for {symbol}")
                
                # Calcula mudança percentual
                change_percent = 0.0
                if previous_close and previous_close > 0:
                    change_percent = ((price - previous_close) / previous_close * 100)
                
                # Dados adicionais
                market_cap = info.get('marketCap', 0.0)
                pe_ratio = info.get('trailingPE', 0.0)
                
                market_data = MarketData(
                    symbol=symbol,
                    price=float(price),
                    volume=int(volume or 0),
                    change_percent=float(change_percent),
                    market_cap=float(market_cap or 0.0),
                    pe_ratio=float(pe_ratio or 0.0),
                    timestamp=datetime.now()
                )
                
                logger.info(f"Successfully fetched market data for {symbol}")
                return market_data
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {symbol}: {str(e)}")
                if attempt < settings.market_data.max_retries - 1:
                    time.sleep(settings.market_data.retry_delay)
                continue
        
        logger.error(f"Failed to fetch market data for {symbol} after {settings.market_data.max_retries} attempts")
        return None
    
    def _calculate_real_technical_indicators(self, symbol: str) -> Optional[TechnicalIndicators]:
        """Calcula indicadores técnicos reais com dados históricos"""
        for attempt in range(settings.market_data.max_retries):
            try:
                logger.info(f"Calculating technical indicators for {symbol} (attempt {attempt + 1})")
                
                # Baixa dados históricos
                df = yf.download(
                    symbol,
                    period=settings.market_data.historical_period,
                    interval=settings.market_data.historical_interval,
                    progress=False,
                    timeout=settings.market_data.yfinance_timeout
                )
                # LOG DETALHADO PARA DIAGNÓSTICO
                #logger.info(f"[DEBUG] DataFrame columns for {symbol}: {df.columns}")
                #logger.info(f"[DEBUG] DataFrame shape for {symbol}: {df.shape}")
                #logger.info(f"[DEBUG] DataFrame head for {symbol}:\n{df.head()}\n")
                # NOVO: Se as colunas forem MultiIndex, achata para o primeiro nível
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                if df.empty:
                    raise ValueError(f"No historical data available for {symbol}")
                
                # NOVO: Checa se as colunas necessárias existem
                if 'Close' not in df.columns or 'Volume' not in df.columns:
                    raise ValueError(f"DataFrame missing required columns for {symbol}: {df.columns}")
                
                # Valida dados mínimos
                if len(df) < settings.technical.ma_long_period:
                    logger.warning(f"Insufficient data for full technical analysis: {symbol}")
                
                # Calcula indicadores usando o calculador otimizado
                indicators = self._calculator.calculate_all_indicators(df)
                
                if not indicators:
                    raise ValueError(f"Failed to calculate indicators for {symbol}")
                
                technical_data = TechnicalIndicators(
                    symbol=symbol,
                    rsi=indicators['rsi'],
                    macd=indicators['macd'],
                    moving_avg_20=indicators['moving_avg_20'],
                    moving_avg_50=indicators['moving_avg_50'],
                    bollinger_upper=indicators['bollinger_upper'],
                    bollinger_lower=indicators['bollinger_lower'],
                    volume_sma=indicators['volume_sma'],
                    timestamp=datetime.now()
                )
                
                logger.info(f"Successfully calculated technical indicators for {symbol}")
                return technical_data
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for technical indicators {symbol}: {str(e)}")
                if attempt < settings.market_data.max_retries - 1:
                    time.sleep(settings.market_data.retry_delay)
                continue
        
        logger.error(f"Failed to calculate technical indicators for {symbol} after {settings.market_data.max_retries} attempts")
        return None
    
    def invalidate_cache(self, symbol: str) -> None:
        """Invalida cache para um símbolo específico"""
        self._market_cache.invalidate(symbol)
        self._technical_cache.invalidate(symbol)
        logger.info(f"Cache invalidated for {symbol}")
    
    def clear_all_cache(self) -> None:
        """Limpa todo o cache"""
        self._market_cache.clear()
        self._technical_cache.clear()
        logger.info("All cache cleared")
    
    def get_cache_stats(self) -> dict:
        """Retorna estatísticas do cache"""
        return {
            'market_cache_size': self._market_cache.size(),
            'technical_cache_size': self._technical_cache.size(),
            'total_cache_size': self._market_cache.size() + self._technical_cache.size()
        }

# Instância global do provedor de dados
market_data_provider = MarketDataProvider()