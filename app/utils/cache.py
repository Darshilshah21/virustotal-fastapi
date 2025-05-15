from time import time
from app.config import CACHE_TTL

_cache = {}

def get_cache(key):
    entry = _cache.get(key)
    if entry and (time() - entry['timestamp'] < CACHE_TTL):
        return entry['value']
    return None

def set_cache(key, value):
    _cache[key] = {"value": value, "timestamp": time()}