"""
ลบ product ที่ชื่อซ้ำใน DB — เก็บเฉพาะรายการแรก (id น้อยสุด) ของแต่ละชื่อ
รันครั้งเดียวหลังมีของซ้ำ แล้วค่อย seed/add ใหม่
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    print("Fetching all products...")
    res = supabase.table("products").select("id, name").order("id").execute()
    rows = res.data or []
    if not rows:
        print("No products found.")
        return

    # หาชื่อซ้ำ: เก็บ id แรกของแต่ละชื่อ, ที่เหลือเป็น id ที่จะลบ
    by_name = {}
    for r in rows:
        name_key = (r.get("name") or "").strip().lower()
        if not name_key:
            continue
        if name_key not in by_name:
            by_name[name_key] = []
        by_name[name_key].append(r["id"])

    to_delete = []
    for name_key, ids in by_name.items():
        if len(ids) > 1:
            to_delete.extend(ids[1:])  # เก็บ id แรก, ลบที่เหลือ

    if not to_delete:
        print("No duplicate product names found.")
        return

    print(f"Found {len(to_delete)} duplicate product(s) to remove (keeping first of each name).")

    # ลบ product — DB มี on delete cascade อยู่แล้ว จะลบ variants/images ให้เอง
    for pid in to_delete:
        try:
            supabase.table("products").delete().eq("id", pid).execute()
        except Exception as e:
            print(f"  Error deleting product id {pid}: {e}")

    print(f"Removed {len(to_delete)} duplicate products.")

if __name__ == "__main__":
    main()
