import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

async def seed_gallery():
    # Connect to MongoDB
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client.SalonsClientsDatabase
    gallery_collection = db.gallery
    
    # Clear existing gallery
    await gallery_collection.delete_many({})
    print("🗑️ Cleared existing gallery images")
    
    # Sample gallery data - Black women hairstyles
    gallery_images = [
        {
            "title": "Box Braids with Beads",
            "description": "Stunning medium box braids with colorful beads and accessories",
            "category": "braids",
            "image_url": "https://images.unsplash.com/photo-1605980776566-0486c3ac7617?w=800",
            "stylist_name": "Nia Williams",
            "date_created": datetime(2024, 3, 15),
            "likes": 89,
            "tags": ["box braids", "beads", "protective style"],
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Knotless Braids",
            "description": "Long knotless braids with curly ends",
            "category": "braids",
            "image_url": "https://images.unsplash.com/photo-1614028674026-a65e31bfd27c?w=800",
            "stylist_name": "Tasha Moore",
            "date_created": datetime(2024, 3, 10),
            "likes": 67,
            "tags": ["knotless braids", "long braids", "curly ends"],
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Lace Front Wig Installation",
            "description": "Natural looking lace front wig with baby hairs",
            "category": "wigs",
            "image_url": "https://images.unsplash.com/photo-1588847812172-9bb02cbf0d3a?w=800",
            "stylist_name": "Monique Davis",
            "date_created": datetime(2024, 2, 20),
            "likes": 112,
            "tags": ["lace front", "wig installation", "natural"],
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Fulani Braids",
            "description": "Beautiful Fulani braids with side pattern and beads",
            "category": "braids",
            "image_url": "https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=800",
            "stylist_name": "Nia Williams",
            "date_created": datetime(2024, 2, 25),
            "likes": 94,
            "tags": ["Fulani braids", "pattern", "tribal"],
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Sister Locs",
            "description": "Micro sister locs styled in an updo",
            "category": "locs",
            "image_url": "https://images.unsplash.com/photo-1585079544977-3b9dd32ccf93?w=800",
            "stylist_name": "Imani Clark",
            "date_created": datetime(2024, 1, 18),
            "likes": 76,
            "tags": ["sister locs", "micro locs", "updo"],
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Crochet Braids",
            "description": "Voluminous crochet braids with curly texture",
            "category": "braids",
            "image_url": "https://images.unsplash.com/photo-1585079544977-3b9dd32ccf93?w=800",
            "stylist_name": "Tasha Moore",
            "date_created": datetime(2024, 1, 25),
            "likes": 58,
            "tags": ["crochet braids", "curly", "protective"],
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Custom Wig Unit",
            "description": "Handmade custom wig with silk base",
            "category": "wigs",
            "image_url": "https://images.unsplash.com/photo-1588847812172-9bb02cbf0d3a?w=800",
            "stylist_name": "Monique Davis",
            "date_created": datetime(2024, 2, 5),
            "likes": 143,
            "tags": ["custom wig", "silk base", "handmade"],
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Goddess Braids",
            "description": "Thick goddess braids styled in a crown",
            "category": "braids",
            "image_url": "https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=800",
            "stylist_name": "Nia Williams",
            "date_created": datetime(2023, 12, 10),
            "likes": 82,
            "tags": ["goddess braids", "crown style", "thick braids"],
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Cornrows with Design",
            "description": "Intricate cornrow patterns with curved designs",
            "category": "braids",
            "image_url": "https://images.unsplash.com/photo-1605980776566-0486c3ac7617?w=800",
            "stylist_name": "Tasha Moore",
            "date_created": datetime(2024, 3, 1),
            "likes": 71,
            "tags": ["cornrows", "design", "pattern"],
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Natural Afro",
            "description": "Big beautiful natural afro with pick",
            "category": "natural",
            "image_url": "https://images.unsplash.com/photo-1525877442103-5ddb208b2c2a?w=800",
            "stylist_name": "Imani Clark",
            "date_created": datetime(2024, 2, 28),
            "likes": 156,
            "tags": ["afro", "natural hair", "volume"],
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Twist Out",
            "description": "Defined twist out on natural hair",
            "category": "natural",
            "image_url": "https://images.unsplash.com/photo-1535233141529-17d6ee7cf8c0?w=800",
            "stylist_name": "Nia Williams",
            "date_created": datetime(2024, 3, 5),
            "likes": 63,
            "tags": ["twist out", "natural", "defined curls"],
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Bantu Knots",
            "description": "Traditional Bantu knots on stretched natural hair",
            "category": "natural",
            "image_url": "https://images.unsplash.com/photo-1535233141529-17d6ee7cf8c0?w=800",
            "stylist_name": "Imani Clark",
            "date_created": datetime(2024, 1, 30),
            "likes": 88,
            "tags": ["Bantu knots", "protective", "traditional"],
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Lemonade Braids",
            "description": "Side-swept lemonade braids inspired by Beyoncé",
            "category": "braids",
            "image_url": "https://images.unsplash.com/photo-1614028674026-a65e31bfd27c?w=800",
            "stylist_name": "Tasha Moore",
            "date_created": datetime(2024, 3, 12),
            "likes": 167,
            "tags": ["lemonade braids", "side swept", "Beyoncé"],
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Straight Lace Wig",
            "description": "Sleek straight lace front wig with melt",
            "category": "wigs",
            "image_url": "https://images.unsplash.com/photo-1588847812172-9bb02cbf0d3a?w=800",
            "stylist_name": "Monique Davis",
            "date_created": datetime(2024, 2, 18),
            "likes": 98,
            "tags": ["straight wig", "lace front", "sleek"],
            "is_featured": False,
            "is_active": True
        },
        {
            "title": "Faux Locs",
            "description": "Bohemian faux locs with curly pieces",
            "category": "locs",
            "image_url": "https://images.unsplash.com/photo-1585079544977-3b9dd32ccf93?w=800",
            "stylist_name": "Imani Clark",
            "date_created": datetime(2024, 3, 8),
            "likes": 104,
            "tags": ["faux locs", "bohemian", "curly ends"],
            "is_featured": True,
            "is_active": True
        },
        {
            "title": "Passion Twist",
            "description": "Springy passion twists with curly texture",
            "category": "braids",
            "image_url": "https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=800",
            "stylist_name": "Nia Williams",
            "date_created": datetime(2024, 3, 14),
            "likes": 79,
            "tags": ["passion twists", "springy", "curly"],
            "is_featured": False,
            "is_active": True
        }
    ]
    
    # Insert all images
    result = await gallery_collection.insert_many(gallery_images)
    print(f"✅ Inserted {len(result.inserted_ids)} gallery images")
    
    # Get category counts
    pipeline = [
        {"$match": {"is_active": True}},
        {"$group": {
            "_id": "$category",
            "count": {"$sum": 1}
        }}
    ]
    
    categories = []
    async for cat in gallery_collection.aggregate(pipeline):
        categories.append(f"  - {cat['_id']}: {cat['count']} images")
    
    print("\n📸 Categories seeded:")
    print("\n".join(categories))
    print("\n✨ Black hair gallery data seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_gallery())