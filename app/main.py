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


@app.get("/return-items")
def return_items():
    return Item(name="soap", description="soap is a good item", price=20)