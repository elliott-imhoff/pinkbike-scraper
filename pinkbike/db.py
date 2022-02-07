"""Connect to the mongo pinkbike database."""

import os

import pymongo


def connect():
    """Connect to the mongo pinkbike database."""
    mongo_connect = os.getenv("MONGO_CONNECT")
    client = pymongo.MongoClient(
        f"mongodb+srv://{mongo_connect}/pinkbike?retryWrites=true&w=majority"
    )
    return client.pinkbike
