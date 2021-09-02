from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils import types
from coc_tools.jobs import responses, game
from coc_tools.db import (
    create_connection,
    list_sessions,
    last_session,
    create_session,
    get_session,
)

app = FastAPI()
db = create_connection()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return responses.greet("API user")


@app.get("/sessions/")
async def sessions():
    sesh = list_sessions(db)
    return _list_normalizer(sesh)


@app.get("/sessions/latest/")
async def latest_session():
    sesh = last_session(db)
    print(list(sesh))
    return _item_normalizer(sesh)


@app.post("/sessions/")
async def new_session(session: types.Session):
    return create_session(db, session.name)


@app.get("/sessions/{session_id}/")
async def session_detail(session_id):
    ret = get_session(db, session_id)
    # TODO: calculate session leaderboard
    if not ret:
        raise HTTPException(status_code=404, detail="Item not found")

    return _item_normalizer(ret)


@app.post("/game/new/")
async def create_game(session_id: types.SessionId):
    game_id = game.start_and_watch(session_id.id)
    return {"id": game_id}


@app.get("/game/latest")
async def latest_game():
    return {"id": "newestgameid"}


@app.get("/game/{game_id}/")
async def game_detail(game_id):
    return {"id": game_id}


def _list_normalizer(items):
    return [_item_normalizer(s) for s in items]


def _item_normalizer(item):
    return {"id": str(item.pop("_id")), **item}
