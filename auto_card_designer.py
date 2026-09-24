import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode

# Dimensions for Standard CR80 Card with 1mm Bleed at 300 DPI
# 87.6 mm x 56 mm -> approx 1035 x 661 pixels
CARD_W = 1035
CARD_H = 661

# Fonts
FONT_THAI_BOLD = r"C:\Windows\Fonts\LeelaUIb.ttf"
FONT_THAI_REG = r"C:\Windows\Fonts\LeelawUI.ttf"
if not os.path.exists(FONT_THAI_BOLD):
    FONT_THAI_BOLD = r"C:\Windows\Fonts\tahomabd.ttf"
    FONT_THAI_REG = r"C:\Windows\Fonts\tahoma.ttf"

def create_card_front(name, title, company, photo_path=None, theme="gold", output_path="front_print_300dpi.png"):
    """Generates 300 DPI print-ready front of card"""
    # Create base canvas (Matte Black / Dark Carbon)
    img = Image.new("RGBA", (CARD_W, CARD_H), (14, 18, 27, 255))
    draw = ImageDraw.Draw(img)

    # Accent colors based on theme
    if theme == "gold":
        accent_color = (212, 175, 55, 255) # Classic Gold #D4AF37
        secondary_color = (245, 222, 140, 255)
    else: # cyber blue
        accent_color = (59, 130, 246, 255) # Blue #3B82F6
        secondary_color = (147, 197, 253, 255)

    # Subtle decorative geometric lines / luxury tech watermark
    for i in range(1, 4):
        draw.arc([-100 - i*20, -100 - i*20, 500 + i*20, 500 + i*20], start=0, end=90, fill=(255, 255, 255, 12), width=2)

    # Corner NFC Icon watermark
    draw.arc([CARD_W - 140, 40, CARD_W - 40, 140], start=180, end=270, fill=accent_color, width=4)
    draw.arc([CARD_W - 120, 60, CARD_W - 40, 140], start=180, end=270, fill=accent_color, width=4)
    draw.arc([CARD_W - 100, 80, CARD_W - 40, 140], start=180, end=270, fill=accent_color, width=4)

    # Top Brand Header
    font_brand = ImageFont.truetype(FONT_THAI_BOLD, 36)
    font_sub = ImageFont.truetype(FONT_THAI_REG, 20)
    draw.text((80, 65), "TAPKARD", fill=(255, 255, 255, 255), font=font_brand)
    draw.text((250, 72), "SMART NFC", fill=accent_color, font=font_sub)

    # Thin accent rule
    draw.line([(80, 125), (CARD_W - 80, 125)], fill=(255, 255, 255, 30), width=2)

    # Photo / Avatar placement (if provided)
    text_x = 80
    if photo_path and os.path.exists(photo_path):
        try:
            avatar = Image.open(photo_path).convert("RGBA")
            avatar_size = 280
            avatar = avatar.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
            
            # Mask to rounded rectangle or circle
            mask = Image.new("L", (avatar_size, avatar_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle([0, 0, avatar_size, avatar_size], radius=35, fill=255)
            
            # Gold border behind avatar
            border_size = avatar_size + 12
            border_img = Image.new("RGBA", (border_size, border_size), (0, 0, 0, 0))
            border_draw = ImageDraw.Draw(border_img)
            border_draw.rounded_rectangle([0, 0, border_size, border_size], radius=40, outline=accent_color, width=5)
            
            img.paste(border_img, (74, 214), border_img)
            img.paste(avatar, (80, 220), mask)
            text_x = 400
        except Exception as e:
            print("Avatar load error:", e)

    # Main Typography
    font_name = ImageFont.truetype(FONT_THAI_BOLD, 62)
    font_title = ImageFont.truetype(FONT_THAI_BOLD, 32)
    font_company = ImageFont.truetype(FONT_THAI_REG, 26)

    # Name
    draw.text((text_x, 235), name, fill=(255, 255, 255, 255), font=font_name)
    # Title / Position
    draw.text((text_x, 320), title, fill=accent_color, font=font_title)
    # Company
    draw.text((text_x, 375), company, fill=(180, 190, 205, 255), font=font_company)

    # Bottom Luxury Chip Indicator
    draw.rounded_rectangle([(CARD_W - 200, CARD_H - 100), (CARD_W - 80, CARD_H - 65)], radius=10, fill=(255, 255, 255, 10), outline=accent_color, width=2)
    font_chip = ImageFont.truetype(FONT_THAI_BOLD, 18)
    draw.text((CARD_W - 180, CARD_H - 92), "NFC ENABLED", fill=secondary_color, font=font_chip)

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Front card saved: {output_path}")
    return output_path

def create_card_back(qr_url, phone, line_id, theme="gold", output_path="back_print_300dpi.png"):
    """Generates 300 DPI print-ready back of card with QR code and NFC wave"""
    img = Image.new("RGBA", (CARD_W, CARD_H), (10, 14, 22, 255))
    draw = ImageDraw.Draw(img)

    if theme == "gold":
        accent_color = (212, 175, 55, 255)
    else:
        accent_color = (59, 130, 246, 255)

    # Generate high-res QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    
    # Resize QR code
    qr_size = 320
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    
    # White rounded background for QR code
    qr_bg_size = qr_size + 30
    qr_bg = Image.new("RGBA", (qr_bg_size, qr_bg_size), (0, 0, 0, 0))
    qr_draw = ImageDraw.Draw(qr_bg)
    qr_draw.rounded_rectangle([0, 0, qr_bg_size, qr_bg_size], radius=25, fill=(255, 255, 255, 255), outline=accent_color, width=4)
    
    qr_x = 90
    qr_y = int((CARD_H - qr_bg_size) / 2)
    img.paste(qr_bg, (qr_x, qr_y), qr_bg)
    img.paste(qr_img, (qr_x + 15, qr_y + 15), qr_img)

    # Right side instructions & contact
    text_x = 480
    font_head = ImageFont.truetype(FONT_THAI_BOLD, 42)
    font_sub = ImageFont.truetype(FONT_THAI_REG, 26)
    font_contact = ImageFont.truetype(FONT_THAI_BOLD, 28)

    draw.text((text_x, 150), "แตะหลังมือถือ หรือ สแกน", fill=(255, 255, 255, 255), font=font_head)
    draw.text((text_x, 215), "เพื่อบันทึกคอนแท็กต์ลงในโทรศัพท์ทันที", fill=(160, 175, 195, 255), font=font_sub)

    # Contact details
    draw.text((text_x, 300), f"TEL: {phone}", fill=accent_color, font=font_contact)
    draw.text((text_x, 350), f"LINE: {line_id}", fill=(255, 255, 255, 255), font=font_contact)

    # Footer
    font_foot = ImageFont.truetype(FONT_THAI_REG, 20)
    draw.text((text_x, 480), "POWERED BY TAPKARD™ SMART NFC SYSTEM", fill=(100, 115, 135, 255), font=font_foot)

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Back card saved: {output_path}")
    return output_path

def create_mockup_preview(front_path, back_path, output_path="card_mockup_preview.png"):
    """Combines front and back into a realistic luxury presentation mockup for client proofing"""
    canvas_w, canvas_h = 1400, 900
    mockup = Image.new("RGBA", (canvas_w, canvas_h), (8, 11, 19, 255))
    draw = ImageDraw.Draw(mockup)

    # Subtle ambient gradient glow in center
    glow = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([0, 0, 800, 800], fill=(30, 58, 138, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    mockup.paste(glow, (300, 50), glow)

    # Resize cards for mockup
    card_w, card_h = 620, 396
    front = Image.open(front_path).convert("RGBA").resize((card_w, card_h), Image.Resampling.LANCZOS)
    back = Image.open(back_path).convert("RGBA").resize((card_w, card_h), Image.Resampling.LANCZOS)

    # Apply rounded corners and drop shadows
    mask = Image.new("L", (card_w, card_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, card_w, card_h], radius=24, fill=255)

    # Paste Front Card (Left, slightly higher)
    mockup.paste(front, (120, 220), mask)
    # Paste Back Card (Right, slightly lower)
    mockup.paste(back, (660, 280), mask)

    # Title header on mockup
    font_title = ImageFont.truetype(FONT_THAI_BOLD, 46)
    font_desc = ImageFont.truetype(FONT_THAI_REG, 24)
    draw.text((120, 80), "แบบตัวอย่างสำหรับส่งสกรีนพิมพ์จริง (TAPKARD™ Proof Preview)", fill=(255, 255, 255, 255), font=font_title)
    draw.text((120, 140), "ความละเอียด 300 DPI ระบบ UV Printing เคลือบด้านกันน้ำ 100%", fill=(147, 197, 253, 255), font=font_desc)

    mockup.save(output_path, "PNG")
    print(f"Mockup preview saved: {output_path}")
    return output_path

if __name__ == "__main__":
    out_dir = r"C:\Users\nattc\OneDrive\Desktop\AI ลองไปเรื่อย\TAPKARD_NFC_SmartCard\sample_proof"
    os.makedirs(out_dir, exist_ok=True)
    
    f_path = os.path.join(out_dir, "front_print_300dpi.png")
    b_path = os.path.join(out_dir, "back_print_300dpi.png")
    m_path = os.path.join(out_dir, "client_mockup_proof.png")

    print("Generating sample card design...")
    create_card_front(
        name="ณัฐพงษ์ เจริญทรัพย์",
        title="Managing Director & Founder",
        company="TAPKARD Enterprise Co., Ltd.",
        theme="gold",
        output_path=f_path
    )
    create_card_back(
        qr_url="https://nattcharoen-beep.github.io/tapkard-nfc-smartcard/profile.html",
        phone="081-234-5678",
        line_id="@tapkard",
        theme="gold",
        output_path=b_path
    )
    create_mockup_preview(f_path, b_path, m_path)
    print("All print assets successfully generated in:", out_dir)
