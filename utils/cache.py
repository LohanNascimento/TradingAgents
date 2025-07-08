import redis
import hashlib
import json
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def make_cache_key(*args):
    key = ":".join(str(a) for a in args)
    return hashlib.sha256(key.encode()).hexdigest()

def get_cache(key):
    value = cache.get(key)
    if value is not None:
        return json.loads(value)
    return None

def set_cache(key, value, expire=3600):
    cache.set(key, json.dumps(value), ex=expire) 