from pydantic import BaseModel
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class ActionType(Enum):
    DELETE = "delete"
    READ = "read"
    UPDATE = "update"
    CREATE = "create"
 
class InterceptRequest(BaseModel):
    action: ActionType
    agent_id: str
    target_resource: str 
    target_id: str
    action_details: dict
    context: dict
class InterceptResponse(BaseModel):
    status: str
    risk_score: float

# check if the server is running 
@app.get("/")
async def root():
    return {"message":"server is up and running!"}

# intercept endpoint
@app.post("/intercept")
def intercept(request: InterceptRequest)-> InterceptResponse:
    return InterceptResponse(status="allowed", risk_score=0.3)