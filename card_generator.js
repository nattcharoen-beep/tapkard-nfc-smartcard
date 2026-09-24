/**
 * TAPKARD™ Cloud-Native 300 DPI Canvas Card Generator
 * Runs 100% in the cloud / browser without needing any local server or .bat file.
 */

const CARD_W = 1035; // 87.6 mm at 300 DPI
const CARD_H = 661;  // 56 mm at 300 DPI

// Helper to load image from URL or File
function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => resolve(img);
    img.onerror = () => resolve(null);
    img.src = src;
  });
}

// Generate Front Card 300 DPI
async function generateFrontCanvas(data) {
  const canvas = document.createElement('canvas');
  canvas.width = CARD_W;
  canvas.height = CARD_H;
  const ctx = canvas.getContext('2d');

  const theme = data.theme || 'gold';
  const isGold = theme === 'gold';
  const accentColor = isGold ? '#D4AF37' : '#3B82F6';
  const secondaryColor = isGold ? '#F6E05E' : '#93C5FD';

  // Base Matte Dark Gradient
  const bgGrad = ctx.createLinearGradient(0, 0, CARD_W, CARD_H);
  bgGrad.addColorStop(0, '#0E121B');
  bgGrad.addColorStop(1, '#080B12');
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, CARD_W, CARD_H);

  // Decorative subtle circular tech waves
  ctx.save();
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
  ctx.lineWidth = 2;
  for (let i = 1; i <= 4; i++) {
    ctx.beginPath();
    ctx.arc(-80, -80, 500 + i * 40, 0, Math.PI / 2);
    ctx.stroke();
  }
  ctx.restore();

  // Top NFC Wave Icon
  ctx.save();
  ctx.strokeStyle = accentColor;
  ctx.lineWidth = 4;
  ctx.lineCap = 'round';
  const nfcX = CARD_W - 80;
  const nfcY = 80;
  for (let r = 20; r <= 45; r += 12) {
    ctx.beginPath();
    ctx.arc(nfcX, nfcY, r, Math.PI * 1.05, Math.PI * 1.55);
    ctx.stroke();
  }
  ctx.restore();

  // Brand Header
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 36px "Prompt", sans-serif';
  ctx.fillText('TAPKARD', 80, 75);

  ctx.fillStyle = accentColor;
  ctx.font = '600 18px "Prompt", sans-serif';
  ctx.fillText('SMART NFC', 260, 72);

  // Accent rule line
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(80, 115);
  ctx.lineTo(CARD_W - 80, 115);
  ctx.stroke();

  let textX = 80;

  // Render Avatar / Photo if provided
  if (data.avatar) {
    const avatarImg = typeof data.avatar === 'string' ? await loadImage(data.avatar) : data.avatar;
    if (avatarImg) {
      const size = 260;
      const ax = 80;
      const ay = 180;

      ctx.save();
      // Outer border
      ctx.strokeStyle = accentColor;
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.roundRect(ax - 4, ay - 4, size + 8, size + 8, 36);
      ctx.stroke();

      // Clip image
      ctx.beginPath();
      ctx.roundRect(ax, ay, size, size, 32);
      ctx.clip();
      ctx.drawImage(avatarImg, ax, ay, size, size);
      ctx.restore();

      textX = 380;
    }
  }

  // Name
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 62px "Prompt", sans-serif';
  ctx.fillText(data.name || 'ชื่อ - นามสกุล', textX, 260);

  // Title / Position
  ctx.fillStyle = accentColor;
  ctx.font = '600 32px "Prompt", sans-serif';
  ctx.fillText(data.title || 'ตำแหน่ง / อาชีพ', textX, 330);

  // Company
  ctx.fillStyle = '#94A3B8';
  ctx.font = '400 28px "Prompt", sans-serif';
  ctx.fillText(data.company || 'ชื่อบริษัท หรือ องค์กร', textX, 385);

  // Bottom Chip Badge
  ctx.save();
  ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
  ctx.strokeStyle = accentColor;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.roundRect(CARD_W - 220, CARD_H - 100, 140, 40, 10);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = secondaryColor;
  ctx.font = 'bold 16px "Prompt", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('NFC ENABLED', CARD_W - 150, CARD_H - 74);
  ctx.restore();

  return canvas;
}

