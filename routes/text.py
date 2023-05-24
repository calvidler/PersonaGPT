from fastapi import APIRouter

router = APIRouter()
from fastapi import HTTPException

from pydantic import BaseModel
from config import world


text_router = APIRouter()


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    agent_id: int
    agent_name: str
    query: str
    response: str
    timestamp: str


@text_router.get("/agents")
def get_all_agents():
    agents = world.get_all_agents()
    return agents


@text_router.put("/deactivate/{agent_id}")
def deactivate_agent(agent_id: int):
    world.deactivate_agent(agent_id)
    return {"message": f"Agent {agent_id} deactivated."}


@text_router.put("/activate/{agent_id}")
def activate_agent(agent_id: int):
    world.activate_agent(agent_id)
    return {"message": f"Agent {agent_id} activated."}


@text_router.get("/dialog/history")
def get_dialog_history():
    dialog_history = world.get_dialog_history()
    return dialog_history


@text_router.get("/dialog/history/{agent_id}")
def get_agent_dialog_history(agent_id: int):
    dialog_history = world.get_agent_dialog_history(agent_id)
    return dialog_history


@text_router.post("/query/{agent_id}", description="Query a specific agent.")
def query_agent(request: QueryRequest, agent_id: int = None):
    try:
        response = world.query_agent(request.query, agent_id)
        return QueryResponse(**response)
    except HTTPException as e:
        raise e


@text_router.post("/query", description="Query a random active agent.")
def query_agent(request: QueryRequest):
    try:
        response = world.query_agent(request.query)
        return QueryResponse(**response)
    except HTTPException as e:
        raise e


@text_router.post("/query/all", description="Query all active agents.")
def query_all_agents(request: QueryRequest):
    try:
        responses = []
        for agent in world.get_all_agents():
            response = world.query_agent(request.query, agent.id)
            responses.routerend(response)
        return responses
    except HTTPException as e:
        raise e


@text_router.get("/dialog/history/human")
def get_human_dialog_history():
    dialog_history = world.get_human_dialog_history()
    return dialog_history


@text_router.get("/actions/history")
def get_action_history():
    action_history = world.get_actions()
    return action_history
