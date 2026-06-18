from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB
from logs.my_logger import logger
from database.validations import Checkmissionsdata



router = APIRouter(prefix="/reports", tags=["repoerts"])
agent = AgentDB()
mission = MissionDB()


@router.get("/summary")
def General_report():
    try:
        active_agents_count = agent.count_active_agents()
        total_missions = mission.count_all_missions()
        open_missions = mission.count_open_missions()
        completed_missions = mission.count_by_status("COMPLETED")
        failed_missions = mission.count_by_status("FAILED")
        critical_missions = mission.count_critical_missions()
        return {"active_agents_count" : active_agents_count,
                "total_missions" : total_missions,
                "open_missions" : open_missions,
                "completed_missions" : completed_missions,
                "failed_missions" : failed_missions,
                "critical_missions" :critical_missions
                }
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.get("/missions-by-status")
def missions_by_status():
    try:
        assignes = mission.count_by_status("ASSIGNED")
        in_progress = mission.count_by_status("IN_PROGRESS")
        completed = mission.count_by_status("COMPLETED")
        failed = mission.count_by_status("FAILED")
        cancelled = mission.count_by_status("CANCELLED")
        return {"open" : assignes + in_progress,
                "in_progress" : in_progress,
                "completed" : completed,
                "failed" : failed,
                "cancelled" : cancelled}
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=500, detail=f"{e}")

@router.get("/top-agent")
def top_agent():
    try:
        top = mission.get_top_agent()
        return top
    except Exception as e:
        logger.error(f"error : {e}")
        raise HTTPException(status_code=500, detail=f"{e}")