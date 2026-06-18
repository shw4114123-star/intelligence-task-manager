from pydantic import BaseModel
from typing import Literal


class Checkagentdata(BaseModel):
    name : str
    specialty : str
    is_active : bool
    completed_missions : int
    failed_missions : int 
    agent_rank : Literal["Junior", "Senior", "Commander"]


class Checkmissionsdata(BaseModel):
    title : str
    description : str
    location : str
    difficulty : int
    importance : int
    status : Literal["NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED"] 
    assigned_agent_id : int | None


def check_risk_level(difficulty, importance):
    result = difficulty * 2 + importance
    if result <= 9:
        return "LOW"
    elif result <= 17:
        return "MEDIUM"
    elif result <= 24:
        return "HIGH"
    else:
        return "CRITICAL"
    