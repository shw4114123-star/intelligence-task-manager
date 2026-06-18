from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB
from logs.my_logger import logger
from database.validations import Checkmissionsdata


router = APIRouter(prefix="/missions", tags=["missions"])
agent = AgentDB()
mission = MissionDB()

@router.post("/")
def create_new_mission(data: Checkmissionsdata):
    logger.info("post/ start create mission")
    try:
        mission.create_mission(data)
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=500, detail=f"{e}")

@router.get("/")
def show_all_missions():
    try:
        logger.info("get/ calls all agents ")
        missions = mission.get_all_missions()
        return missions
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=500, detail=f"{e}")

@router.get("/{id}")
def show_mission_by_id(id: int):
    if mission.check_mission_exists(id):
        return mission.get_mission_by_id(id)
    else:
        logger.error(f"error : not found")
        raise HTTPException(status_code=404, detail="not found mission with this id.")

@router.put("/{id}/assign/{agent_id}")
def assign_to_agent(id: int, agent_id: int):
    my_agent = agent.get_agent_by_id(agent_id)
    my_mission = mission.get_mission_by_id(id)
    if mission.check_mission_exists(id):
        if agent.check_agent_exists(agent_id):
            if my_agent["is_active"] == True:
                if my_mission["status"] == "NEW":
                    if my_mission["risk_level"] == "CRITICAL" and my_agent["agent_rank"] in ["Senior", "Junior"]:
                        logger.error("error : Only Commander can handle critical missions")
                        raise HTTPException(status_code=400, detail="Only Commander can handle critical missions")
                    else:
                        mission.assign_mission(id, agent_id)
                else:
                    logger.error("error : Mission not available")
                    raise HTTPException(status_code=400, detail="Mission not available.")
            else:
                logger.error("error : Agent is not active")
                raise HTTPException(status_code=400, detail="Agent is not active.")
        else:
            logger.error("error : not found")
            raise HTTPException(status_code=404, detail="Agent not found.")
    else:
        logger.error("error : not found")
        raise HTTPException(status_code=404, detail="Mission not found.")

@router.put("/{id}/start")
def start_mission(id: int):
    if mission.check_mission_exists(id):
        my_mission = mission.get_mission_by_id(id)
        if my_mission["status"] == "NEW":
            mission.update_mission_status(id, "ASSIGNED")
        else:
            raise HTTPException(status_code=400, detail="You cannot start a non-new mission.")
    else:
        logger.error("error : not found")
        raise HTTPException(status_code=404, detail="not found mission with this id.")


@router.put("/{id}/complete")
def ent_mission_cuccecfuly(id: int):
    try:
        if mission.check_mission_exists(id):
            mission.update_mission_status(id, "COMPLETED")
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=500, detail=f"{e}")

@router.put("/{id}/fail")
def ent_mission_failed(id: int):
    try:
        if mission.check_mission_exists(id):
            mission.update_mission_status(id, "FAILED")
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=500, detail=f"{e}")

@router.put("/{id}/cancel")
def cencel_mission(id: int):
    try:
        if mission.check_mission_exists(id):
            mission.update_mission_status(id, "CANCELLED")
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=500, detail=f"{e}")















