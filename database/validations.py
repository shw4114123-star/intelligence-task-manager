from pydantic import BaseModel
from typing import Literal


class Checkagentdata(BaseModel):
    id : int
    name : str
    specialty : str
    is_active : bool
    completed_missions : int
    failed_missions : int 
    agent_rank : Literal["Junior", "Senior", "Commander"]


class Checkmissionsdata(BaseModel):
    id : int
    title : str
    description : str
    location : str
    difficulty : int
    importance : int
    status : Literal["NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED"] 
    assigned_agent_id : int | None


def risk_level(difficulty, importance):
    result = difficulty * 2 + importance
    if 0 < result < 9:
        return "LOW"
    elif 10 <= result <= 17:
        return "MEDIUM"
    elif 18 <= result <= 24:
        return "HIGH"
    elif result >= 25:
        return "CRITICAL"