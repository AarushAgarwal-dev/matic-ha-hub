import logging
import sys
from pydantic_settings import BaseSettings
from typing import List, Optional, Dict, Union

class HubSettings(BaseSettings):
    name: str = "Matic Home Hub"
    local_ip: str = "0.0.0.0"
    port: int = 8080
    enable_mqtt: bool = True
    enable_rest_api: bool = True

class MqttSettings(BaseSettings):
    broker_url: str = "mosquitto"
    broker_port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    discovery_prefix: str = "homeassistant"

class RobotSettings(BaseSettings):
    mac_address: str
    ip_address: str
    name: str
    zones: List[Dict[str, Union[str, float]]] = []

class Settings(BaseSettings):
    hub: HubSettings = HubSettings()
    mqtt: MqttSettings = MqttSettings()
    robots: Dict[str, RobotSettings] = {
        "primary": RobotSettings(
            mac_address="AA:BB:CC:DD:EE:FF",
            ip_address="192.168.1.50",
            name="Main Floor Matic",
            zones=[
                {"name": "kitchen", "area": 45},
                {"name": "living_room", "area": 120}
            ]
        )
    }
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

settings = Settings()

def setup_logging():
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
