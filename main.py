from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import Service as ServiceModel
from logger import logger

class ServiceRegistration(BaseModel):
    name: str
    url: str
    version: str
    health_endpoint: str


app = FastAPI()
platform_start_time = datetime.now()
# services: Dict[str, dict] = {}

@app.get("/")
async def read_root():
    return RedirectResponse(url="/docs")


@app.get("/discover/{name}")
async def discover_service(name: str, db: Session = Depends(get_db)):
    """Get a specific service from database"""
    
    logger.info(
        "Service discovery request received",
        service_name=name,
        endpoint="/discover"
    )
    
    service = db.query(ServiceModel).filter(ServiceModel.name == name).first()
    
    if not service:
        logger.warning(
            "Service not found",
            service_name=name,
            endpoint="/discover"
        )
        raise HTTPException(
            status_code=404,
            detail=f"Service '{name}' not found in registry"
        )
    logger.info(
        "Service discovered",
        service_name=name,
        endpoint="/discover"
    )
    return service.to_dict()



@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Platform health check with database connection test"""
    try:

        service_count = db.query(ServiceModel).count()
        uptime_seconds = (datetime.now() - platform_start_time).total_seconds()

        logger.debug(
            "Health check passed",
            service_count=service_count,
            uptime_seconds=uptime_seconds
        )

        return {
            "status": "healthy",
            "registered_services": service_count,
            "uptime_seconds": uptime_seconds,
            "timestamp": datetime.now().isoformat(),
            "database": "connected"
        }
    except Exception as e:
        logger.error(
            "Health check failed - database connection error",
            error=str(e),
            error_type=type(e).__name__
        )

        return {
            "status": "unhealthy",
            "error": "Database connection failed",
            "database": "disconnected"
        }

@app.get("/services")
async def list_services(db: Session = Depends(get_db)):
    """List all registered services from database"""
    logger.info("Service list requested", endpoint="/services")

    try:
        services = db.query(ServiceModel).all()
        logger.info(
                "Service list returned",
                count=len(services),
                endpoint="/services"
        )
        return {
            "count": len(services),
            "services": (service.to_dict() for service in services)
        }
    except Exception as e:
        logger.error(
            "Failed to retrieve service list",
            error=str(e),
            error_type=type(e).__name__
        )
        raise

@app.get("/services/{name}")
async def get_service(name: str, db: Session = Depends(get_db)):
    """Get a specific service from database"""

    logger.info(
        "Service discovery request received",
        service_name=name,
        endpoint="/services (discover)"
    )

    service = db.query(ServiceModel).filter(ServiceModel.name == name).first()
    if not service:
        logger.warning(
            "Service not found",
            service_name=name,
            endpoint="/services (discover)"
        )
        raise HTTPException(
            status_code=404,
            detail=f"Service '{name}' not found in registry"
        )

    logger.info(
        "Service discovered",
        service_name=name,
        endpoint="/services (discover)"
    )
    return service.to_dict()


@app.post("/register")
async def register(service: ServiceRegistration, db: Session = Depends(get_db)):
    """Register a new service in the database"""
    logger.info(
        f"Registering service: {service.name}",
        url=service.url,
        version=service.version,
        endpoint="/register"
    )
    try:
        existing = db.query(ServiceModel).filter(ServiceModel.name == service.name).first()
        if existing:
            existing.url = service.url
            existing.version = service.version
            existing.health_endpoint = service.health_endpoint
            existing.registered_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return {
                "message": "Service updated successfully",
                "service": service.name
            }
        else:
            new_service = ServiceModel(
                name=service.name,
                url=service.url,
                version=service.version,
                health_endpoint=service.health_endpoint,
                registered_at=datetime.utcnow()
            )
            db.add(new_service)
            db.commit()
            db.refresh(new_service)
            return {
                "message": "Service registered successfully",
                "service": service.name
            }
    except Exception as e:
        logger.error(
            "Service registration failed",
            service_name=service.name,
            error=str(e),
            error_type=type(e).__name__
        )
        raise

@app.delete("/services/{name}")
async def deregister(name: str, db: Session = Depends(get_db)):
    """Deregister a service from database"""
    service = db.query(ServiceModel).filter(ServiceModel.name == name).first()

    if not service:
        logger.warning(
            "Cannot deregister - service not found",
            service_name=name
        )
        raise HTTPException(
            status_code=404,
            detail=f"Service '{name}' not found"
        )

    db.delete(service)
    db.commit()

    logger.info(
        "Service deregistered successfully",
        service_name=name
    )

    return {"message": f"Service {name} deregistered successfully."}


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up service registry platform",
                ver="1.0.0 ",
                db="postgresql"
        )

    try:
        from database import init_db
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down service registry platform")