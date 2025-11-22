import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from matic_hub.config import settings, setup_logging
from matic_hub.logger import logger
from matic_hub.adapters.mqtt_adapter import MqttAdapter
from matic_hub.bridge.matic_bridge import MaticBridge
from matic_hub.adapters.rest_adapter import router as api_router

from matic_hub.bridge.matic_bridge import get_bridge

# Initialize components
bridge = get_bridge()
mqtt_adapter = MqttAdapter(bridge)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting Matic Home Automation Integration Hub")
    
    # Start Bridge
    await bridge.start()
    
    # Start MQTT
    if settings.hub.enable_mqtt:
        await mqtt_adapter.start()
    
    yield
    
    # Shutdown
    await mqtt_adapter.stop()
    await bridge.stop()
    logger.info("Hub stopped")

app = FastAPI(
    title="Matic Home Automation Hub",
    description="Local-first middleware for Matic robots",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router, prefix="/api/v1")

# Mount static files for frontend
try:
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
except Exception:
    logger.warning("Static directory not found, frontend will not be served")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("matic_hub.main:app", host="0.0.0.0", port=8080, reload=True)
