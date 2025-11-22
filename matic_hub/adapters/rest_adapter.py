from fastapi import APIRouter, HTTPException
from matic_hub.bridge.matic_bridge import MaticBridge
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter()

# We need a way to access the bridge instance. 
# In a real app, we'd use dependency injection.
# For now, we'll import the global instance from main (circular import risk, but handled by Python's module caching if careful, or better: use a singleton pattern or pass it in).
# Actually, let's just instantiate a new one or use a singleton pattern in bridge.
# To keep it simple and avoid circular imports with main, we will rely on the fact that the bridge state is in memory.
# A better pattern is to have a `dependencies.py`.
# For this MVP, I'll create a singleton in `matic_bridge.py` or just re-instantiate (which won't share state).
# Let's fix `matic_bridge.py` to be a singleton or use a global variable there.

# RE-WRITING matic_bridge.py approach:
# I will modify `matic_bridge.py` to expose a global `get_bridge()` function.

from matic_hub.bridge.matic_bridge import MaticBridge

# Singleton instance holder
_bridge_instance = None

def get_bridge():
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = MaticBridge()
    return _bridge_instance

class ZoneCommand(BaseModel):
    zone: str

@router.get("/robots")
async def get_robots():
    bridge = get_bridge()
    return list(bridge.robots.values())

@router.get("/robots/{robot_id}")
async def get_robot(robot_id: str):
    bridge = get_bridge()
    status = await bridge.get_robot_status(robot_id)
    if not status:
        raise HTTPException(status_code=404, detail="Robot not found")
    return status

@router.post("/robots/{robot_id}/commands/start")
async def start_cleaning(robot_id: str):
    bridge = get_bridge()
    await bridge.start_cleaning(robot_id)
    return {"status": "command_sent"}

@router.post("/robots/{robot_id}/commands/stop")
async def stop_cleaning(robot_id: str):
    bridge = get_bridge()
    await bridge.stop_cleaning(robot_id)
    return {"status": "command_sent"}

@router.post("/robots/{robot_id}/commands/pause")
async def pause_cleaning(robot_id: str):
    bridge = get_bridge()
    await bridge.pause_cleaning(robot_id)
    return {"status": "command_sent"}

@router.post("/robots/{robot_id}/commands/zone")
async def clean_zone(robot_id: str, cmd: ZoneCommand):
    bridge = get_bridge()
    await bridge.start_cleaning(robot_id, zone=cmd.zone)
    return {"status": "command_sent"}

# --- Mock Data & Endpoints for UI Completeness ---

class Schedule(BaseModel):
    id: str
    name: str
    time: str
    days: List[str]
    zone: Optional[str] = None
    enabled: bool = True

class HistoryItem(BaseModel):
    id: str
    date: str
    duration: str
    area: int
    status: str

# In-memory storage for MVP
_schedules = [
    Schedule(id="1", name="Daily Clean", time="09:00", days=["Mon", "Tue", "Wed", "Thu", "Fri"], zone="whole_house"),
    Schedule(id="2", name="Kitchen After Dinner", time="20:30", days=["Daily"], zone="kitchen")
]

_history = [
    HistoryItem(id="101", date="2025-11-21 09:00", duration="45m", area=350, status="completed"),
    HistoryItem(id="102", date="2025-11-20 09:00", duration="42m", area=340, status="completed"),
    HistoryItem(id="103", date="2025-11-19 20:30", duration="15m", area=120, status="completed"),
]

@router.get("/schedules", response_model=List[Schedule])
async def get_schedules():
    return _schedules

@router.post("/schedules")
async def create_schedule(schedule: Schedule):
    _schedules.append(schedule)
    return schedule

@router.delete("/schedules/{schedule_id}")
async def delete_schedule(schedule_id: str):
    global _schedules
    _schedules = [s for s in _schedules if s.id != schedule_id]
    return {"status": "deleted"}

@router.get("/history", response_model=List[HistoryItem])
async def get_history():
    return _history
