#!/usr/bin/env python3
"""
module created for caching and tracking purpose
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis = redis.Redis()


def response_cacher(method: Callable) -> Callable:
    """ decorator for caching and tracking
    """
    @wraps(method)
    def invoker(url) -> str:
        """ wrapper function checks redis store if the response is
        already there or if not caches the response for 10 sec and
        return response
        """
        cache_data = redis.get(f'cached:{url}')
        if cache_data:
            return cache_data.decode('utf-8')

        count_key = 'count:' + url
        response = method(url)

        redis.incr(count_key)
        redis.setex(f'cached:{url}', 10, response)
        return response
    return invoker


@response_cacher
def get_page(url: str) -> str:
    """ returns  the HTML content of a particular URL
    """
    return requests.get(url).text
