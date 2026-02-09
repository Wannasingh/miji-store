"""
ร้านแบบ MUJI — ขายเฉพาะ เสื้อผ้า, เฟอร์นิเจอร์, ของใช้ในบ้าน.
เพิ่มจาก DummyJSON + Fake Store + Platzi (Clothes, Furniture, Shoes) ชื่อกับรูปจาก record เดียวกัน
"""
import os
import re
import httpx
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client
import random

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# เฉพาะหมวด MUJI: เสื้อผ้า, กระเป๋า, นาฬิกา, แว่น, ของแต่งบ้าน, เฟอร์นิเจอร์, โคม
MINIMAL_CATEGORIES = [
    "mens-shirts",
    "mens-shoes",
    "mens-watches",
    "womens-dresses",
    "womens-shoes",
    "womens-bags",
    "womens-jewellery",
    "tops",
    "sunglasses",
    "home-decoration",
    "furniture",
    "lighting",
]

EXCLUDE_KEYWORDS = re.compile(
    r"phone|smartphone|iphone|android|laptop|tablet\s*(pc|computer)?|electronic|computer\s*(keyboard|mouse|monitor)?|"
    r"oppo|samsung\s*(galaxy|phone)|xiaomi|macbook|keyboard|wireless\s*mouse|monitor\s*\d",
    re.I
)

def is_muji_only(p: dict) -> bool:
    """True ถ้าเป็นสินค้าแบบ MUJI ไม่ใช่มือถือ/อิเล็กทรอนิกส์"""
    name = (p.get("name") or "")
    desc = (p.get("description") or "")
    return not bool(EXCLUDE_KEYWORDS.search(f"{name} {desc}"))

async def fetch_dummy_json_minimal_only():
    """Fetch only minimal categories from DummyJSON (no groceries, veggies, etc.)."""
    print("Fetching from DummyJSON (minimal categories only)...")
    async with httpx.AsyncClient() as client:
        response = await client.get("https://dummyjson.com/products?limit=194")
        data = response.json()
        all_prods = data.get("products", [])
    products = [p for p in all_prods if p.get("category") in MINIMAL_CATEGORIES]
    print(f"  Found {len(products)} minimal products (excluded groceries, skincare, etc.)")
    return products

def normalize_dummy(p):
    """Normalize DummyJSON product to our format."""
    main_image = p["images"][0] if p.get("images") else p.get("thumbnail", "")
    return {
        "name": p["title"],
        "description": p.get("description", ""),
        "price": float(p["price"]),
        "image_url": main_image,
        "category_name": p["category"].replace("-", " ").title(),
        "images": p.get("images") or [main_image],
    }

# Fake Store API — มีรูปสินค้าจริงทุกรายการ (men/women clothing, jewellery)
FAKE_STORE_CATEGORIES = ["men's clothing", "women's clothing", "jewelery"]

async def fetch_fake_store_products():
    """Fetch from Fake Store API (real product images)."""
    print("Fetching from Fake Store API (real images)...")
    all_products = []
    async with httpx.AsyncClient() as client:
        for cat in FAKE_STORE_CATEGORIES:
            slug = cat.replace(" ", "%20")
            try:
                r = await client.get(f"https://fakestoreapi.com/products/category/{slug}")
                if r.status_code == 200:
                    data = r.json()
                    all_products.extend(data)
            except Exception as e:
                print(f"  Warning: {cat} — {e}")
    print(f"  Found {len(all_products)} products with real images")
    return all_products

def normalize_fake_store(p):
    """Normalize Fake Store product (has 'image' URL)."""
    img = p.get("image") or ""
    cat = (p.get("category") or "general").replace("'", "").title()
    if "men" in cat.lower():
        cat = "Apparel"
    elif "women" in cat.lower():
        cat = "Apparel"
    elif "jewel" in cat.lower():
        cat = "Accessories"
    return {
        "name": p.get("title", "Product"),
        "description": p.get("description", "") or "Quality product.",
        "price": float(p.get("price", 0)) or 19.99,
        "image_url": img,
        "category_name": cat,
        "images": [img] if img else [],
    }

async def fetch_platzi_muji():
    """Platzi: เอาทุกหมวดที่ไม่ใช่ electronics/phone (API เปลี่ยน id แล้ว)."""
    print("Fetching from Platzi API (all non-electronics)...")
    all_p = []
    async with httpx.AsyncClient() as client:
        for offset in range(0, 400, 50):
            try:
                r = await client.get(f"https://api.escuelajs.co/api/v1/products?offset={offset}&limit=50")
                if r.status_code != 200:
                    break
                data = r.json()
                for p in data:
                    cat = p.get("category") or {}
                    cid, cname = cat.get("id"), (cat.get("name") or "").lower()
                    if cid in (2, 5) or "electronic" in cname or "phone" in cname:
                        continue
                    all_p.append(p)
                if len(data) < 50:
                    break
            except Exception as e:
                print(f"  Warning: {e}")
                break
    print(f"  Found {len(all_p)} products")
    return all_p

