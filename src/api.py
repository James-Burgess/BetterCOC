from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from coc_tools.jobs.greeting import greet
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
    return greet("API user")


@app.get("/sessions/")
async def sessions():
    sesh = list_sessions(db)
    return _list_normailzer(sesh)


@app.get("/sessions/latest/")
async def sessions():
    sesh = last_session(db)
    print(list(sesh))
    return _item_normalizer(sesh)


class Session(BaseModel):
    name: str


@app.post("/sessions/")
async def new_session(session: Session):
    return create_session(db, session.name)


@app.get("/sessions/{session_name}/")
async def session_detail(session_name):
    print(session_name)
    ret = get_session(db, session_name)
    if not ret:
        raise HTTPException(status_code=404, detail="Item not found")

    return _item_normalizer(ret)


def _list_normailzer(items):
    return [_item_normalizer(s) for s in items]


def _item_normalizer(item):
    return {"id": str(item.pop("_id")), **item}

# Start match
# Get match stats
