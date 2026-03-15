from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


class InterceptRequest(BaseModel):
    action: str  =  'delete' | 'read' | 'update' | 'create'
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