import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUBABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUBABASE_URL, SUPABASE_KEY)

def check_db():
    print("Checking Categories...")
    cats = supabase.table("categories").select("*").execute()
    for c in cats.data:
        print(f"Category: {c['name']} (ID: {c['id']})")
    
    print("\nChecking First 5 Products...")
    prods = supabase.table("products").select("name, image_url, category_id").limit(5).execute()
    for p in prods.data:
        print(f"Product: {p['name']} | Image: {p['image_url']} | CatID: {p['category_id']}")

if __name__ == "__main__":
    check_db()
