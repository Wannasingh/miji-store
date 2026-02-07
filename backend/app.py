import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

app = Flask(__name__)
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

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_PORT", 8080))
    # Explicitly enable threading to handle concurrent requests from Home page
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
