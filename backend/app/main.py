from fastapi import FastAPI
from app.api.v1.users import router as user_router

app = FastAPI()

app.include_router(user_router)


@app.get("/")
def home():
    return {"message": "hello world!"}
