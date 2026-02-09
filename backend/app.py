import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Production: ตั้ง CORS_ORIGINS ใน .env (คั่นด้วย comma)
# Development: ไม่ตั้ง = อนุญาตทุก origin
_cors_origins = os.environ.get("CORS_ORIGINS", "").strip()
if _cors_origins:
    CORS(app, origins=[o.strip() for o in _cors_origins.split(",") if o.strip()])
else:
    CORS(app)

# Configure logging to catch intermittent errors
logging.basicConfig(
    filename='backend_errors.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Supabase configuration
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "Flask is running"}), 200

@app.route('/api/hero-banners', methods=['GET'])
def get_hero_banners():
    try:
        response = supabase.table("hero_banners").select("*").eq("is_active", True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        response = supabase.table("categories").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        # Fetch products from 'products' table in Supabase
        # The Python SDK uses HTTPS (Port 443) which should bypass port blockage
        response = supabase.table("products").select("*, categories(name)").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product_detail(id):
    try:
        # Fetch product detail with variants and additional images
        product = supabase.table("products").select("*, categories(name)").eq("id", id).single().execute()
        variants = supabase.table("product_variants").select("*").eq("product_id", id).execute()
        images = supabase.table("product_images").select("*").eq("product_id", id).execute()
        
        return jsonify({
            "product": product.data,
            "variants": variants.data,
            "images": images.data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- Auth (Supabase Auth) ----------
@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    """ล็อกอิน — รับ email, password ส่งคืน token และ user"""
    try:
        data = request.get_json() or {}
        email = data.get("email", "").strip()
        password = data.get("password", "")
        if not email or not password:
            return jsonify({"error": "กรุณากรอกอีเมลและรหัสผ่าน"}), 400
        resp = supabase.auth.sign_in_with_password({"email": email, "password": password})
        session = resp.session
        if not session:
            return jsonify({"error": "ล็อกอินไม่สำเร็จ"}), 401
        return jsonify({
            "token": session.access_token,
            "user": {
                "id": session.user.id,
                "email": session.user.email,
            }
        }), 200
    except Exception as e:
        err = str(e).lower()
        if "invalid" in err or "credentials" in err or "email" in err:
            return jsonify({"error": "อีเมลหรือรหัสผ่านไม่ถูกต้อง"}), 401
        return jsonify({"error": "ล็อกอินไม่สำเร็จ"}), 401


@app.route('/api/auth/signup', methods=['POST'])
def auth_signup():
    """สมัครสมาชิก — รับ email, password, name (optional)"""
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "กรุณาส่ง JSON (Content-Type: application/json)"}), 400
        email = (data.get("email") or "").strip()
        password = (data.get("password") or "")
        name = (data.get("name") or "").strip() or None
        if not email or not password:
            return jsonify({"error": "กรุณากรอกอีเมลและรหัสผ่าน"}), 400
        if len(password) < 6:
            return jsonify({"error": "รหัสผ่านต้องมีอย่างน้อย 6 ตัว"}), 400
        opts = {"email": email, "password": password}
        if name:
            opts["options"] = {"data": {"full_name": name}}
        resp = supabase.auth.sign_up(opts)
        if resp.user and resp.session:
            return jsonify({
                "token": resp.session.access_token,
                "user": {"id": resp.user.id, "email": resp.user.email}
            }), 200
        return jsonify({
            "message": "สมัครสำเร็จ กรุณายืนยันอีเมล (ถ้าเปิดใช้)",
            "user": {"id": resp.user.id, "email": resp.user.email} if resp.user else None
        }), 200
    except Exception as e:
        err = str(e).lower()
        if "already" in err or "registered" in err:
            return jsonify({"error": "อีเมลนี้ถูกใช้งานแล้ว"}), 409
        if "invalid" in err or "email" in err or "format" in err:
            return jsonify({"error": "รูปแบบอีเมลไม่ถูกต้อง"}), 400
        logging.exception("auth_signup failed: %s", e)
        # ส่งข้อความจาก Supabase กลับไปให้ frontend แสดง (เช่น รหัสผ่านสั้นเกินไป)
        return jsonify({"error": str(e) or "สมัครสมาชิกไม่สำเร็จ"}), 400


@app.route('/api/auth/me', methods=['GET'])
def auth_me():
    """ตรวจสอบ token จาก header Authorization: Bearer <token>"""
    try:
        auth = request.headers.get("Authorization") or ""
        if not auth.startswith("Bearer "):
            return jsonify({"error": "ไม่มี token"}), 401
        token = auth[7:].strip()
        if not token:
            return jsonify({"error": "ไม่มี token"}), 401
        try:
            user = supabase.auth.get_user(jwt=token)
        except Exception:
            return jsonify({"error": "token ไม่ถูกต้องหรือหมดอายุ"}), 401
        if not user or not getattr(user, "user", None):
            return jsonify({"error": "token ไม่ถูกต้องหรือหมดอายุ"}), 401
        return jsonify({
            "user": {"id": user.user.id, "email": user.user.email}
        }), 200
    except Exception as e:
        return jsonify({"error": "token ไม่ถูกต้องหรือหมดอายุ"}), 401


if __name__ == '__main__':
    port = int(os.environ.get("FLASK_PORT", 8080))
    # Explicitly enable threading to handle concurrent requests from Home page
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
