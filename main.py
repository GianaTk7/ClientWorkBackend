from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
import os
from dotenv import load_dotenv

# Import from database.py instead of defining here
from utils.database import (
    db,
    users_collection,
    services_collection,
    stylists_collection,
    appointments_collection,
    gallery_collection,
    get_db,
    get_users_collection,
    get_services_collection,
    get_stylists_collection,
    get_appointments_collection,
    get_gallery_collection
)

load_dotenv()

# ==================== PYDANTIC MODELS ====================
class BookingRequest(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    stylist_id: str
    service_id: str
    appointment_date: str  # ISO format date
    appointment_time: str  # HH:MM format
    notes: Optional[str] = None

class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    duration_minutes: int
    price: float
    category: str
    image_url: Optional[str] = None

# ==================== FASTAPI APP ====================
app = FastAPI(
    title="Salon Booking API",
    description="API for salon appointment booking system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "https://your-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ROOT ENDPOINTS ====================
@app.get("/")
async def root():
    return {
        "message": "Salon Booking API",
        "status": "running",
        "version": "1.0.0",
        "collections": {
            "users": "users_collection",
            "services": "services_collection",
            "stylists": "stylists_collection",
            "appointments": "appointments_collection",
            "gallery": "gallery_collection"
        }
    }

@app.get("/health")
async def health_check():
    try:
        await db.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    return {"status": "healthy", "timestamp": datetime.utcnow(), "database": db_status}

# ==================== SERVICES ENDPOINTS ====================
@app.get("/api/services")
async def get_services(category: Optional[str] = None):
    """Get all services"""
    query = {"is_active": True}
    if category:
        query["category"] = category
    
    services = []
    cursor = services_collection.find(query)
    async for service in cursor:
        service["_id"] = str(service["_id"])
        services.append(service)
    
    return services

@app.get("/api/services/{service_id}")
async def get_service(service_id: str):
    """Get service by ID"""
    try:
        service = await services_collection.find_one({"_id": ObjectId(service_id)})
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        service["_id"] = str(service["_id"])
        return service
    except:
        raise HTTPException(status_code=400, detail="Invalid service ID")

# ==================== STYLISTS ENDPOINTS ====================
@app.get("/api/stylists")
async def get_stylists():
    """Get all stylists"""
    stylists = []
    cursor = stylists_collection.find({"is_active": True})
    
    async for stylist in cursor:
        stylist["_id"] = str(stylist["_id"])
        stylist["user_id"] = str(stylist["user_id"])
        stylists.append(stylist)
    
    return stylists

@app.get("/api/stylists/{stylist_id}")
async def get_stylist(stylist_id: str):
    """Get stylist by ID"""
    try:
        stylist = await stylists_collection.find_one({"_id": ObjectId(stylist_id)})
        if not stylist:
            raise HTTPException(status_code=404, detail="Stylist not found")
        
        stylist["_id"] = str(stylist["_id"])
        stylist["user_id"] = str(stylist["user_id"])
        
        return stylist
    except:
        raise HTTPException(status_code=400, detail="Invalid stylist ID")

@app.get("/api/stylists/{stylist_id}/availability")
async def get_stylist_availability(
    stylist_id: str,
    date: str
):
    """Get available time slots for a stylist on a specific date"""
    try:
        target_date = datetime.fromisoformat(date).date()
        
        # Working hours: 9 AM - 6 PM, 30-minute slots
        working_hours = {"start": 9, "end": 18, "slot_duration": 30}
        
        start_of_day = datetime.combine(target_date, datetime.min.time())
        end_of_day = datetime.combine(target_date, datetime.max.time())
        
        # Get existing appointments for this stylist on this date
        booked_slots = []
        cursor = appointments_collection.find({
            "stylist_id": stylist_id,
            "start_time": {"$gte": start_of_day, "$lte": end_of_day},
            "status": {"$in": ["confirmed", "pending"]}
        })
        
        async for apt in cursor:
            booked_slots.append({
                "start": apt["start_time"],
                "end": apt["end_time"]
            })
        
        # Generate available slots
        available_slots = []
        current_time = datetime.combine(target_date, datetime.min.time().replace(hour=working_hours["start"]))
        end_time = datetime.combine(target_date, datetime.min.time().replace(hour=working_hours["end"]))
        
        while current_time < end_time:
            slot_end = current_time + timedelta(minutes=working_hours["slot_duration"])
            
            is_available = True
            for booked in booked_slots:
                if current_time < booked["end"] and slot_end > booked["start"]:
                    is_available = False
                    break
            
            if is_available:
                available_slots.append(current_time.strftime("%H:%M"))
            
            current_time += timedelta(minutes=working_hours["slot_duration"])
        
        return {"available_slots": available_slots}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# ==================== BOOKING ENDPOINTS ====================
@app.post("/api/book-appointment")
async def book_appointment(booking: BookingRequest):
    """Book an appointment (no login required)"""
    
    try:
        # Validate service exists
        service = await services_collection.find_one({"_id": ObjectId(booking.service_id)})
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        # Validate stylist exists
        stylist = await stylists_collection.find_one({"_id": ObjectId(booking.stylist_id)})
        if not stylist:
            raise HTTPException(status_code=404, detail="Stylist not found")
        
        # Combine date and time
        appointment_datetime = datetime.fromisoformat(f"{booking.appointment_date}T{booking.appointment_time}")
        end_datetime = appointment_datetime + timedelta(minutes=service["duration_minutes"])
        
        # Check if time slot is already booked
        existing = await appointments_collection.find_one({
            "stylist_id": booking.stylist_id,
            "status": {"$in": ["confirmed", "pending"]},
            "$or": [
                {"start_time": {"$lt": end_datetime, "$gte": appointment_datetime}},
                {"end_time": {"$gt": appointment_datetime, "$lte": end_datetime}}
            ]
        })
        
        if existing:
            raise HTTPException(status_code=409, detail="Time slot already booked. Please choose another time.")
        
        # Create appointment
        new_appointment = {
            "customer_name": booking.customer_name,
            "customer_email": booking.customer_email,
            "customer_phone": booking.customer_phone,
            "stylist_id": booking.stylist_id,
            "stylist_name": stylist.get("name", "Stylist"),
            "service_id": booking.service_id,
            "service_name": service["name"],
            "service_price": service["price"],
            "start_time": appointment_datetime,
            "end_time": end_datetime,
            "status": "confirmed",
            "notes": booking.notes,
            "total_price": service["price"],
            "created_at": datetime.utcnow()
        }
        
        result = await appointments_collection.insert_one(new_appointment)
        
        return {
            "success": True,
            "message": "Appointment booked successfully!",
            "appointment_id": str(result.inserted_id),
            "appointment_details": {
                "customer_name": booking.customer_name,
                "service": service["name"],
                "stylist": stylist.get("name", "Stylist"),
                "date": booking.appointment_date,
                "time": booking.appointment_time,
                "total_price": service["price"]
            }
        }
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail=f"Booking failed: {str(e)}")

@app.get("/api/appointments/lookup")
async def lookup_appointment(email: str, phone: Optional[str] = None):
    """Look up appointments by email (no login required)"""
    
    query = {"customer_email": email}
    if phone:
        query["customer_phone"] = phone
    
    appointments = []
    cursor = appointments_collection.find(query).sort("start_time", -1)
    
    async for apt in cursor:
        apt["_id"] = str(apt["_id"])
        apt["stylist_id"] = str(apt["stylist_id"])
        apt["service_id"] = str(apt["service_id"])
        appointments.append(apt)
    
    return {"appointments": appointments}

@app.put("/api/appointments/{appointment_id}/cancel")
async def cancel_appointment(appointment_id: str, email: str):
    """Cancel an appointment using email verification"""
    
    try:
        # Find appointment by ID and email
        appointment = await appointments_collection.find_one({
            "_id": ObjectId(appointment_id),
            "customer_email": email
        })
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found or email doesn't match")
        
        # Check if appointment is in the past
        if appointment["start_time"] < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Cannot cancel past appointments")
        
        # Cancel appointment
        await appointments_collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"status": "cancelled"}}
        )
        
        return {"success": True, "message": "Appointment cancelled successfully"}
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail="Invalid appointment ID")

