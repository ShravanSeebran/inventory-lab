from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
from app.api.v1.users import router as user_router
from app.api.v1 import users, inventory
from app.db import Base, engine


@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
frontend = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/assets", StaticFiles(directory=frontend / "src" / "assets"), name="assets")


@app.get("/register", include_in_schema=False)
def registration_page():
    return FileResponse(frontend / "public" / "index.html")


@app.get("/login", include_in_schema=False)
def login_page():
    return FileResponse(frontend / "public" / "login.html")

app.include_router(user_router)
app.include_router(inventory.router)

@app.get("/")
def home():
    return {"message": "hello world!"}
