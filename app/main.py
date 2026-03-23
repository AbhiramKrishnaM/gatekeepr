from pydantic import BaseModel
from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

class ActionType(Enum):
    DELETE = "delete"
    READ = "read"
    UPDATE = "update"
    CREATE = "create"
 
class InterceptRequest(BaseModel):
    action: ActionType   # what opeation the agent wants to perform
    agent_id: str # unique identifier for the agent making the request
    target_resource: str #  what type of resource the agent wants to operate on
    target_id: str # the specific id of the resource being acted upon
    action_details: Optional[dict] = None# additional details about the action 
    context: Optional[dict] = None # metadata about when/where/how the action was initiated
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