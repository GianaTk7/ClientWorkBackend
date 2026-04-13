from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr
from bson import ObjectId
import os
import secrets
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import resend
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Models import BookingRequest, ForgotPasswordRequest, ResetPasswordRequest

security = HTTPBasic()


# Import from database.py instead of defining here
from utils.database import (
    db,
    users_collection,
    services_collection,
    stylists_collection,
    appointments_collection,
    gallery_collection,
)

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

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

# ==================== BOOKING ENDPOINTS ====================

@app.post("/api/book-appointment")
async def book_appointment(booking: BookingRequest):
    try:
        appointment_datetime = datetime.fromisoformat(f"{booking.appointment_date}T{booking.appointment_time}")
        
        new_appointment = {
            "customer_name": booking.customer_name,
            "customer_email": booking.customer_email,
            "customer_phone": booking.customer_phone,
            "service_name": booking.service_name,
            "start_time": appointment_datetime,
            "status": "confirmed",
            "notes": booking.notes,
            "created_at": datetime.utcnow()
        }
        
        result = await appointments_collection.insert_one(new_appointment)
        
        return {
            "success": True,
            "message": "Appointment booked successfully",
            "appointment_id": str(result.inserted_id)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "esthermusa@gmail.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "esther123")

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_EMAIL or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


@app.get("/api/admin/appointments")
async def get_admin_appointments(auth: bool = Depends(verify_admin)):
    appointments = []
    cursor = appointments_collection.find().sort("created_at", -1)
    async for apt in cursor:
        apt["_id"] = str(apt["_id"])
        appointments.append(apt)
    return {"appointments": appointments}

@app.put("/api/admin/appointments/{appointment_id}/status")
async def update_appointment_status(appointment_id: str, status: str, auth: bool = Depends(verify_admin)):
    try:
        await appointments_collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"status": status}}
        )
        return {"success": True, "message": "Status updated"}
    except:
        raise HTTPException(status_code=400, detail="Invalid appointment ID")

@app.delete("/api/admin/appointments/{appointment_id}")
async def delete_appointment(appointment_id: str, auth: bool = Depends(verify_admin)):
    try:
        await appointments_collection.delete_one({"_id": ObjectId(appointment_id)})
        return {"success": True, "message": "Appointment deleted"}
    except:
        raise HTTPException(status_code=400, detail="Invalid appointment ID")


@app.put("/api/admin/appointments/{appointment_id}/status")
async def update_appointment_status(appointment_id: str, status: str, auth: bool = Depends(verify_admin)):
    try:
        await appointments_collection.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"status": status}}
        )
        return {"success": True, "message": "Status updated"}
    except:
        raise HTTPException(status_code=400, detail="Invalid appointment ID")

@app.delete("/api/admin/appointments/{appointment_id}")
async def delete_appointment(appointment_id: str, auth: bool = Depends(verify_admin)):
    try:
        await appointments_collection.delete_one({"_id": ObjectId(appointment_id)})
        return {"success": True, "message": "Appointment deleted"}
    except:
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
    
def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_EMAIL or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return True

def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:3000/reset-password?token={token}"
    
    # Use Gmail SMTP (free)
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # Gmail app password
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = "Reset Your Admin Password"
    
    body = f"Reset your password here: {reset_link}\n\nThis link expires in 1 hour."
    msg.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except:
        return False
async def forgot_password(request: ForgotPasswordRequest):
    if request.email != ADMIN_EMAIL:
        raise HTTPException(status_code=404, detail="Email not found")
    
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    await password_resets_collection.update_one(
        {"email": request.email},
        {"$set": {"token": token, "expires_at": expires_at}},
        upsert=True
    )
    
    try:
        send_reset_email(request.email, token)
        return {"success": True, "message": "Reset link sent to your email"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send email")

@app.post("/api/admin/reset-password")
async def reset_password(request: ResetPasswordRequest):
    reset_record = await password_resets_collection.find_one({
        "token": request.token,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    
    if not reset_record:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    global ADMIN_PASSWORD
    ADMIN_PASSWORD = request.new_password
    
    import os
    env_path = ".env"
    with open(env_path, "r") as f:
        lines = f.readlines()
    
    with open(env_path, "w") as f:
        for line in lines:
            if line.startswith("ADMIN_PASSWORD="):
                f.write(f"ADMIN_PASSWORD={request.new_password}\n")
            else:
                f.write(line)
    
    await password_resets_collection.delete_many({"email": reset_record["email"]})
    
    return {"success": True, "message": "Password reset successfully"}