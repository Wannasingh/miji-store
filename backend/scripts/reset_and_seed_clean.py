"""
ร้านแบบ MUJI — ขายเฉพาะ เสื้อผ้า, เฟอร์นิเจอร์, ของใช้ในบ้าน.
Seed จาก 3 แหล่ง: DummyJSON + Fake Store + Platzi (Clothes, Furniture, Shoes) เพื่อให้ได้จำนวนมากขึ้น
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

# เฉพาะหมวด MUJI: เสื้อผ้า, กระเป๋า, นาฬิกา, แว่น, ของแต่งบ้าน, เฟอร์นิเจอร์, โคม — ไม่มีมือถือ/อิเล็กทรอนิกส์
MINIMAL_CATEGORIES = [
    "mens-shirts", "mens-shoes", "mens-watches",
    "womens-dresses", "womens-shoes", "womens-bags", "womens-jewellery",
    "tops", "sunglasses", "home-decoration", "furniture", "lighting",
]

# ตัดรายการที่ชื่อ/คำอธิบายเกี่ยวกับมือถือหรืออิเล็กทรอนิกส์ (แม้ API ส่งมา)
EXCLUDE_KEYWORDS = re.compile(
    r"phone|smartphone|iphone|android|laptop|tablet\s*(pc|computer)?|electronic|computer\s*(keyboard|mouse|monitor)?|"
    r"oppo|samsung\s*(galaxy|phone)|xiaomi|macbook|keyboard|wireless\s*mouse|monitor\s*\d",
    re.I
)

def is_muji_only(p: dict) -> bool:
    """True ถ้าเป็นสินค้าแบบ MUJI (เสื้อผ้า/เฟอร์นิเจอร์/ของใช้) ไม่ใช่มือถือ/อิเล็กทรอนิกส์"""
    name = (p.get("name") or "")
    desc = (p.get("description") or "")
    text = f"{name} {desc}"
    return not bool(EXCLUDE_KEYWORDS.search(text))

async def fetch_dummy_minimal():
    print("Fetching DummyJSON (minimal only)...")
    async with httpx.AsyncClient() as client:
        r = await client.get("https://dummyjson.com/products?limit=194")
        all_p = r.json().get("products", [])
    products = [p for p in all_p if p.get("category") in MINIMAL_CATEGORIES]
    print(f"  {len(products)} products (name+image from same record)")
    return products

async def fetch_fake_store():
    print("Fetching Fake Store API (clothing + jewellery)...")
    all_p = []
    async with httpx.AsyncClient() as client:
        for cat in ["men's clothing", "women's clothing", "jewelery"]:
            slug = cat.replace(" ", "%20")
            try:
                r = await client.get(f"https://fakestoreapi.com/products/category/{slug}")
                if r.status_code == 200:
                    all_p.extend(r.json())
            except Exception as e:
                print(f"  Warning: {e}")
    print(f"  {len(all_p)} products (name+image from same record)")
    return all_p

async def fetch_platzi_muji():
    """Platzi: เอา every product แล้วกรองเฉพาะหมวดที่ไม่ใช่ electronics/phone (API เปลี่ยน id แล้ว)."""
    print("Fetching Platzi API (all non-electronics)...")
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
                    cid = cat.get("id")
                    cname = (cat.get("name") or "").lower()
                    # ไม่เอา electronics, phone
                    if cid in (2, 5):
                        continue
                    if "electronic" in cname or "phone" in cname:
                        continue
                    all_p.append(p)
                if len(data) < 50:
                    break
            except Exception as e:
                print(f"  Warning: {e}")
                break
    print(f"  {len(all_p)} products (name+image from same record)")
    return all_p

def norm_platzi(p):
    imgs = p.get("images") or []
    if isinstance(imgs, str):
        imgs = [imgs] if imgs else []
    main = imgs[0] if imgs else "https://placehold.co/400x400?text=Product"
    cat = (p.get("category") or {}).get("name") or "General"
    return {
        "name": p.get("title", p.get("name", "Product")),
        "description": (p.get("description") or "Quality product.")[:2000],
        "price": float(p.get("price", 0)) or 19.99,
        "image_url": main,
        "category_name": "Apparel" if cat.lower() in ("clothes", "shoes") else "Furniture",
        "images": imgs if len(imgs) > 1 else [main],
    }

def norm_dummy(p):
    main = p["images"][0] if p.get("images") else p.get("thumbnail", "")
    return {
        "name": p["title"],
        "description": p.get("description", ""),
        "price": float(p["price"]),
        "image_url": main,
        "category_name": p["category"].replace("-", " ").title(),
        "images": p.get("images") or [main],
    }

def norm_fake(p):
    img = p.get("image") or ""
    cat = (p.get("category") or "").replace("'", "").title()
    if "men" in cat.lower() or "women" in cat.lower():
        cat = "Apparel"
    elif "jewel" in cat.lower():
        cat = "Accessories"
    return {
        "name": p.get("title", "Product"),
        "description": (p.get("description") or "Quality product.")[:2000],
        "price": float(p.get("price", 0)) or 19.99,
        "image_url": img,
        "category_name": cat,
        "images": [img] if img else [],
    }

async def get_or_create_category(category_name: str):
    slug = category_name.lower().replace(" ", "-").replace("'", "")
    res = supabase.table("categories").select("id").eq("slug", slug).execute()
    if res.data:
        return res.data[0]["id"]
    res = supabase.table("categories").insert({"name": category_name.capitalize(), "slug": slug}).execute()
    return res.data[0]["id"]

async def main():
    print("Clearing existing products (variants, images, products)...")
    try:
        supabase.table("product_variants").delete().neq("id", 0).execute()
        supabase.table("product_images").delete().neq("id", 0).execute()
        supabase.table("products").delete().neq("id", 0).execute()
    except Exception as e:
        print(f"  Note: {e}")
    print("  Done.\n")

    dummy_raw = await fetch_dummy_minimal()
    fake_raw = await fetch_fake_store()
    platzi_raw = await fetch_platzi_muji()
    print(f"  Raw: DummyJSON={len(dummy_raw)}, Fake Store={len(fake_raw)}, Platzi={len(platzi_raw)}")

    combined = (
        [norm_dummy(p) for p in dummy_raw]
        + [norm_fake(p) for p in fake_raw]
        + [norm_platzi(p) for p in platzi_raw]
    )
    seen = set()
    unique = []
    for p in combined:
        key = (p.get("name") or "").strip().lower()
        img = p.get("image_url") or ""
        if not key or key in seen or not img or "placehold" in img:
            continue
        if not is_muji_only(p):
            continue
        seen.add(key)
        unique.append(p)

    print(f"Total to seed (after dedupe + MUJI filter + has image): {len(unique)}\n")

    colors = [("Charcoal", "#333333"), ("Sand", "#C2B280"), ("Midnight", "#191970"), ("Ivory", "#FFFFF0")]
    sizes = ["S", "M", "L", "XL"]

    for i, p in enumerate(unique):
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
                continue
            product_id = prod_res.data[0]["id"]
            imgs = p.get("images") or [p["image_url"]]
            if len(imgs) > 1:
                supabase.table("product_images").insert([
                    {"product_id": product_id, "image_url": u} for u in imgs[1:5]
                ]).execute()
            sel = random.sample(colors, random.randint(1, 2))
            variants = [
                {"product_id": product_id, "color_name": c[0], "color_hex": c[1], "size": s, "stock_quantity": random.randint(0, 50)}
                for c in sel for s in sizes
            ]
            supabase.table("product_variants").insert(variants).execute()
            if (i + 1) % 20 == 0:
                print(f"  Progress: {i+1}/{len(unique)}")
        except Exception as e:
            print(f"  Error product {i}: {e}")

    print(f"\nDone. Seeded {len(unique)} products — ทุกรายการชื่อกับรูปจาก API เดียวกัน (ไม่สุ่ม).")

if __name__ == "__main__":
    asyncio.run(main())
