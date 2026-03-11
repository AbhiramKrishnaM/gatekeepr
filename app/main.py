from enum import Enum
from fastapi import FastAPI

app = FastAPI()

# check if the server is running 
@app.get("/")
async def root():
    return {"message":"server is up and running!"}
