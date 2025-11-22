import asyncio
import json
import logging
import paho.mqtt.client as mqtt
from matic_hub.config import settings
from matic_hub.bridge.matic_bridge import MaticBridge

logger = logging.getLogger(__name__)

class MqttAdapter:
    def __init__(self, bridge: MaticBridge):
        self.bridge = bridge
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        if settings.mqtt.username:
            self.client.username_pw_set(settings.mqtt.username, settings.mqtt.password)

    async def start(self):
        logger.info(f"Connecting to MQTT Broker at {settings.mqtt.broker_url}:{settings.mqtt.broker_port}")
        try:
            self.client.connect(settings.mqtt.broker_url, settings.mqtt.broker_port, 60)
            self.client.loop_start()
            asyncio.create_task(self._publish_status_loop())
        except Exception as e:
            logger.error(f"Failed to connect to MQTT: {e}")

    async def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected to MQTT Broker with result code {rc}")
        # Subscribe to commands
        client.subscribe("matic/robots/+/commands/#")
        self._publish_discovery()

    def on_message(self, client, userdata, msg):
        topic_parts = msg.topic.split("/")
        if len(topic_parts) < 5:
            return
        
        robot_id = topic_parts[2]
        command = topic_parts[4]
        payload = msg.payload.decode()
        
        logger.info(f"Received MQTT command: {command} for {robot_id}")
        
        # Handle commands asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        if command == "start":
            asyncio.run(self.bridge.start_cleaning(robot_id))
        elif command == "stop":
            asyncio.run(self.bridge.stop_cleaning(robot_id))
        elif command == "pause":
            asyncio.run(self.bridge.pause_cleaning(robot_id))
        elif command == "zone":
            asyncio.run(self.bridge.start_cleaning(robot_id, zone=payload))

    def _publish_discovery(self):
        """Publish Home Assistant Discovery Config"""
        for robot_id, robot_config in settings.robots.items():
            discovery_topic = f"{settings.mqtt.discovery_prefix}/vacuum/matic_{robot_id}/config"
            payload = {
                "name": robot_config.name,
                "unique_id": f"matic_{robot_id}",
                "command_topic": f"matic/robots/{robot_id}/commands/start",
                "state_topic": f"matic/robots/{robot_id}/status",
                "battery_level_topic": f"matic/robots/{robot_id}/battery",
                "send_command_topic": f"matic/robots/{robot_id}/commands/custom",
                "device": {
                    "identifiers": [f"matic_{robot_id}"],
                    "name": robot_config.name,
                    "manufacturer": "Matic",
                    "model": "Matic Robot"
                }
            }
            self.client.publish(discovery_topic, json.dumps(payload), retain=True)

    async def _publish_status_loop(self):
        while True:
            for robot_id in settings.robots.keys():
                status = await self.bridge.get_robot_status(robot_id)
                if status:
                    self.client.publish(f"matic/robots/{robot_id}/status", status.state)
                    self.client.publish(f"matic/robots/{robot_id}/battery", str(status.battery))
                    self.client.publish(f"matic/robots/{robot_id}/mode", status.mode)
                    if status.current_zone:
                        self.client.publish(f"matic/robots/{robot_id}/location", status.current_zone)
            await asyncio.sleep(5)
