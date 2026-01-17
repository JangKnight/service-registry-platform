from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class ServiceRegistration(BaseModel):
    name: str
    url: str
    version: str
    health_endpoint: str

app = FastAPI()
services: Dict[str, dict] = {}
platform_start_time = datetime.now()

@app.get("/")
async def read_root():
    return {
        {
        "Documents": "/docs",
        "Endpoints": {
            "Discover": "Use /discover/{name} to find a service by name.",
            "Health": "Use /health to check platform status.",
            "Register": "Use /register (POST) to register a new service.",
            "Deregister": "Use /services/{name} (DELETE) to deregister a service",
            "List Services": "Use /services to list all registered services."
        }
    }
}


@app.get("/discover/{name}")
async def discover_service(name: str):
    if name not in services:
        raise HTTPException(status_code=404, detail=f"Service '{name}' not found")
    return services[name]



@app.get("/health")
async def health_check():
    uptime = (datetime.now() - platform_start_time).total_seconds()
    return{
        "status": "OK",  # OK until data persistence is implemented
        "registered_services": len(services),
        "uptime": f"{uptime} seconds",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/services")
async def list_services():
    return {
        "count": len(services),
        "services": list(services.values())
    }

@app.get("/services/{name}")
async def get_service(name: str):
    if name not in services:
        raise HTTPException(status_code=404, detail=f"Service '{name}' not found")
    return services[name]

@app.post("/register")
async def register(service: ServiceRegistration):
    # if service.name in services:
    #     raise HTTPException(status_code=400, detail="Service already registered")

    if not service.url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    if not service.version:
        raise HTTPException(status_code=400, detail="Version is required")

    if not service.health_endpoint:
        raise HTTPException(status_code=400, detail="Health endpoint is required")

    services[service.name] = {
        "name": service.name,
        "url": service.url,
        "version": service.version,
        "health_endpoint": service.health_endpoint,
        "registered_at": datetime.utcnow().isoformat()
    }
    return {"message": f"Service {service.name} registered successfully."}

@app.delete("/services/{name}")
async def deregister(name: str):
    if name not in services:
        raise HTTPException(status_code=404, detail=f"Service '{name}' not found")
    del services[name]
    return {"message": f"Service {name} deregistered successfully."}


