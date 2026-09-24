import os
import sys
import json
import base64
import time
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from datetime import datetime

# Import card designer
import auto_card_designer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORDERS_DIR = os.path.join(BASE_DIR, "orders")
ORDERS_FILE = os.path.join(BASE_DIR, "orders_db.json")

os.makedirs(ORDERS_DIR, exist_ok=True)
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def load_env():
    env_path = os.path.join(BASE_DIR, ".env")
    env = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

class TapkardServer(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/orders":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                data = f.read()
            self.wfile.write(data.encode("utf-8"))
            return

        # Serve static files from orders/ directory
        if path.startswith("/orders/"):
            super().do_GET()
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")

        try:
            data = json.loads(body) if body else {}
        except Exception:
            data = {}

        if path == "/api/orders/create":
            response = self.handle_create_order(data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))
            return

        if path == "/api/orders/update-status":
            order_id = data.get("order_id")
            new_status = data.get("status")
            success = self.update_order_status(order_id, new_status)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": success}, ensure_ascii=False).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def handle_create_order(self, data):
        order_id = f"TK-{int(time.time())}"
        order_folder = os.path.join(ORDERS_DIR, order_id)
        os.makedirs(order_folder, exist_ok=True)

        name = data.get("name", "ณัฐพงษ์ เจริญทรัพย์")
        title = data.get("title", "Managing Director")
        company = data.get("company", "TAPKARD Enterprise")
        phone = data.get("phone", "081-234-5678")
        line_id = data.get("line_id", "@tapkard")
        email = data.get("email", "contact@tapkard.com")
        theme = data.get("theme", "gold")
        notes = data.get("notes", "")
        customer_address = data.get("address", "")

        # Avatar handle
        avatar_path = None
        avatar_b64 = data.get("avatar_base64")
        if avatar_b64 and "," in avatar_b64:
            avatar_b64 = avatar_b64.split(",", 1)[1]
            avatar_path = os.path.join(order_folder, "avatar_upload.png")
            with open(avatar_path, "wb") as f:
                f.write(base64.b64decode(avatar_b64))

        # Destination URL for NFC
        profile_url = f"https://nattcharoen-beep.github.io/tapkard-nfc-smartcard/profile.html?name={urllib.parse.quote(name)}&title={urllib.parse.quote(title)}&company={urllib.parse.quote(company)}&phone={urllib.parse.quote(phone)}&line={urllib.parse.quote(line_id)}&email={urllib.parse.quote(email)}"

        # Output paths
        f_path = os.path.join(order_folder, "front_print_300dpi.png")
        b_path = os.path.join(order_folder, "back_print_300dpi.png")
        m_path = os.path.join(order_folder, "client_mockup_proof.png")

        # Run auto card designer
        auto_card_designer.create_card_front(name, title, company, avatar_path, theme, f_path)
        auto_card_designer.create_card_back(profile_url, phone, line_id, theme, b_path)
        auto_card_designer.create_mockup_preview(f_path, b_path, m_path)

        # Print Specification Sheet for Print Shop
        spec_content = f"""=====================================================
ใบสั่งพิมพ์สกรีน UV: TAPKARD SMART NFC (Order: {order_id})
=====================================================
วันที่สั่งซื้อ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
ชื่อลูกค้า: {name}
ตำแหน่ง: {title}
บริษัท: {company}
เบอร์โทรศัพท์: {phone}
LINE ID: {line_id}
ที่อยู่จัดส่ง: {customer_address}

สเปกงานพิมพ์:
- ชนิดวัสดุ: บัตรพลาสติก PVC เคลือบด้านสีดำ (Matte Black)
- ขนาดตัดจริง: 85.6 x 54 มม. (มาตรฐานบัตรเครดิต CR80)
- เทคนิคการพิมพ์: UV Flatbed Printing 300 DPI สองหน้า
- หน้าบัตร: ไฟล์ front_print_300dpi.png
- หลังบัตร: ไฟล์ back_print_300dpi.png
- ลิงก์บันทึกลงชิป NFC: {profile_url}
=====================================================
"""
        spec_path = os.path.join(order_folder, "print_spec.txt")
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(spec_content)

        order_record = {
            "order_id": order_id,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "pending_proof", # pending_proof, approved, sent_to_printer, printed, completed
            "customer_name": name,
            "title": title,
            "company": company,
            "phone": phone,
            "line_id": line_id,
            "email": email,
            "address": customer_address,
            "notes": notes,
            "theme": theme,
            "profile_url": profile_url,
            "front_image": f"/orders/{order_id}/front_print_300dpi.png",
            "back_image": f"/orders/{order_id}/back_print_300dpi.png",
            "mockup_image": f"/orders/{order_id}/client_mockup_proof.png",
            "spec_file": f"/orders/{order_id}/print_spec.txt"
        }

        # Save to database
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            orders = json.load(f)
        orders.insert(0, order_record)
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "order_id": order_id,
            "profile_url": profile_url,
            "mockup_url": order_record["mockup_image"],
            "front_url": order_record["front_image"],
            "back_url": order_record["back_image"]
        }

    def update_order_status(self, order_id, new_status):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            orders = json.load(f)
        found = False
        for o in orders:
            if o.get("order_id") == order_id:
                o["status"] = new_status
                found = True
                break
        if found:
            with open(ORDERS_FILE, "w", encoding="utf-8") as f:
                json.dump(orders, f, ensure_ascii=False, indent=2)
        return found

def run():
    env = load_env()
    port = int(env.get("PORT", 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, TapkardServer)
    print(f"🚀 TAPKARD Backend Server running at http://localhost:{port}")
    print(f"📁 Orders stored at: {ORDERS_DIR}")
    print(f"👑 Admin Dashboard: http://localhost:{port}/admin.html")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
