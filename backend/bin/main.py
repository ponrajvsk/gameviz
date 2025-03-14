from fastapi import FastAPI
from db.db import CollectionAdapters

# FastAPI app
app = FastAPI()


@app.get("/")
async def test():
    await CollectionAdapters.PLAYERS.insert_one({"name": "ponraj"})
