"""
อัปเดต product ที่ใช้รูป placeholder เป็นรูปไม่ซ้ำ (Picsum seed ตามชื่อสินค้า)
รันครั้งเดียวเพื่อแก้ของเดิมที่รูปซ้ำ/placeholder
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def picsum_url_for_product(name: str, size: int = 400) -> str:
    """รูปไม่ซ้ำต่อชื่อ (Picsum seed จาก hash ชื่อ)."""
    seed = abs(hash(name)) % (10 ** 9)
    return f"https://picsum.photos/seed/{seed}/{size}/{size}"

def main():
    res = supabase.table("products").select("id, name, image_url").execute()
    products = res.data or []
    to_update = [
        p for p in products
        if not p.get("image_url") or "placehold.co" in (p.get("image_url") or "")
    ]
    if not to_update:
        print("No products with placeholder or missing images.")
        return
    print(f"Updating {len(to_update)} products with unique images (Picsum by name)...")
    for p in to_update:
        name = p.get("name") or f"product-{p['id']}"
        new_url = picsum_url_for_product(name)
        try:
            supabase.table("products").update({"image_url": new_url}).eq("id", p["id"]).execute()
        except Exception as e:
            print(f"  Error id {p['id']}: {e}")
    print("Done.")

if __name__ == "__main__":
    main()
