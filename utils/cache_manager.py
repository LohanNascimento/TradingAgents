# utils/cache_manager.py
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, Any, Generic, TypeVar
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class CacheEntry(Generic[T]):
    """Entrada do cache com timestamp e TTL"""
    data: T
    timestamp: datetime
    ttl: timedelta
    
    @property
    def is_expired(self) -> bool:
        return datetime.now() - self.timestamp > self.ttl

class ThreadSafeCache(Generic[T]):
    """Cache thread-safe com TTL automático e limpeza periódica"""
    
    def __init__(self, default_ttl: timedelta, max_size: int = 1000):
        self._cache: Dict[str, CacheEntry[T]] = {}
        self._lock = threading.RLock()
        self._default_ttl = default_ttl
        self._max_size = max_size
        self._last_cleanup = datetime.now()
        self._cleanup_interval = timedelta(minutes=30)
    
    def get(self, key: str) -> Optional[T]:
        """Obtém item do cache se não estiver expirado"""
        with self._lock:
            self._maybe_cleanup()
            entry = self._cache.get(key)
            if entry and not entry.is_expired:
                return entry.data
            elif entry:
                # Remove entrada expirada
                del self._cache[key]
            return None
    
    def set(self, key: str, value: T, ttl: Optional[timedelta] = None) -> None:
        """Adiciona item ao cache"""
        with self._lock:
            self._maybe_cleanup()
            
            # Verifica limite de tamanho
            if len(self._cache) >= self._max_size:
                self._evict_oldest()
            
            entry = CacheEntry(
                data=value,
                timestamp=datetime.now(),
                ttl=ttl or self._default_ttl
            )
            self._cache[key] = entry
    
    def invalidate(self, key: str) -> None:
        """Remove item específico do cache"""
        with self._lock:
            self._cache.pop(key, None)
    
    def clear(self) -> None:
        """Limpa todo o cache"""
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        """Retorna tamanho atual do cache"""
        with self._lock:
            return len(self._cache)
    
    def _maybe_cleanup(self) -> None:
        """Executa limpeza se necessário"""
        now = datetime.now()
        if now - self._last_cleanup > self._cleanup_interval:
            self._cleanup_expired()
            self._last_cleanup = now
    
    def _cleanup_expired(self) -> None:
        """Remove todas as entradas expiradas"""
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.is_expired
        ]
        for key in expired_keys:
            del self._cache[key]
    
    def _evict_oldest(self) -> None:
        """Remove a entrada mais antiga"""
        if not self._cache:
            return
        
        oldest_key = min(
            self._cache.keys(),
            key=lambda k: self._cache[k].timestamp
        )
        del self._cache[oldest_key]

class CacheManager:
    """Gerenciador centralizado de múltiplos caches"""
    
    def __init__(self):
        self._caches: Dict[str, ThreadSafeCache] = {}
        self._lock = threading.Lock()
    
    def get_cache(self, name: str, default_ttl: timedelta, max_size: int = 1000) -> ThreadSafeCache:
        """Obtém ou cria um cache específico"""
        with self._lock:
            if name not in self._caches:
                self._caches[name] = ThreadSafeCache(default_ttl, max_size)
            return self._caches[name]
    
    def clear_all(self) -> None:
        """Limpa todos os caches"""
        with self._lock:
            for cache in self._caches.values():
                cache.clear()
    
    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas dos caches"""
        with self._lock:
            return {name: cache.size() for name, cache in self._caches.items()}

# Instância global do gerenciador de cache
cache_manager = CacheManager()