def normalize_platzi(p):
    imgs = p.get("images") or []
    if isinstance(imgs, str):
        imgs = [imgs] if imgs else []
    main = imgs[0] if imgs else ""
    cat = (p.get("category") or {}).get("name") or "General"
    return {
        "name": p.get("title", p.get("name", "Product")),
        "description": (p.get("description") or "Quality product.")[:2000],
        "price": float(p.get("price", 0)) or 19.99,
        "image_url": main,
        "category_name": "Apparel" if str(cat).lower() in ("clothes", "shoes") else "Furniture",
        "images": imgs if len(imgs) > 1 else [main],
    }

async def get_existing_product_names():
    """Get all product names already in DB to avoid duplicates."""
    res = supabase.table("products").select("name").execute()
    return {row["name"].strip().lower() for row in (res.data or []) if row.get("name")}

async def get_or_create_category(category_name: str):
    slug = category_name.lower().replace(" ", "-").replace("'", "")
    res = supabase.table("categories").select("id").eq("slug", slug).execute()
    if res.data:
        return res.data[0]["id"]
    res = supabase.table("categories").insert({
        "name": category_name.capitalize(),
        "slug": slug,
    }).execute()
    return res.data[0]["id"]

async def insert_one_product(p: dict, index: int, existing_names: set) -> bool:
    """Insert one product (skip if name already exists). Returns True if inserted."""
    name_key = (p.get("name") or "").strip().lower()
    if name_key in existing_names:
        return False
    try:
        category_id = await get_or_create_category(p["category_name"])
        prod_res = supabase.table("products").insert({
            "name": p["name"],
            "description": (p["description"] or "")[:2000],
            "price": p["price"],
            "image_url": p["image_url"],
            "category_id": category_id,
            "is_new_arrival": random.choice([True, False]),
            "is_featured": random.choice([True, False]),
            "is_limited_edition": random.choice([True, False, False, False]),
        }).execute()

        if not prod_res.data:
            return False

        product_id = prod_res.data[0]["id"]
        images = p.get("images") or [p["image_url"]]
        if len(images) > 1:
            rows = [{"product_id": product_id, "image_url": u} for u in images[1:5]]
            supabase.table("product_images").insert(rows).execute()

        colors = [
            ("Charcoal", "#333333"),
            ("Sand", "#C2B280"),
            ("Midnight", "#191970"),
            ("Ivory", "#FFFFF0"),
        ]
        sizes = ["S", "M", "L", "XL"]
        selected = random.sample(colors, random.randint(1, 2))
        variants = []
        for c_name, c_hex in selected:
            for s in sizes:
                variants.append({
                    "product_id": product_id,
                    "color_name": c_name,
                    "color_hex": c_hex,
                    "size": s,
                    "stock_quantity": random.randint(0, 50),
                })
        supabase.table("product_variants").insert(variants).execute()

        if (index + 1) % 50 == 0:
            print(f"  Progress: {index + 1}...")
        existing_names.add(name_key)
        return True
    except Exception as e:
        print(f"  Error at index {index}: {e}")
        return False

async def main():
    dummy_raw = await fetch_dummy_json_minimal_only()
    fake_raw = await fetch_fake_store_products()
    platzi_raw = await fetch_platzi_muji()
    dummy_norm = [normalize_dummy(p) for p in dummy_raw]
    fake_norm = [normalize_fake_store(p) for p in fake_raw]
    platzi_norm = [normalize_platzi(p) for p in platzi_raw]
    combined = dummy_norm + fake_norm + platzi_norm
    # ลบชื่อซ้ำ + ตัดมือถือ/อิเล็กทรอนิกส์ — เหลือเฉพาะแบบ MUJI
    seen = set()
    unique_norm = []
    for p in combined:
        key = (p["name"] or "").strip().lower()
        if not key or key in seen or not p.get("image_url"):
            continue
        if not is_muji_only(p):
            continue
        if "placehold" in (p.get("image_url") or ""):
            continue
        seen.add(key)
        unique_norm.append(p)
    existing_names = await get_existing_product_names()
    to_insert = [p for p in unique_norm if (p.get("name") or "").strip().lower() not in existing_names]

    print(f"From APIs: {len(unique_norm)} unique. In DB: {len(existing_names)}. To add: {len(to_insert)} (name+image matched only)")

    added = 0
    for i, p in enumerate(to_insert):
        if await insert_one_product(p, i, existing_names):
            added += 1

    print(f"Done. Added {added} new products (name+image from API only, no random/synthetic).")

if __name__ == "__main__":
    asyncio.run(main())
