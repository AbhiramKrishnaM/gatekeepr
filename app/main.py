from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str
    price: int

# check if the server is running 
@app.get("/")
async def root():
    return {"message":"server is up and running!"}

# post
@app.post("/items")
def create_item(item:Item):
    return item 