#!/usr/bin/env python3
""" Module for working with redis
"""

import redis
from typing import Union, Callable, Optional
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Counts the number of calls made to a method in a Cache class
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ after incrementing the counter for call made to the method
        it invokes the method
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Tracks the call history of a method in a cache class
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """calls the method after storing the input and output of the
        method in a redis list
        """
        input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


class Cache:
    """Cache class"""

    def __init__(self):
        """ initialization method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generates a random key and stores
            the input data
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """get method that take a key string argument and
        an optional Callable argument named fn
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ automatically parametrize Cache.get to str """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ automatically parametrize Cache.get to int """
        return self.get(key, lambda x: int(x))
