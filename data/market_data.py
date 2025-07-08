# data/market_data.py 
import random
from datetime import datetime, timedelta
from core.data_models import MarketData, TechnicalIndicators
import yfinance as yf

class MarketDataProvider:
    def __init__(self):
        self._market_data_cache = {}
        self._technical_cache = {}
        self.cache_duration = timedelta(minutes=5)

    def get_market_data(self, symbol: str) -> MarketData:
        now = datetime.now()
        cache_entry = self._market_data_cache.get(symbol)
        if cache_entry:
            data, ts = cache_entry
            if now - ts < self.cache_duration:
                return data
        # Busca dados reais do yfinance
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get('regularMarketPrice')
            volume = info.get('volume')
            previous_close = info.get('regularMarketPreviousClose')
            change_percent = ((price - previous_close) / previous_close * 100) if price and previous_close else 0.0
            market_cap = info.get('marketCap', 0.0)
            pe_ratio = info.get('trailingPE', 0.0)
            data = MarketData(
                symbol=symbol,
                price=price or 0.0,
                volume=volume or 0,
                change_percent=change_percent,
                market_cap=market_cap or 0.0,
                pe_ratio=pe_ratio or 0.0,
                timestamp=now
            )
            self._market_data_cache[symbol] = (data, now)
            return data
        except Exception:
            pass
        # Fallback: simulação
        price = random.uniform(50, 500)
        volume = random.randint(1000000, 10000000)
        change_percent = random.uniform(-5, 5)
        market_cap = random.uniform(1e9, 1e12)
        pe_ratio = random.uniform(10, 30)
        data = MarketData(
            symbol=symbol,
            price=price,
            volume=volume,
            change_percent=change_percent,
            market_cap=market_cap,
            pe_ratio=pe_ratio,
            timestamp=now
        )
        self._market_data_cache[symbol] = (data, now)
        return data

    def get_technical_indicators(self, symbol: str) -> TechnicalIndicators:
        now = datetime.now()
        cache_entry = self._technical_cache.get(symbol)
        if cache_entry:
            data, ts = cache_entry
            if now - ts < self.cache_duration:
                return data
        # Busca dados reais do yfinance
        try:
            df = yf.download(symbol, period="3mo", interval="1d", progress=False)
            if not df.empty:
                closes = df['Close'].tolist()
                rsi = self._calc_rsi(closes)
                macd = self._calc_macd(closes)
                ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else closes[-1]
                ma50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else closes[-1]
                bollinger_upper = ma20 + 2 * self._stddev(closes[-20:]) if len(closes) >= 20 else ma20
                bollinger_lower = ma20 - 2 * self._stddev(closes[-20:]) if len(closes) >= 20 else ma20
                volume_sma = df['Volume'][-20:].mean() if len(df['Volume']) >= 20 else df['Volume'][-1]
                data = TechnicalIndicators(
                    symbol=symbol,
                    rsi=rsi,
                    macd=macd,
                    moving_avg_20=ma20,
                    moving_avg_50=ma50,
                    bollinger_upper=bollinger_upper,
                    bollinger_lower=bollinger_lower,
                    volume_sma=volume_sma,
                    timestamp=now
                )
                self._technical_cache[symbol] = (data, now)
                return data
        except Exception:
            pass
        # Fallback: simulação
        data = TechnicalIndicators(
            symbol=symbol,
            rsi=random.uniform(20, 80),
            macd=random.uniform(-2, 2),
            moving_avg_20=random.uniform(45, 55),
            moving_avg_50=random.uniform(40, 60),
            bollinger_upper=random.uniform(55, 65),
            bollinger_lower=random.uniform(35, 45),
            volume_sma=random.randint(500000, 2000000),
            timestamp=now
        )
        self._technical_cache[symbol] = (data, now)
        return data

    def _calc_rsi(self, closes, period=14):
        if len(closes) < period + 1:
            return 50.0
        gains = [max(0, closes[i] - closes[i-1]) for i in range(1, period+1)]
        losses = [max(0, closes[i-1] - closes[i]) for i in range(1, period+1)]
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def _calc_macd(self, closes, fast=12, slow=26, signal=9):
        if len(closes) < slow + signal:
            return 0.0
        def ema(prices, period):
            k = 2 / (period + 1)
            ema_val = prices[0]
            for price in prices[1:]:
                ema_val = price * k + ema_val * (1 - k)
            return ema_val
        macd_line = ema(closes[-fast:], fast) - ema(closes[-slow:], slow)
        return macd_line

    def _stddev(self, values):
        mean = sum(values) / len(values)
        return (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5 