import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# ==================== DATABASE CONNECTION ====================
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.salon_db

# ==================== COLLECTIONS ====================
users_collection = db.users
services_collection = db.services
stylists_collection = db.stylists
appointments_collection = db.appointments
gallery_collection = db.gallery
password_resets_collection = db.password_resets


# ==================== HELPER FUNCTIONS ====================
def get_db():
    return db

def get_users_collection():
    return users_collection

def get_services_collection():
    return services_collection

def get_stylists_collection():
    return stylists_collection

def get_appointments_collection():
    return appointments_collection

def get_gallery_collection():
    return gallery_collection