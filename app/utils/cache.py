# utils/cache.py

from typing import Optional
from threading import Lock
import time

# Simple in-memory cache with TTL
_cache = {}
_cache_lock = Lock()
DEFAULT_TTL = 60 * 60  # 1 hour

def get_from_cache(key: str) -> Optional[dict]:
    with _cache_lock:
        if key in _cache:
            value, expiry = _cache[key]
            if time.time() < expiry:
                return value
            else:
                del _cache[key]  # Expired
    return None

def set_in_cache(key: str, value: dict, ttl: int = DEFAULT_TTL):
    with _cache_lock:
        _cache[key] = (value, time.time() + ttl)

def invalidate_cache(key: str):
    with _cache_lock:
        if key in _cache:
            del _cache[key]
