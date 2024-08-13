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

    print("IPs:")
    req_logs = mongo_collection.aggregate(
        [
            {
                "$group": {"_id": "$ip", "tot_reqs": {"$sum": 1}}
            },
            {
                "$sort": {"tot_reqs": -1}
            },
            {
                "$limit": 10
            },
        ]
    )

    for req in req_logs:
        ip = req['_id']
        ip_count = req['tot_reqs']
        print(f"\t{ip}: {ip_count}")


if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    show_stats(nginx_collection)
