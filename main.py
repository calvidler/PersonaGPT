from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from word import World

app = FastAPI()
world = World(db_file="world.db")




class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    agent_id: int
    agent_name: str
    query: str
    response: str
    timestamp: str


@app.get("/agents")
def get_all_agents():
    agents = world.get_all_agents()
    return agents


@app.post("/query")
def query_agent(request: QueryRequest):
    try:
        response = world.query_agent(request.query)
        return QueryResponse(**response)
    except HTTPException as e:
        raise e


@app.put("/deactivate/{agent_id}")
def deactivate_agent(agent_id: int):
    world.deactivate_agent(agent_id)
    return {"message": f"Agent {agent_id} deactivated."}
