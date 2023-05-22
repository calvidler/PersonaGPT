from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from pydantic import BaseModel
from models import Agent

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


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/agents")
def get_all_agents():
    agents = world.get_all_agents()
    return agents


@app.put("/deactivate/{agent_id}")
def deactivate_agent(agent_id: int):
    world.deactivate_agent(agent_id)
    return {"message": f"Agent {agent_id} deactivated."}


@app.put("/activate/{agent_id}")
def activate_agent(agent_id: int):
    world.activate_agent(agent_id)
    return {"message": f"Agent {agent_id} activated."}


@app.get("/dialog/history")
def get_dialog_history():
    dialog_history = world.get_dialog_history()
    return dialog_history


@app.get("/dialog/history/{agent_id}")
def get_agent_dialog_history(agent_id: int):
    dialog_history = world.get_agent_dialog_history(agent_id)
    return dialog_history


@app.post("/query/{agent_id}", description="Query a specific agent.")
def query_agent(request: QueryRequest, agent_id: int = None):
    try:
        response = world.query_agent(request.query, agent_id)
        return QueryResponse(**response)
    except HTTPException as e:
        raise e


@app.post("/query", description="Query a random active agent.")
def query_agent(request: QueryRequest):
    try:
        response = world.query_agent(request.query)
        return QueryResponse(**response)
    except HTTPException as e:
        raise e


@app.post("/query/all", description="Query all active agents.")
def query_all_agents(request: QueryRequest):
    try:
        responses = []
        for agent in world.get_all_agents():
            response = world.query_agent(request.query, agent.id)
            responses.append(response)
        return responses
    except HTTPException as e:
        raise e


@app.get("/dialog/history/human")
def get_human_dialog_history():
    dialog_history = world.get_human_dialog_history()
    return dialog_history


@app.get("/actions/history")
def get_action_history():
    action_history = world.get_actions()
    return action_history
