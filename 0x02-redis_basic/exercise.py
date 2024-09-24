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


def replay(method: Callable) -> None:
    """Displays a call history of a method in
    a cache class
    """
    if method is None or not hasattr(method, '__self__'):
        return
    redis_store = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fn_name = method.__qualname__
    input_key = '{}:inputs'.format(fn_name)
    output_key = '{}:outputs'.format(fn_name)
    fn_call_count = 0

    if redis_store.exists(fn_name) != 0:
        fn_call_count = int(redis_store.get(fn_name))
    print('{} was called {} times:'.format(fn_name, fn_call_count))

    fn_inputs = redis_store.lrange(input_key, 0, -1)
    fn_outputs = redis_store.lrange(output_key, 0, -1)
    for fn_input, fn_output in zip(fn_inputs, fn_outputs):
        print('{}(*{}) -> {}'.format(
            fn_name,
            fn_input.decode('utf-8'),
            fn_output
        ))


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
