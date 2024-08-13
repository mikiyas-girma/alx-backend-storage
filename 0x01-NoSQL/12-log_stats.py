#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def show_stats(mongo_collection, option=None):
    """provides stats about nginx logs
    """
    METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    if option:
        value = mongo_collection.count_documents(
            {"method": option})
        print(f"\tmethod {option}: {value}")
        return

    result = mongo_collection.count_documents({})
    print(f"{result} logs")
    print("Methods:")
    for method in METHODS:
        show_stats(nginx_collection, method)
    status_check = mongo_collection.count_documents({"path": "/status"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    show_stats(nginx_collection)
