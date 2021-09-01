from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from coc_tools.jobs.greeting import greet
from coc_tools.db import create_connection, list_sessions, create_session, get_session

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


@app.get('/sessions/')
async def sessions():
    sesh = list_sessions(db)
    return _list_normailzer(sesh)


class Session(BaseModel):
    name: str


@app.post("/sessions/")
async def new_session(session: Session):
    return create_session(db, session.name)


@app.get("/sessions/{session_name}/")
async def session_detail(session_name):
    return get_session(db, session_name)

def _list_normailzer(items):
    return [{"id": str(s.pop("_id")), **s} for s in items]

# Start match
# Get match stats