# ==================== GALLERY ENDPOINTS ====================
@app.post("/api/gallery/{image_id}/like")
async def like_gallery_image(image_id: str):
    """Increment likes count for a gallery image"""
    try:
        result = await gallery_collection.update_one(
            {"_id": ObjectId(image_id), "is_active": True},
            {"$inc": {"likes": 1}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Image not found or inactive")
        
        # Return updated image
        image = await gallery_collection.find_one({"_id": ObjectId(image_id)})
        image["_id"] = str(image["_id"])
        return {"message": "Image liked successfully", "likes": image["likes"]}
    
    except:
        raise HTTPException(status_code=400, detail="Invalid image ID")
@app.get("/api/gallery/categories")
async def get_gallery_categories():
    """Get all unique categories with image counts"""
    
    pipeline = [
        {"$match": {"is_active": True}},
        {"$group": {
            "_id": "$category",
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    
    cursor = gallery_collection.aggregate(pipeline)
    categories = []
    async for cat in cursor:
        categories.append({
            "name": cat["_id"],
            "count": cat["count"]
        })
    
    # Add "all" category
    total = await gallery_collection.count_documents({"is_active": True})
    categories.insert(0, {"name": "all", "count": total})
    
    return categories

@app.get("/api/gallery")
async def get_gallery_images(
    category: Optional[str] = Query(None, description="Filter by category"),
    featured_only: bool = Query(False, description="Show only featured images"),
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """Get all gallery images from database"""
    
    # Build query
    query = {"is_active": True}
    if category and category != "all":
        query["category"] = category
    if featured_only:
        query["is_featured"] = True
    
    # Get total count
    total = await gallery_collection.count_documents(query)
    
    # Get images with pagination
    cursor = gallery_collection.find(query).sort("date_created", -1).skip(skip).limit(limit)
    
    images = []
    async for image in cursor:
        image["_id"] = str(image["_id"])
        images.append(image)
    
    return {
        "images": images,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@app.get("/api/gallery/{image_id}")
async def get_gallery_image(image_id: str):
    """Get a single gallery image by ID"""
    try:
        image = await gallery_collection.find_one({"_id": ObjectId(image_id), "is_active": True})
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        image["_id"] = str(image["_id"])
        return image
    except:
        raise HTTPException(status_code=400, detail="Invalid image ID")