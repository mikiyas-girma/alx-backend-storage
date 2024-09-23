#!/usr/bin/env python3
""" Module for working with redis
"""

import redis
from typing import Union
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
