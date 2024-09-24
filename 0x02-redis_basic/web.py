#!/usr/bin/env python3
"""
module created for caching and tracking purpose
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def response_cacher(method: Callable) -> Callable:
    """ decorator for caching and tracking
    """
    @wraps(method)
    def invoker(url) -> str:
        """ wrapper function checks redis store if the response is
        already there or if not caches the response for 10 sec and
        return response
        """
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@response_cacher
def get_page(url: str) -> str:
    """ returns  the HTML content of a particular URL
    """
    return requests.get(url).text
