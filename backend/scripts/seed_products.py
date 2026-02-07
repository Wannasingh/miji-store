import os
import httpx
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client
import random

load_dotenv()

SUBABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUBABASE_URL, SUPABASE_KEY)

async def fetch_dummy_json_products():
    print("Fetching from DummyJSON (Minimal Categories)...")
    # Specific categories that fit the "Miji/MUJI" minimalist aesthetic
    minimal_categories = [
        "mens-shirts", "mens-shoes", 
        "womens-dresses", "womens-shoes", "womens-bags",
        "home-decoration", "furniture"
    ]
    
    products = []
    async with httpx.AsyncClient() as client:
        # Fetch up to 200 to have more to filter from
        response = await client.get("https://dummyjson.com/products?limit=194")
        all_prods = response.json()["products"]
        products = [p for p in all_prods if p["category"] in minimal_categories]
    return products

async def fetch_platzi_products():
    print("Fetching from Platzi (Clothing/Furniture)...")
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.escuelajs.co/api/v1/products?offset=0&limit=200")
        all_prods = response.json()
        minimal_ids = [1, 3] # Clothes and Furniture
        products = [p for p in all_prods if p["category"]["id"] in minimal_ids]
    return products

async def get_or_create_category(category_name):
    # Normalize category name
    slug = category_name.lower().replace(" ", "-")
    
    # Check if exists
    res = supabase.table("categories").select("id").eq("slug", slug).execute()
    if res.data:
        return res.data[0]["id"]
    
    # Create if not exists
    res = supabase.table("categories").insert({"name": category_name.capitalize(), "slug": slug}).execute()
    return res.data[0]["id"]

async def seed_data():
    # Truncate existing data in correct order of dependency
    print("Clearing existing data...")
    try:
        supabase.table("product_variants").delete().neq("id", 0).execute()
        supabase.table("product_images").delete().neq("id", 0).execute()
        supabase.table("products").delete().neq("id", 0).execute()
        supabase.table("categories").delete().neq("id", 0).execute()
    except Exception as e:
        print(f"Truncation Note: {e}")
    
    # Stick to DummyJSON for guaranteed high quality MUJI-style data
    dummy_products = await fetch_dummy_json_products()
    # Skip Platzi as it contains too much community-vandalized/garbage data
    # platzi_products = await fetch_platzi_products()
    
    combined = []
    
    # Normalize DummyJSON
    for p in dummy_products:
        # Use images[0] if available for better resolution than thumbnail
        main_image = p["images"][0] if p["images"] else p["thumbnail"]
        combined.append({
            "name": p["title"],
            "description": p["description"],
            "price": p["price"],
            "image_url": main_image,
            "category_name": p["category"],
            "images": p["images"]
        })
        
    # Platzi is skipped to ensure high quality data
        
    print(f"Total products to seed: {len(combined)}")
    
    for i, p in enumerate(combined):
        try:
            category_id = await get_or_create_category(p["category_name"])
            
            # Insert Product
            prod_res = supabase.table("products").insert({
                "name": p["name"],
                "description": p["description"],
                "price": p["price"],
                "image_url": p["image_url"],
                "category_id": category_id,
                "is_new_arrival": random.choice([True, False]),
                "is_featured": random.choice([True, False]),
                "is_limited_edition": random.choice([True, False, False, False])
            }).execute()
            
            if prod_res.data:
                product_id = prod_res.data[0]["id"]
                
                # Insert additional images
                if len(p["images"]) > 1:
                    image_rows = [{"product_id": product_id, "image_url": img_url} for img_url in p["images"][1:5]]
                    supabase.table("product_images").insert(image_rows).execute()
                
                # Seed Variants
                variants = []
                colors = [("Charcoal", "#333333"), ("Sand", "#C2B280"), ("Midnight", "#191970"), ("Ivory", "#FFFFF0")]
                sizes = ["S", "M", "L", "XL"]
                
                selected_colors = random.sample(colors, random.randint(1, 2))
                for c_name, c_hex in selected_colors:
                    for s in sizes:
                        variants.append({
                            "product_id": product_id,
                            "color_name": c_name,
                            "color_hex": c_hex,
                            "size": s,
                            "stock_quantity": random.randint(0, 50)
                        })
                supabase.table("product_variants").insert(variants).execute()
                
            if (i+1) % 10 == 0:
                print(f"Progress: {i+1}/{len(combined)}")
                
        except Exception as e:
            print(f"Error seeding product {i}: {e}")

if __name__ == "__main__":
    asyncio.run(seed_data())
