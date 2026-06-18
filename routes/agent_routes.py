from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from logs.my_logger import logger
from database.validations import Checkagentdata


router = APIRouter(prefix="/agents", tags=["agents"])
agent = AgentDB()

@router.post("/")
def create_new_agent(dict: Checkagentdata):
    try:
        agent.create_agent(dict)
    except Exception as e:
        logger.error(f"error: {e}")
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.get("/")
def show_all_agent():
    agents = agent.get_all_agents()
    return agents

@router.get("/{id}")
def show_agent_by_id(id: int):
    if agent.check_agent_exists(id):
        return agent.get_agent_by_id(id)
    else:
        logger.error("error : not found")
        raise HTTPException(status_code=404, detail="not found agent with this id.")
    
@router.put("/{id}")
def cheng_agent(id: int, data: Checkagentdata):
    if agent.check_agent_exists(id):
        agent.update_agent(id, data)
        return "the agent updated succecfuly"
    else:
        logger.error("error : not found")
        raise HTTPException(status_code=404, detail="not found agent with this id.")
    
@router.put("/{id}/deactivate")
def shutdoun_agent(id: int):
    if agent.check_agent_exists(id):
        agent.deactivate_agent(id)
        return "the agent disabled"
    else:
        logger.error("error : not found")
        raise HTTPException(status_code=404, detail="not found agent with this id.")
    
@router.get("/{id}/performance")
def agent_performance(id: int):
    if agent.check_agent_exists(id):
        performance = agent.get_agent_performance(id)
        return performance
    else:
        logger.error("error : not found")
        raise HTTPException(status_code=404, detail="not found agent with this id.")
