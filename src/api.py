from fastapi import FastAPI
from pydantic import BaseModel

from coc_tools.jobs.greeting import greet
from coc_tools.db import create_connection, list_sessions, create_session, get_session

app = FastAPI()
db = create_connection()


@app.get("/")
async def root():
    return greet("API user")


@app.get('/sessions/')
async def sessions():
    return list_sessions(db)


class Session(BaseModel):
    name: str


@app.post("/sessions/")
async def new_session(session: Session):
    return create_session(db, session.name)


@app.get("/sessions/{session_name}/")
async def session_detail(session_name):
    return get_session(db, session_name)


# Start match
# Get match stats
