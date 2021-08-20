import time

from pymongo import MongoClient


DB_URL = "0.0.0.0:27017"
DB_NAME = "test"


def create_connection():
    client = MongoClient(DB_URL)
    return client[DB_NAME]


def list_sessions(cnxn):
    cursor = cnxn.sessions.find({})
    return list(cursor)


def create_session(cnxn, name):
    cnxn.sessions.insert({
        "date": time.time_ns(),
        "name": name,
        "games": []
    })


def list_games(cnxn):
    cursor = cnxn.games.find({})
    return list(cursor)


def get_game(cnxn, game):
    cursor = cnxn.games.find_one({"_id": game})
    return cursor


def add_game(cnxn, session, game):
    game_id = cnxn.games.insert({"_id": game})

    sesh = {"_id": session}
    cnxn.sessions.update_one(sesh, {"$push": {"games": game}})

    return game_id


def add_test(cnxn, test, game_id):
    cnxn.games.update_one({"_id": game_id}, {"$push": {"test": test}})


def update_game(cnxn, game):
    cnxn.games.update_one({"_id": game.get("_id")}, {"$set": game})
