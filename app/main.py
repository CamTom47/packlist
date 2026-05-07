from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from app.routers import items, auths, users, trips, packs

app = FastAPI()
app.include_router(users.router)
app.include_router(items.router)
app.include_router(auths.router)
app.include_router(packs.router)
app.include_router(trips.router)