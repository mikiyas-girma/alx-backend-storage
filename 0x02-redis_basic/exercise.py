#!/usr/bin/env python3
""" Module for working with redis
"""

import redis
from typing import Union, Callable, Optional
from uuid import uuid4


class Cache:
    """Cache class"""

    def __init__(self):
        """ initialization method """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
