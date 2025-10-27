from fastapi import FastAPI
from app.api.v1.users import router as user_router
from app.api.v1 import users, inventory

app = FastAPI()

app.include_router(user_router)
app.include_router(inventory.router)

@app.get("/")
def home():
    return {"message": "hello world!"}
