from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.utils.database import create_db_and_tables
from src import *
from src.modules.authentication.route import auth

"""
An asynchronous context manager for managing the lifespan of the FastAPI application.

This function is intended to be used with FastAPI's lifespan event to perform
setup and teardown operations when the application starts and stops.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST", "PATCH"]
)


@app.get("/", tags=["Health"])
def root():
    return JSONResponse(
        content={"message": "Biometric API service is Active.."}, status_code=200
    )
