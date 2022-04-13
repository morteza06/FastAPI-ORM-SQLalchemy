from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.vote import vote
from . import models
from .database import engine
from .routers import user, post, auth, vote
from .config import settings

from app import database

# models.Base.metadata.create_all(bind=engine)          # with alembic no need this command to generate 

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/" )  #decorator for clear request fastapi is Get
def root():
    return {"message": "Hello World successfully deployed from CI/CD pipeline"}