import asyncio
import logging
from typing import Dict, Optional, List
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class RobotStatus(BaseModel):
    id: str
    state: str  # idle, cleaning, error, paused
    battery: int
    mode: str  # vacuum, mop
    current_zone: Optional[str] = None

class MaticBridge:
    def __init__(self):
        self.robots: Dict[str, RobotStatus] = {
            "primary": RobotStatus(
                id="primary",
                state="idle",
                battery=100,
                mode="vacuum"
            )
        }
        self._running = False

    async def start(self):
        self._running = True
        logger.info("Matic Bridge started. Discovering robots...")
        # Simulate discovery delay
        await asyncio.sleep(1)
        logger.info(f"Discovered {len(self.robots)} robots")
        asyncio.create_task(self._simulate_robot_activity())

    async def stop(self):
        self._running = False
        logger.info("Matic Bridge stopped")

    async def get_robot_status(self, robot_id: str) -> Optional[RobotStatus]:
        return self.robots.get(robot_id)

    async def start_cleaning(self, robot_id: str, zone: Optional[str] = None):
        if robot_id in self.robots:
            self.robots[robot_id].state = "cleaning"
            self.robots[robot_id].current_zone = zone or "whole_house"
            logger.info(f"Robot {robot_id} started cleaning {self.robots[robot_id].current_zone}")

    async def stop_cleaning(self, robot_id: str):
        if robot_id in self.robots:
            self.robots[robot_id].state = "idle"
            self.robots[robot_id].current_zone = None
            logger.info(f"Robot {robot_id} stopped cleaning")

    async def pause_cleaning(self, robot_id: str):
        if robot_id in self.robots:
            self.robots[robot_id].state = "paused"
            logger.info(f"Robot {robot_id} paused")

    async def _simulate_robot_activity(self):
        """Simulate battery drain and state changes"""
        while self._running:
            for robot in self.robots.values():
                if robot.state == "cleaning":
                    robot.battery = max(0, robot.battery - 1)
                    if robot.battery < 10:
                        logger.warning(f"Robot {robot.id} low battery! Returning to dock.")
                        robot.state = "idle"
                        robot.battery = 100 # Simulate charging
                elif robot.state == "idle" and robot.battery < 100:
                    robot.battery += 5
            
            await asyncio.sleep(5)

_bridge_instance = None

def get_bridge():
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = MaticBridge()
    return _bridge_instance
