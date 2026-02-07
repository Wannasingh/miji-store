import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUBABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUBABASE_URL, SUPABASE_KEY)

def update_hero():
    print("Updating hero banner to high-res...")
    res = supabase.table("hero_banners").update({
        "image_url": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?q=80&w=2070&auto=format&fit=crop",
        "title": "Minimalist <br/> Aesthetics",
        "subtitle": "Elevate your wardrobe with our high-definition essentials. Curated for the modern silhouette."
    }).eq("id", 1).execute()
    print("Update complete:", res.data)

if __name__ == "__main__":
    update_hero()