// Generate Back Card 300 DPI
async function generateBackCanvas(data) {
  const canvas = document.createElement('canvas');
  canvas.width = CARD_W;
  canvas.height = CARD_H;
  const ctx = canvas.getContext('2d');

  const theme = data.theme || 'gold';
  const isGold = theme === 'gold';
  const accentColor = isGold ? '#D4AF37' : '#3B82F6';

  // Base Matte Dark Canvas
  ctx.fillStyle = '#090D15';
  ctx.fillRect(0, 0, CARD_W, CARD_H);

  // QR Code Generation
  const qrUrl = data.profile_url || `https://nattcharoen-beep.github.io/tapkard-nfc-smartcard/profile.html?name=${encodeURIComponent(data.name || '')}`;
  const qrApiUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&margin=0&data=${encodeURIComponent(qrUrl)}`;
  const qrImg = await loadImage(qrApiUrl);

  const qrBoxSize = 340;
  const qx = 80;
  const qy = (CARD_H - qrBoxSize) / 2;

  // Rounded White Box for QR Code
  ctx.save();
  ctx.fillStyle = '#FFFFFF';
  ctx.strokeStyle = accentColor;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.roundRect(qx, qy, qrBoxSize, qrBoxSize, 28);
  ctx.fill();
  ctx.stroke();

  if (qrImg) {
    ctx.drawImage(qrImg, qx + 20, qy + 20, 300, 300);
  }
  ctx.restore();

  // Instructions & Contact details on Right
  const textX = 470;
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 44px "Prompt", sans-serif';
  ctx.fillText('แตะหลังมือถือ หรือ สแกน', textX, 180);

  ctx.fillStyle = '#94A3B8';
  ctx.font = '400 24px "Prompt", sans-serif';
  ctx.fillText('เพื่อบันทึกคอนแท็กต์ลงในโทรศัพท์ทันที', textX, 235);

  ctx.fillStyle = accentColor;
  ctx.font = 'bold 28px "Prompt", sans-serif';
  ctx.fillText(`TEL: ${data.phone || '08X-XXX-XXXX'}`, textX, 320);

  ctx.fillStyle = '#FFFFFF';
  ctx.fillText(`LINE: ${data.line_id || '@tapkard'}`, textX, 370);

  ctx.fillStyle = '#64748B';
  ctx.font = '400 18px "Prompt", sans-serif';
  ctx.fillText('POWERED BY TAPKARD™ SMART NFC SYSTEM', textX, 480);

  return canvas;
}

// Generate Realistic 3D Mockup Presentation
async function generateMockupCanvas(frontCanvas, backCanvas) {
  const canvas = document.createElement('canvas');
  canvas.width = 1400;
  canvas.height = 900;
  const ctx = canvas.getContext('2d');

  // Background
  const grad = ctx.createRadialGradient(700, 450, 50, 700, 450, 700);
  grad.addColorStop(0, '#1E293B');
  grad.addColorStop(1, '#0B0F19');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Header Title
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 42px "Prompt", sans-serif';
  ctx.fillText('แบบตัวอย่างสำหรับส่งสกรีนพิมพ์จริง (TAPKARD™ Proof Preview)', 100, 80);

  ctx.fillStyle = '#93C5FD';
  ctx.font = '400 22px "Prompt", sans-serif';
  ctx.fillText('ความละเอียด 300 DPI ระบบ UV Printing เคลือบด้านกันน้ำ 100%', 100, 130);

  const cardW = 620;
  const cardH = 396;

  // Front Card
  ctx.save();
  ctx.shadowColor = 'rgba(0, 0, 0, 0.7)';
  ctx.shadowBlur = 35;
  ctx.shadowOffsetX = -10;
  ctx.shadowOffsetY = 20;
  ctx.beginPath();
  ctx.roundRect(100, 220, cardW, cardH, 24);
  ctx.clip();
  ctx.drawImage(frontCanvas, 100, 220, cardW, cardH);
  ctx.restore();

  // Back Card
  ctx.save();
  ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
  ctx.shadowBlur = 45;
  ctx.shadowOffsetX = 15;
  ctx.shadowOffsetY = 25;
  ctx.beginPath();
  ctx.roundRect(660, 290, cardW, cardH, 24);
  ctx.clip();
  ctx.drawImage(backCanvas, 660, 290, cardW, cardH);
  ctx.restore();

  return canvas;
}

// Master function
window.generatePrintPackage = async function(data) {
  const frontCanvas = await generateFrontCanvas(data);
  const backCanvas = await generateBackCanvas(data);
  const mockupCanvas = await generateMockupCanvas(frontCanvas, backCanvas);

  return {
    frontDataUrl: frontCanvas.toDataURL('image/png'),
    backDataUrl: backCanvas.toDataURL('image/png'),
    mockupDataUrl: mockupCanvas.toDataURL('image/png'),
    frontBlob: await new Promise(r => frontCanvas.toBlob(r, 'image/png')),
    backBlob: await new Promise(r => backCanvas.toBlob(r, 'image/png')),
    mockupBlob: await new Promise(r => mockupCanvas.toBlob(r, 'image/png'))
  };
};
