from unittest.mock import patch
from books.infrastructure.cache.redis_cache import redis_cache, redis_client
import json
import pytest
from datetime import timedelta

test_prefix = "test_prefix"
default_ttl = 7200


@redis_cache(cache_key_prefix=test_prefix)
def sample_function(_self, arg1):
    return {"result": f"Computed value for {arg1}"}


@pytest.mark.parametrize(
    "cache_key, cached_value",
    [
        [
            "test_key",
            {"result": "Cached value for 'test_key'"},
        ]
    ],
)
def test_redis_cache_hit(cache_key, cached_value):
    with patch.object(
        redis_client,
        "get",
        return_value=json.dumps(cached_value),
    ) as mock_get:
        with patch.object(redis_client, "setex") as mock_set:
            result = sample_function(None, cache_key)

            assert result == cached_value
            mock_get.assert_called_once_with(f"{test_prefix}:{cache_key}")

            mock_set.assert_not_called()


@pytest.mark.parametrize("cache_key", ["test_key"])
def test_redis_cache_miss(cache_key):
    expected_value = {"result": f"Computed value for {cache_key}"}
    with patch.object(redis_client, "get", return_value=None) as mock_get:
        with patch.object(redis_client, "setex") as mock_set:
            result = sample_function(None, cache_key)

            assert result == expected_value

            mock_get.assert_called_once_with(f"{test_prefix}:{cache_key}")

            mock_set.assert_called_once()
            args, kwargs = mock_set.call_args
            assert args[0] == f"{test_prefix}:{cache_key}"
            assert json.loads(args[2]) == expected_value
