from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
# from logs.my_logger import logger
from database.validations import Checkagentdata


router = APIRouter()
agent = AgentDB()

@router.post("/agents")
def create_new_agent(dict: Checkagentdata):
    try:
        agent.create_agent(dict)
        agenti = agent.get_all_agents()
        return agenti[-1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.get("/agents")
def show_all_agent():
    agents = agent.get_all_agents()
    return agents

@router.get("/agents/{id}")
def show_agent_by_id(id: int):
    if agent.check_agent_exists(id):
        return agent.get_agent_by_id(id)
    else:
        raise HTTPException(status_code=404, detail="not found agent with this id.")
    
@router.put("/agents/{id}")
def cheng_agent(id: int, data: Checkagentdata):
    if agent.check_agent_exists(id):
        agent.update_agent(id, data)
        return "the agent updated succecfuly"
    else:
        raise HTTPException(status_code=404, detail="not found agent with this id.")
    
@router.put("/agents/{id}/deactivate")
def shutdoun_agent(id: int):
    if agent.check_agent_exists(id):
        agent.deactivate_agent(id)
        return "the agent disabled"
    else:
        raise HTTPException(status_code=404, detail="not found agent with this id.")
    
@router.get("/agents/{id}/performance")
def agent_performance(id: int):
    if agent.check_agent_exists(id):
        performance = agent.get_agent_performance(id)
        return performance
    else:
        raise HTTPException(status_code=404, detail="not found agent with this id.")
