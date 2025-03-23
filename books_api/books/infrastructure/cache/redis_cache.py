import redis
import json
from functools import wraps
from datetime import timedelta

from django.conf import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)


def redis_cache(cache_key_prefix: str, ttl: int = 7200):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{cache_key_prefix}:{args[1]}"

            cache_value = redis_client.get(cache_key)
            if cache_value:
                print(f"Cache hit for key: {cache_key}")
                return json.loads(cache_value)

            result = func(*args, **kwargs)

            redis_client.setex(
                cache_key, timedelta(seconds=ttl), json.dumps(result)
            )
            print(f"Cache miss for key: {cache_key}")
            return result

        return wrapper

    return decorator
