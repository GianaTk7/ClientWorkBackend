from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# ==================== USER MODEL ====================
class User(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    firebase_uid: Optional[str] = None
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "customer"  # customer, stylist, admin
    is_guest: bool = False
    loyalty_points: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_booking_at: Optional[datetime] = None
    booking_count: int = 0
    
    class Config:
        populate_by_name = True

# ==================== SERVICE MODEL ====================
class Service(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    description: Optional[str] = None
    duration_minutes: int
    price: float
    category: str  # Hair, Nails, Makeup, Skincare
    image_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True

# ==================== STYLIST MODEL ====================
class Stylist(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    user_id: str  # Reference to User
    bio: Optional[str] = None
    specialty: List[str] = []
    profile_image: Optional[str] = None
    is_active: bool = True
    years_experience: Optional[int] = None
    
    class Config:
        populate_by_name = True

# ==================== APPOINTMENT MODEL ====================
class Appointment(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    customer_id: Optional[str] = None  # Null for guest users
    guest_email: Optional[EmailStr] = None
    guest_name: Optional[str] = None
    guest_phone: Optional[str] = None
    stylist_id: str
    service_id: str
    start_time: datetime
    end_time: datetime
    status: str = "confirmed"  # confirmed, completed, cancelled, no_show
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    total_price: float
    reminder_sent: bool = False
    confirmation_code: Optional[str] = None
    
    class Config:
        populate_by_name = True

# ==================== GALLERY MODEL ====================
class GalleryImage(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    title: str
    description: Optional[str] = None
    category: str  # hair, makeup, nails, skincare
    image_url: str
    stylist_name: str
    stylist_id: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow)
    likes: int = 0
    tags: List[str] = []
    is_featured: bool = False
    is_active: bool = True
    
    class Config:
        populate_by_name = True