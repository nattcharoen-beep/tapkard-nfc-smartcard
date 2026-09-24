# 🚀 TAPKARD™ — Smart NFC Business Card & Google Review Stand

ระบบเว็บไซต์ครบวงจรสำหรับธุรกิจ **นามบัตรดิจิทัลอัจฉริยะ (Smart NFC Business Card)** และ **ป้ายแตะรีวิว Google Maps 5 ดาว (Google Review Tap Stand)** แตะปุ๊บ วาร์ปปั๊บ ไม่ต้องโหลดแอป!

---

## 🌟 ฟีเจอร์หลักของระบบ (Features)

1. **🌐 หน้าเว็บ Landing Page ปิดการขาย (`index.html`):**
   - สลับ 2 โหมดในคลิกเดียว: สำหรับบุคคล/เซลล์ (B2C) และ สำหรับร้านค้า/คาเฟ่/คลินิก (B2B)
   - ตัวจำลอง 3D Card Simulator กดลองแตะเสมือนจริง (Interactive Live Tap Demo)
   - ฟอร์ม Checkout สั่งซื้อ พร้อมระบบคำนวณโค้ดส่วนลด `VIP50`, ช่องทางการชำระ PromptPay QR & เก็บเงินปลายทาง
   - ฝัง Schema SEO (JSON-LD) ครบถ้วน เพื่อให้ติดอันดับ Google Rich Snippets

2. **📱 หน้าโปรไฟล์นามบัตรดิจิทัลจริง (`profile.html`):**
   - รองรับ Dynamic Query Parameters เช่น `?name=...&title=...&phone=...&line=...`
   - **ปุ่ม One-Tap บันทึกเบอร์ลงเครื่อง (.vcf):** แตะครั้งเดียวโหลดไฟล์ vCard บันทึกคอนแท็กต์เข้า iPhone และ Android ทันที
   - ปุ่มลัดโทรออก, แอด LINE, ส่งอีเมล, แผนที่, บัญชีพร้อมเพย์
   - ระบบแลกคอนแท็กต์ (Exchange Contact Modal)

3. **⭐ หน้าป้ายแตะรีวิว Google 5 ดาว (`review.html`):**
   - สำหรับตั้งโต๊ะร้านอาหาร คาเฟ่ คลินิก
   - แตะดาว 5 ดาว เด้งเข้าหน้าเขียนรีวิว Google Maps ทันที
   - มีปุ่มคัดลอกข้อความรีวิวตัวอย่าง (Copy Review Templates) ช่วยให้ลูกค้ากดส่งรีวิวง่ายขึ้น 10 เท่า
   - คูปองรับส่วนลด/ของแถมท้ายบิลเมื่อรีวิว

4. **🛠️ ระบบสร้างโปรไฟล์และเขียนชิป NFC (`builder.html`):**
   - ฟอร์มกรอกข้อมูลพร้อมพรีวิวแบบ Real-time
   - สร้าง URL และ QR Code ความละเอียดสูงสำหรับพิมพ์สกรีนหลังบัตร
   - คู่มือ 3 ขั้นตอนในการใช้มือถือ (เช่น Xiaomi 14T Pro / iPhone) เขียนข้อมูลลงชิป NFC ผ่านแอปฟรี `NFC Tools`

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```text
TAPKARD_NFC_SmartCard/
├── index.html                           # หน้าหลัก Landing Page & Sales Funnel
├── profile.html                         # หน้าโปรไฟล์นามบัตรดิจิทัล (ปลายทางแตะ NFC)
├── review.html                          # หน้าป้ายแตะรีวิว Google 5 ดาว หน้าร้าน
├── builder.html                         # เครื่องมือสร้างโปรไฟล์ & ลิงก์เขียนชิป NFC
├── สรุปแผนธุรกิจ_TAPKARD_นามบัตรNFC.html # แดชบอร์ดสรุปต้นทุน กำไร และแผนธุรกิจ
├── viral-video-playbook.md              # คัมภีร์สคริปต์วิดีโอไวรัล 4 รูปแบบ (TikTok/Reels)
├── seo-and-ads-strategy.md              # แผนยุทธศาสตร์ SEO และคู่มือยิง Meta/TikTok/Google Ads
└── README.md                            # คู่มือภาพรวมโครงการ
```

---

## 🛠️ วิธีการใช้งาน & การเขียนชิป NFC

1. เปิดหน้า [`builder.html`](builder.html) เพื่อกรอกข้อมูลของคุณ
2. คัดลอกลิงก์ที่ระบบสร้างให้
3. เปิดแอป **NFC Tools** บนมือถือ ➔ เลือก **Write** ➔ **Add a record** ➔ **URL** ➔ วางลิงก์ลงไป
4. นำบัตร NFC หรือป้ายอะคริลิกมาทาบหลังมือถือบริเวณโมดูลกล้อง ก็พร้อมใช้งานทันที!
