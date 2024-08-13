#!/usr/bin/env python3
"""Python function that changes all topics of a
school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """changes a collection with given name with
    provided topics
    """
    result = mongo_collection.update_many(
                {"name": name},
                {"$set": {"topics": topics}}
            )

    return result
