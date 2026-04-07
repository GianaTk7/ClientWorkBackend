from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from models import Service
from utils.database import get_db
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_services(
    category: Optional[str] = None,
    active_only: bool = True,
    db = Depends(get_db)
):
    """Get all services, optionally filtered by category"""
    query = {}
    if active_only:
        query["is_active"] = True
    if category:
        query["category"] = category
    
    services = []
    cursor = db.services.find(query)
    async for service in cursor:
        service["_id"] = str(service["_id"])
        services.append(service)
    
    return services

@router.get("/{service_id}")
async def get_service(
    service_id: str,
    db = Depends(get_db)
):
    """Get a single service by ID"""
    try:
        service = await db.services.find_one({"_id": ObjectId(service_id)})
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        service["_id"] = str(service["_id"])
        return service
    except:
        raise HTTPException(status_code=400, detail="Invalid service ID")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_service(
    service: Service,
    db = Depends(get_db)
):
    """Create a new service (admin only - will add auth later)"""
    service_dict = service.dict(by_alias=True, exclude={"id"})
    result = await db.services.insert_one(service_dict)
    return {"id": str(result.inserted_id), "message": "Service created successfully"}