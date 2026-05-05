#!/usr/bin/env python3
"""Generate AI tutor video for Complex Analysis course.

Uses Microsoft Edge Neural TTS for narration and PIL for animated visuals.
Outputs a single MP4 file ready to embed on the website.
"""

import asyncio
import math
import os
import subprocess
import sys
from io import BytesIO
from pathlib import Path

import edge_tts
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ============== CONFIG ==============
W, H = 1280, 720
FPS = 24
VOICE = 'en-US-AvaMultilingualNeural'  # high-quality neural voice
GAP = 0.35  # seconds between scenes
BUILD = Path(__file__).parent / 'build'
BUILD.mkdir(exist_ok=True)
AUDIO_DIR = BUILD / 'audio'
AUDIO_DIR.mkdir(exist_ok=True)
OUT = Path(__file__).parent / 'tutor-video.mp4'

# ============== FONTS ==============
FONT_FILES = {
    ('serif', False): '/System/Library/Fonts/Supplemental/STIXTwoMath.otf',
    ('serif', True):  '/System/Library/Fonts/Supplemental/STIXTwoMath.otf',
    ('serif-it', True): '/System/Library/Fonts/Supplemental/STIXTwoText-Italic.ttf',
    ('serif-it', False): '/System/Library/Fonts/Supplemental/STIXTwoText-Italic.ttf',
    ('sans', False): '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    ('sans', True):  '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    ('mono', False): '/System/Library/Fonts/Menlo.ttc',
}
_font_cache = {}
def F(family='serif', size=20, bold=False):
    key = (family, size, bold)
    if key not in _font_cache:
        path = FONT_FILES.get((family, bold)) or FONT_FILES[('sans', False)]
        try:
            _font_cache[key] = ImageFont.truetype(path, size)
        except Exception:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]

# ============== SCENES ==============
SCENES = [
    {'title': 'Welcome', 'visual': 'title', 'formula': '',
     'text': "Hi! I'm your AI tutor for complex analysis. In about twelve minutes, we'll go through the entire course, from imaginary numbers all the way to evaluating real integrals using residues. Let's get started."},
    {'title': 'The Imaginary Unit', 'visual': 'imaginary', 'formula': 'i^2 = -1',
     'text': "Everything begins with one bold invention. The imaginary unit i, defined by i squared equals negative one. From this single rule, an entire universe of new numbers opens up."},
    {'title': 'Complex Numbers', 'visual': 'number', 'formula': 'z = x + iy',
     'text': "A complex number is z equals x plus i times y, where x and y are real numbers. We call x the real part of z, and y the imaginary part. Just y, not i y. That's a common trip up."},
    {'title': 'The Complex Plane', 'visual': 'plane', 'formula': '',
     'text': "We picture each complex number as a point in the plane. x is the horizontal coordinate, y is vertical. Adding two complex numbers is just like adding two vectors, component by component."},
    {'title': 'Modulus', 'visual': 'modulus', 'formula': '|z| = sqrt(x^2 + y^2)',
     'text': "The modulus, written z with vertical bars, is the distance from z to the origin. Square root of x squared plus y squared. It measures how big z is."},
    {'title': 'Conjugate', 'visual': 'conjugate', 'formula': 'z * conj(z) = |z|^2',
     'text': "The conjugate, z bar, flips the sign of the imaginary part. Geometrically, it's reflection across the real axis. And here's a fundamental identity we'll use everywhere. z times its conjugate equals z modulus squared."},
    {'title': 'Polar Form', 'visual': 'polar', 'formula': 'z = r e^(i theta)',
     'text': "In polar form, we write z as r times e to the i theta. Where r is the modulus, and theta is the angle from the positive real axis. This form is incredibly useful for multiplication and powers."},
    {'title': "Euler's Formula", 'visual': 'euler', 'formula': 'e^(i theta) = cos(theta) + i sin(theta)',
     'text': "Behind it all is Euler's formula. e to the i theta equals cosine theta plus i sine theta. This single equation links exponentials and trigonometry. It's everywhere in this subject."},
    {'title': 'Multiplication', 'visual': 'multiply', 'formula': '',
     'text': "Polar form makes multiplication beautifully geometric. To multiply two complex numbers, you multiply their moduli, and add their angles. Multiplication is a rotation combined with a scaling."},
    {'title': 'Roots of Unity', 'visual': 'roots', 'formula': '',
     'text': "Every nonzero complex number has exactly n n-th roots, equally spaced around a circle. Here are the five fifth roots of unity. They form a perfect pentagon."},
    {'title': 'Functions', 'visual': 'func', 'formula': 'f(z) = u(x,y) + i v(x,y)',
     'text': "A complex function takes complex numbers in, and returns complex numbers out. We usually write f equals u plus i v. Where u and v are real-valued functions of x and y."},
    {'title': 'The Complex Derivative', 'visual': 'derivative', 'formula': '',
     'text': "The complex derivative is defined just like the real one. But with a critical twist. The limit must exist, and be the same value, no matter which direction delta z approaches zero from."},
    {'title': 'Cauchy-Riemann', 'visual': 'cr', 'formula': '',
     'text': "That single requirement is incredibly strict. It forces the Cauchy Riemann equations. u sub x equals v sub y. And u sub y equals minus v sub x. These two equations are the fingerprint of complex differentiability."},
    {'title': 'Analytic Functions', 'visual': 'analytic', 'formula': '',
     'text': "A function is analytic at a point if it's differentiable in some open disk around that point. Not just at the point. Analytic functions are the heroes of complex analysis. Almost every theorem assumes analyticity."},
    {'title': 'Real vs Complex', 'visual': 'compare', 'formula': '',
     'text': "Here's where the magic begins. In real calculus, differentiable does not mean infinitely differentiable. But in complex analysis, analytic at a single point means infinitely differentiable, equal to its Taylor series, and a host of other miracles."},
    {'title': 'The Exponential', 'visual': 'exp', 'formula': '',
     'text': "The exponential extends naturally. e to the z equals e to the x times cosine y plus i sine y. It's an entire function. Analytic on all of the complex plane. And surprisingly, it's periodic with period two pi i."},
    {'title': 'The Logarithm', 'visual': 'log', 'formula': '',
     'text': "Because the exponential is periodic, the complex logarithm is multi valued. log z equals natural log r, plus i theta plus 2 n pi i. For any integer n. Infinitely many values for the same z."},
    {'title': 'Branch Cuts', 'visual': 'branch', 'formula': '',
     'text': "To make log single valued and analytic, we cut a ray out of the plane. We call this the branch cut. And we choose one consistent value of theta. The principal branch uses theta between negative pi and pi."},
    {'title': 'Contour Integration', 'visual': 'contour', 'formula': '',
     'text': "To integrate a complex function, we integrate along a curve, called a contour. Parametrize the curve as z of t. Then integrate f of z of t, times z prime of t, dt. It's a one dimensional integral over a curve in the plane."},
    {'title': 'Cauchy-Goursat', 'visual': 'goursat', 'formula': '',
     'text': "Now the first big theorem. Cauchy Goursat. If f is analytic everywhere inside and on a closed loop, then the integral around that loop is exactly zero. It's a kind of conservation law."},
    {'title': 'The 1/z Example', 'visual': 'oneoverz', 'formula': '',
     'text': "But if f has a singularity inside, the integral can be nonzero. The classic example. The integral of one over z, around any loop enclosing the origin, is exactly two pi i. Always two pi i, no matter the shape of the loop."},
    {'title': 'Cauchy Integral Formula', 'visual': 'cif', 'formula': '',
     'text': "From Cauchy Goursat we get the magical Cauchy integral formula. If z naught is inside the loop, the value f at z naught equals one over two pi i, times the integral of f of z divided by z minus z naught, around the loop. The values inside are completely determined by the values on the boundary."},
    {'title': 'Infinitely Differentiable', 'visual': 'derivatives', 'formula': '',
     'text': "By differentiating this formula again and again, you express every higher derivative as an integral. So in complex analysis, analytic on an open set means infinitely differentiable. This is dramatically stronger than the real case."},
    {'title': "Liouville's Theorem", 'visual': 'liouville', 'formula': '',
     'text': "Here's another miracle. Liouville's theorem. Any bounded entire function must be constant. Unlike sine x in real analysis, you can't have an interesting bounded function defined on the entire complex plane."},
    {'title': 'Fundamental Theorem of Algebra', 'visual': 'fta', 'formula': '',
     'text': "From Liouville, we derive the fundamental theorem of algebra. Every non constant complex polynomial has at least one root, and factors completely into linear factors. Real analysis can not do this."},
    {'title': 'Taylor and Laurent Series', 'visual': 'series', 'formula': '',
     'text': "If a function is analytic on a disk, it equals its Taylor series there. If the function has a singularity at the center, we extend with negative powers. That's the Laurent series. It converges in an annulus around the singular point."},
    {'title': 'Three Singularity Types', 'visual': 'singularities', 'formula': '',
     'text': "We classify isolated singularities by the principal part of the Laurent series. Three types. Removable, where there are no negative powers. Poles of order m, with finitely many. And essential, where there are infinitely many."},
    {'title': 'The Residue', 'visual': 'residue', 'formula': '',
     'text': "Here's the magic number. The residue of f at a singularity is just b sub one. The coefficient of one over z minus z naught in the Laurent series. This single complex number captures all the integration behavior at the singularity."},
    {'title': 'Residue Theorem', 'visual': 'rt', 'formula': '',
     'text': "Cauchy's residue theorem. The integral of f around a closed loop equals two pi i, times the sum of the residues of f at all singularities inside the loop. This single formula computes integrals that would otherwise be nearly impossible."},
    {'title': 'Real Integrals', 'visual': 'realint', 'formula': '',
     'text': "And the punchline. Hard real integrals, like the integral from zero to infinity of one over x to the sixth plus one, fall to residues in just a few lines. Extend to a complex contour, find the residues in the upper half plane, and you're done."},
    {'title': 'Goodbye!', 'visual': 'closing', 'formula': '',
     'text': "That's complex analysis, end to end. The whole subject is built on one idea. Complex differentiability is so strong it forces every other miracle. Thanks for watching, and good luck on your final!"},
]

# ============== AUDIO GEN ==============
async def gen_audio():
    print(f"[1/4] Generating narration for {len(SCENES)} scenes...")
    for i, sc in enumerate(SCENES):
        path = AUDIO_DIR / f'scene_{i:02d}.mp3'
        if path.exists() and path.stat().st_size > 1000:
            continue
        c = edge_tts.Communicate(sc['text'], VOICE, rate='+0%', pitch='+0Hz')
        await c.save(str(path))
        print(f"  scene {i+1}/{len(SCENES)}: {sc['title']}")

    # silence file
    silence = AUDIO_DIR / 'silence.mp3'
    if not silence.exists():
        subprocess.run([
            'ffmpeg', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=24000:cl=mono',
            '-t', str(GAP), '-q:a', '9', '-acodec', 'libmp3lame', str(silence)
        ], check=True, capture_output=True)

    # concat list
    concat_path = BUILD / 'concat.txt'
    with open(concat_path, 'w') as f:
        for i in range(len(SCENES)):
            ap = (AUDIO_DIR / f'scene_{i:02d}.mp3').absolute()
            f.write(f"file '{ap}'\n")
            if i < len(SCENES) - 1:
                f.write(f"file '{silence.absolute()}'\n")

    full_audio = BUILD / 'full_audio.mp3'
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat_path),
        '-acodec', 'libmp3lame', '-b:a', '192k', str(full_audio)
    ], check=True, capture_output=True)
    return full_audio

def get_duration(path):
    r = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=nw=1:nk=1', str(path)
    ], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())

def compute_timings():
    timings = []
    t = 0.0
    for i in range(len(SCENES)):
        d = get_duration(AUDIO_DIR / f'scene_{i:02d}.mp3')
        timings.append((t, t + d))
        t += d + GAP
    return timings, t

# ============== LAYOUT ==============
LEFT_W = 380
PAD = 24
TOPBAR_H = 56
BOTBAR_H = 80
# left panel: avatar top, caption bottom
AVA_X = PAD
AVA_Y = TOPBAR_H + PAD
AVA_W = LEFT_W - 2*PAD
AVA_H = 290
CAP_X = AVA_X
CAP_Y = AVA_Y + AVA_H + PAD
CAP_W = AVA_W
CAP_H = H - CAP_Y - PAD - BOTBAR_H
# right panel
VX = LEFT_W + PAD
VY = TOPBAR_H + PAD
VW = W - VX - PAD
VH = H - VY - PAD - BOTBAR_H - 100  # leave 100 for formula box
FX = VX
FY = VY + VH + PAD
FW = VW
FH = 100 - PAD

# coord system for visualizations: origin at center of right panel
CX = VX + VW // 2
CY = VY + VH // 2
SCALE = 95

# ============== HELPERS ==============
def plot(x, y):
    return (CX + x*SCALE, CY - y*SCALE)

def draw_axes(d, label=True):
    # x axis
    d.line([(VX + 30, CY), (VX + VW - 30, CY)], fill=(120, 130, 150), width=2)
    # y axis
    d.line([(CX, VY + 30), (CX, VY + VH - 30)], fill=(120, 130, 150), width=2)
    # arrows
    d.polygon([(VX + VW - 30, CY), (VX + VW - 40, CY - 7), (VX + VW - 40, CY + 7)], fill=(120, 130, 150))
    d.polygon([(CX, VY + 30), (CX - 7, VY + 40), (CX + 7, VY + 40)], fill=(120, 130, 150))
    if label:
        d.text((VX + VW - 26, CY + 4), 'Re', font=F('serif-it', 18, True), fill=(80, 85, 100))
        d.text((CX + 8, VY + 28), 'Im', font=F('serif-it', 18, True), fill=(80, 85, 100))

def draw_grid(d):
    for i in range(-5, 6):
        if i == 0: continue
        x = CX + i*SCALE
        y = CY - i*SCALE
        if VX + 30 <= x <= VX + VW - 30:
            d.line([(VX + 30, y), (VX + VW - 30, y)] if False else
                   [(x, VY + 30), (x, VY + VH - 30)],
                   fill=(235, 240, 248), width=1)
        if VY + 30 <= y <= VY + VH - 30:
            d.line([(VX + 30, y), (VX + VW - 30, y)], fill=(235, 240, 248), width=1)

def draw_arrow(d, x1, y1, x2, y2, color=(220, 38, 38), width=3):
    d.line([(x1, y1), (x2, y2)], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    head = 12
    p1 = (x2 - head*math.cos(ang - math.pi/6), y2 - head*math.sin(ang - math.pi/6))
    p2 = (x2 - head*math.cos(ang + math.pi/6), y2 - head*math.sin(ang + math.pi/6))
    d.polygon([(x2, y2), p1, p2], fill=color)

def draw_text_centered(d, text, cx, cy, font, fill):
    bbox = d.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text((cx - w//2, cy - h//2), text, font=font, fill=fill)

def fill_panel(d):
    # right panel white background
    d.rounded_rectangle([VX, VY, VX+VW, VY+VH], radius=12, fill=(255, 255, 255))

# ============== AVATAR ==============
def draw_avatar(d, t, speaking=True, mouth_amp=None):
    # Background circle (panel)
    cx = AVA_X + AVA_W//2
    cy = AVA_Y + 130
    # Body (shoulders)
    d.rounded_rectangle([cx-55, cy+85, cx+55, cy+170], radius=12,
                        fill=(70, 80, 100))
    # name plate
    d.rounded_rectangle([cx-35, cy+95, cx+35, cy+115], radius=4, fill=(30, 41, 59))
    draw_text_centered(d, 'AI', cx, cy+106, F('mono', 13, True), (251, 191, 36))
    # antenna
    d.line([(cx, cy-90), (cx, cy-110)], fill=(251, 191, 36), width=3)
    pulse_r = 6 + int(2*math.sin(t*3))
    d.ellipse([cx-pulse_r, cy-110-pulse_r, cx+pulse_r, cy-110+pulse_r],
              fill=(251, 191, 36))
    # head
    head_r = 75
    # head shadow
    d.ellipse([cx-head_r-2, cy-head_r-2+4, cx+head_r+2, cy+head_r+2+4],
              fill=(20, 30, 50))
    d.ellipse([cx-head_r, cy-head_r, cx+head_r, cy+head_r],
              fill=(96, 165, 250), outline=(30, 58, 138), width=2)
    # ear pods
    d.rounded_rectangle([cx-head_r-12, cy-12, cx-head_r+2, cy+22], radius=3, fill=(70, 80, 100))
    d.rounded_rectangle([cx+head_r-2, cy-12, cx+head_r+12, cy+22], radius=3, fill=(70, 80, 100))
    # eyes - blink every ~3 seconds
    blink_phase = (t % 3.5)
    blink = 1.0 if blink_phase > 0.15 else max(0.05, 1 - (0.15 - blink_phase) / 0.075)
    eye_w, eye_h = 14, int(17 * blink)
    eye_y = cy - 12
    d.ellipse([cx-22-eye_w, eye_y-eye_h, cx-22+eye_w, eye_y+eye_h], fill=(245, 250, 255))
    d.ellipse([cx+22-eye_w, eye_y-eye_h, cx+22+eye_w, eye_y+eye_h], fill=(245, 250, 255))
    if blink > 0.5:
        # pupils
        d.ellipse([cx-22-6, eye_y-6+2, cx-22+6, eye_y+6+2], fill=(30, 41, 59))
        d.ellipse([cx+22-6, eye_y-6+2, cx+22+6, eye_y+6+2], fill=(30, 41, 59))
        d.ellipse([cx-22-1, eye_y-3+2, cx-22+3, eye_y-3+6+2], fill=(255, 255, 255))
        d.ellipse([cx+22-1, eye_y-3+2, cx+22+3, eye_y-3+6+2], fill=(255, 255, 255))
    # eyebrows
    d.arc([cx-38, eye_y-22, cx-6, eye_y-2], start=200, end=340, fill=(30, 58, 138), width=3)
    d.arc([cx+6, eye_y-22, cx+38, eye_y-2], start=200, end=340, fill=(30, 58, 138), width=3)
    # mouth
    if speaking and mouth_amp is not None:
        amp = mouth_amp
    elif speaking:
        amp = 0.5 + 0.5 * abs(math.sin(t * 8))
    else:
        amp = 0.05
    mouth_h = int(3 + amp * 12)
    d.ellipse([cx-22, cy+30-mouth_h, cx+22, cy+30+mouth_h], fill=(30, 41, 59))
    if amp > 0.3:
        # tongue/teeth hint
        d.ellipse([cx-12, cy+30-int(mouth_h*0.5), cx+12, cy+30+int(mouth_h*0.5)],
                  fill=(220, 38, 60))

# ============== VISUALIZATIONS ==============
def vis_title(d, t):
    # full-canvas dark BG with sparkles - but we just draw on top of right panel area
    d.rounded_rectangle([VX, VY, VX+VW, VY+VH], radius=12, fill=(15, 23, 42))
    # sparkles
    for i in range(40):
        x = VX + ((i*137 + int(t*30)) % VW)
        y = VY + ((i*91) % VH)
        r = max(1, int(2 + 2*math.sin(t*1.5 + i)))
        col_h = (i*8) % 360
        # convert HSL-ish to a color
        bright = int(150 + 60*math.sin(t*2 + i))
        d.ellipse([x-r, y-r, x+r, y+r], fill=(min(bright+50, 255), bright, 255))
    # title
    title_w, title_h = d.textbbox((0,0), 'Complex Analysis', font=F('serif', 60, True))[2:]
    wobble = int(math.sin(t*0.8) * 4)
    d.text((CX - title_w//2, CY - 60 + wobble), 'Complex Analysis',
           font=F('serif', 60, True), fill=(251, 191, 36))
    sub = 'A 12-minute video tour'
    sw, _ = d.textbbox((0,0), sub, font=F('serif-it', 26))[2:]
    d.text((CX - sw//2, CY + 25), sub, font=F('serif-it', 26), fill=(220, 230, 245))
    sub2 = 'from i^2 = -1 to the residue theorem'
    sw, _ = d.textbbox((0,0), sub2, font=F('sans', 18))[2:]
    d.text((CX - sw//2, CY + 70), sub2, font=F('sans', 18), fill=(150, 160, 180))

def vis_imaginary(d, t):
    fill_panel(d)
    # big formula
    txt = 'i² = -1'
    s = 1 + 0.04 * math.sin(t * 1.5)
    fsz = int(110 * s)
    f = F('serif', fsz, True)
    bbox = d.textbbox((0,0), txt, font=f)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text((CX - w//2, CY - h//2), txt, font=f, fill=(30, 41, 59))
    # subtitle
    sub = 'the rule that opens a new universe'
    sf = F('serif-it', 22)
    sb = d.textbbox((0,0), sub, font=sf)
    d.text((CX - (sb[2]-sb[0])//2, VY + VH - 60), sub, font=sf, fill=(220, 38, 38))
    # floating i's
    for i in range(10):
        ix = VX + 60 + ((i*87 + int(t*20)) % (VW - 120))
        iy = VY + 80 + ((i*53) % 100)
        col = (50 + i*15, 100, 200 - i*8)
        d.text((ix, iy), 'i', font=F('serif-it', 24, True), fill=col)

def vis_number(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    px, py = 2.5, 1.8
    x, y = plot(px, py)
    # dashed projections
    for px2 in range(int(CY), int(y), -8):
        d.line([(x, max(y, px2-3)), (x, max(y, px2-3+4))], fill=(120, 130, 150), width=1)
    for px2 in range(int(CX), int(x), 8):
        d.line([(min(x, px2), y), (min(x, px2+4), y)], fill=(120, 130, 150), width=1)
    # axis labels
    d.text((x - 30, CY + 8), 'x = 2.5', font=F('serif', 16, True), fill=(220, 38, 38))
    d.text((CX + 8, y - 8), 'y = 1.8', font=F('serif', 16, True), fill=(220, 38, 38))
    # point with pulse
    pulse = 8 + int(2 * math.sin(t*3))
    d.ellipse([x-pulse, y-pulse, x+pulse, y+pulse], fill=(220, 38, 38))
    # label
    d.text((x + 14, y - 22), 'z = 2.5 + 1.8i', font=F('serif', 22, True), fill=(30, 41, 59))

def vis_plane(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    ax, ay = plot(2, 1)
    bx, by = plot(1, 2)
    sx, sy = plot(3, 3)
    draw_arrow(d, CX, CY, ax, ay, (59, 130, 246))
    draw_arrow(d, CX, CY, bx, by, (16, 185, 129))
    # parallelogram dashed
    for px2 in range(0, int(((sx-ax)**2 + (sy-ay)**2)**0.5), 8):
        ratio = px2 / max(1, ((sx-ax)**2 + (sy-ay)**2)**0.5)
        d.line([(ax + (sx-ax)*ratio, ay + (sy-ay)*ratio),
                (ax + (sx-ax)*(min(1,ratio + 0.05)), ay + (sy-ay)*(min(1, ratio + 0.05)))],
               fill=(150, 160, 180), width=1)
    draw_arrow(d, CX, CY, sx, sy, (220, 38, 38), width=4)
    d.text((ax+10, ay-30), 'z₁ = 2+i', font=F('serif', 18, True), fill=(59, 130, 246))
    d.text((bx-100, by+10), 'z₂ = 1+2i', font=F('serif', 18, True), fill=(16, 185, 129))
    d.text((sx+10, sy-30), 'z₁+z₂ = 3+3i', font=F('serif', 18, True), fill=(220, 38, 38))

def vis_modulus(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    px, py = 3, 2
    x, y = plot(px, py)
    draw_arrow(d, CX, CY, x, y, (220, 38, 38), width=4)
    # length label
    d.text((int((CX+x)/2)+12, int((CY+y)/2)-30), '|z| = √13',
           font=F('serif', 24, True), fill=(30, 41, 59))
    # projections (dashed)
    seg = 8
    yy = CY
    safety = 0
    while yy > y and safety < 200:
        d.line([(x, yy), (x, max(y, yy-4))], fill=(120, 130, 150), width=1)
        yy -= seg
        safety += 1
    xx = CX
    safety = 0
    while xx < x and safety < 200:
        d.line([(xx, CY), (min(x, xx+4), CY)], fill=(120, 130, 150), width=1)
        xx += seg
        safety += 1
    d.text((int((CX+x)/2) - 10, CY + 10), 'x', font=F('serif-it', 18), fill=(80, 90, 110))
    d.text((x + 10, int((CY+y)/2)), 'y', font=F('serif-it', 18), fill=(80, 90, 110))
    d.ellipse([x-7, y-7, x+7, y+7], fill=(220, 38, 38))
    d.text((x+12, y-30), 'z = 3+2i', font=F('serif', 18, True), fill=(30, 41, 59))

def vis_conjugate(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    px, py = 2.5, 2
    x, y = plot(px, py)
    x2, y2 = plot(px, -py)
    # original
    d.ellipse([x-9, y-9, x+9, y+9], fill=(220, 38, 38))
    d.text((x+12, y-25), 'z', font=F('serif', 22, True), fill=(220, 38, 38))
    # reflected
    d.ellipse([x2-9, y2-9, x2+9, y2+9], fill=(59, 130, 246))
    d.text((x2+12, y2+8), 'z̄', font=F('serif', 22, True), fill=(59, 130, 246))
    # dashed line
    yy = y
    while yy < y2:
        d.line([(x, yy), (x, min(y2, yy+5))], fill=(120, 130, 150), width=1)
        yy += 8
    sub = 'reflection across the real axis'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-50), sub, font=F('serif-it', 18), fill=(30, 41, 59))

def vis_polar(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    r = 2.5
    theta = math.pi/4 + 0.2*math.sin(t)
    x = CX + int(r*SCALE*math.cos(theta))
    y = CY - int(r*SCALE*math.sin(theta))
    # arc for theta
    d.arc([CX-50, CY-50, CX+50, CY+50], start=-math.degrees(theta), end=0,
          fill=(16, 185, 129), width=3)
    # r line
    draw_arrow(d, CX, CY, x, y, (220, 38, 38), width=4)
    # labels
    d.text((CX+58, CY-25), 'θ', font=F('serif', 22, True), fill=(16, 185, 129))
    d.text((int((CX+x)/2)+10, int((CY+y)/2)-15), 'r', font=F('serif', 22, True), fill=(220, 38, 38))
    d.text((x+12, y-30), 'z = re^(iθ)', font=F('serif', 22, True), fill=(30, 41, 59))
    d.ellipse([x-7, y-7, x+7, y+7], fill=(220, 38, 38))

def vis_euler(d, t):
    fill_panel(d)
    draw_axes(d, label=False)
    # unit circle
    d.ellipse([CX-SCALE, CY-SCALE, CX+SCALE, CY+SCALE], outline=(59, 130, 246), width=3)
    theta = (t * 0.7) % (2*math.pi)
    x = CX + int(SCALE*math.cos(theta))
    y = CY - int(SCALE*math.sin(theta))
    draw_arrow(d, CX, CY, x, y, (220, 38, 38), width=3)
    # projections (dashed)
    direction = -1 if y < CY else 1
    yy = CY
    safety = 0
    while abs(yy - y) > 8 and safety < 200:
        d.line([(x, yy), (x, yy + 4*direction)], fill=(120, 130, 150), width=1)
        yy += 8 * direction
        safety += 1
    direction = 1 if x > CX else -1
    xx = CX
    safety = 0
    while abs(xx - x) > 8 and safety < 200:
        d.line([(xx, y), (xx + 4*direction, y)], fill=(120, 130, 150), width=1)
        xx += 8 * direction
        safety += 1
    d.ellipse([x-7, y-7, x+7, y+7], fill=(220, 38, 38))
    d.text((x+12, y-30), 'e^(iθ)', font=F('serif', 18, True), fill=(30, 41, 59))
    # big formula
    txt = 'e^(iθ) = cos θ + i sin θ'
    bb = d.textbbox((0,0), txt, font=F('serif', 26, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-50), txt, font=F('serif', 26, True), fill=(30, 41, 59))

def vis_multiply(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    phase = (t * 0.5)
    r1, t1 = 1.2, 0.5
    r2, t2 = 1.1, 0.8 + 0.5*math.sin(phase)
    r3, t3 = r1*r2, t1+t2
    x1, y1 = CX + int(r1*SCALE*math.cos(t1)), CY - int(r1*SCALE*math.sin(t1))
    x2, y2 = CX + int(r2*SCALE*math.cos(t2)), CY - int(r2*SCALE*math.sin(t2))
    x3, y3 = CX + int(r3*SCALE*math.cos(t3)), CY - int(r3*SCALE*math.sin(t3))
    draw_arrow(d, CX, CY, x1, y1, (59, 130, 246), width=3)
    draw_arrow(d, CX, CY, x2, y2, (16, 185, 129), width=3)
    draw_arrow(d, CX, CY, x3, y3, (220, 38, 38), width=4)
    d.text((x1+8, y1-25), 'z₁', font=F('serif', 18, True), fill=(59, 130, 246))
    d.text((x2+8, y2-25), 'z₂', font=F('serif', 18, True), fill=(16, 185, 129))
    d.text((x3+8, y3-25), 'z₁·z₂', font=F('serif', 18, True), fill=(220, 38, 38))
    sub = 'multiply moduli, add angles'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 20))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-50), sub, font=F('serif-it', 20), fill=(30, 41, 59))

def vis_roots(d, t):
    fill_panel(d)
    draw_axes(d, label=False)
    R = int(SCALE*1.6)
    d.ellipse([CX-R, CY-R, CX+R, CY+R], outline=(200, 210, 220), width=2)
    # pentagon
    pts = []
    for k in range(5):
        theta = 2*math.pi*k/5 + math.pi/2
        px = CX + int(R*math.cos(theta))
        py = CY - int(R*math.sin(theta))
        pts.append((px, py))
    d.line(pts + [pts[0]], fill=(59, 130, 246), width=2)
    for k, (px, py) in enumerate(pts):
        pulse = 9 + int(3*math.sin(t*2 + k))
        col_hue = k * 72
        # simple HSL to RGB approximation
        if col_hue < 60: c = (255, int(255*col_hue/60), 80)
        elif col_hue < 120: c = (int(255*(120-col_hue)/60), 255, 80)
        elif col_hue < 180: c = (80, 255, int(255*(col_hue-120)/60))
        elif col_hue < 240: c = (80, int(255*(240-col_hue)/60), 255)
        elif col_hue < 300: c = (int(255*(col_hue-240)/60), 80, 255)
        else: c = (255, 80, int(255*(360-col_hue)/60))
        d.ellipse([px-pulse, py-pulse, px+pulse, py+pulse], fill=c)
    sub = '5 fifth roots of unity'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 20))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-50), sub, font=F('serif-it', 20), fill=(30, 41, 59))

def vis_func(d, t):
    fill_panel(d)
    sq = 200
    lx = VX + 60
    ly = CY - sq//2
    rx = VX + VW - 60 - sq
    ry = CY - sq//2
    d.rectangle([lx, ly, lx+sq, ly+sq], outline=(59, 130, 246), width=2)
    d.text((lx + sq//2 - 60, ly - 28), 'z plane (input)', font=F('serif', 18, True), fill=(59, 130, 246))
    d.rectangle([rx, ry, rx+sq, ry+sq], outline=(16, 185, 129), width=2)
    d.text((rx + sq//2 - 70, ry - 28), 'w plane (output)', font=F('serif', 18, True), fill=(16, 185, 129))
    # animated point
    phase = t * 0.7
    px_, py_ = math.cos(phase) * 0.6, math.sin(phase) * 0.6
    lpx = lx + sq//2 + int(px_*70)
    lpy = ly + sq//2 - int(py_*70)
    rsq = (px_*px_ + py_*py_)
    rth = math.atan2(py_, px_)
    wpx = rsq*math.cos(2*rth)
    wpy = rsq*math.sin(2*rth)
    rpx = rx + sq//2 + int(wpx*120)
    rpy = ry + sq//2 - int(wpy*120)
    d.ellipse([lpx-9, lpy-9, lpx+9, lpy+9], fill=(220, 38, 38))
    d.ellipse([rpx-9, rpy-9, rpx+9, rpy+9], fill=(220, 38, 38))
    # arrow between
    draw_arrow(d, lx + sq + 10, ly + sq//2, rx - 10, ry + sq//2, (75, 85, 105), width=3)
    d.text(((lx+sq+rx)//2 - 5, ly + sq//2 - 35), 'f', font=F('serif', 22, True), fill=(30, 41, 59))
    sub = 'example: f(z) = z²'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 18), fill=(75, 85, 105))

def vis_derivative(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    zx, zy = plot(0.5, 0.5)
    d.ellipse([zx-7, zy-7, zx+7, zy+7], fill=(30, 41, 59))
    d.text((zx+10, zy-25), 'z₀', font=F('serif', 20, True), fill=(30, 41, 59))
    k = int(t*3) % 8
    for i in range(8):
        ang = i * math.pi / 4
        active = i == k
        length = 70 + (8 if active else 0)
        ex = zx + int(length*math.cos(ang))
        ey = zy + int(length*math.sin(ang))
        col = (220, 38, 38) if active else (140, 150, 170)
        sx_, sy_ = zx + int(14*math.cos(ang)), zy + int(14*math.sin(ang))
        draw_arrow(d, ex, ey, sx_, sy_, col, width=3 if active else 1)
    sub = 'Δz → 0 from any direction — limit must agree'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 18), fill=(30, 41, 59))

def vis_cr(d, t):
    fill_panel(d)
    title = 'Cauchy-Riemann Equations'
    bb = d.textbbox((0,0), title, font=F('serif', 32, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+50), title, font=F('serif', 32, True), fill=(30, 41, 59))
    # eq 1
    s = 1 + 0.04*math.sin(t*2)
    fsz = int(56 * s)
    eq1 = 'u_x = v_y'
    bb = d.textbbox((0,0), eq1, font=F('serif', fsz, True))
    d.text((CX-(bb[2]-bb[0])//2, CY-50), eq1, font=F('serif', fsz, True), fill=(30, 41, 59))
    eq2 = 'u_y = -v_x'
    fsz2 = int(56 * (1 + 0.04*math.cos(t*2)))
    bb = d.textbbox((0,0), eq2, font=F('serif', fsz2, True))
    d.text((CX-(bb[2]-bb[0])//2, CY+30), eq2, font=F('serif', fsz2, True), fill=(30, 41, 59))
    sub = 'the fingerprint of complex differentiability'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 22))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-60), sub, font=F('serif-it', 22), fill=(220, 38, 38))

def vis_analytic(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    zx, zy = plot(0.8, 0.8)
    r = 100 + int(5*math.sin(t*1.5))
    d.ellipse([zx-r, zy-r, zx+r, zy+r], fill=(220, 235, 255), outline=(59, 130, 246), width=3)
    d.ellipse([zx-7, zy-7, zx+7, zy+7], fill=(30, 41, 59))
    d.text((zx+10, zy-25), 'z₀', font=F('serif', 18, True), fill=(30, 41, 59))
    sub = 'analytic = differentiable in an OPEN neighborhood'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 20))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 20), fill=(30, 41, 59))

def vis_compare(d, t):
    fill_panel(d)
    title = 'Real vs Complex Differentiability'
    bb = d.textbbox((0,0), title, font=F('serif', 28, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+30), title, font=F('serif', 28, True), fill=(30, 41, 59))
    lx = VX + VW//4
    rx = VX + 3*VW//4
    d.text((lx-70, VY+90), 'Real (R → R)', font=F('serif', 22, True), fill=(220, 38, 38))
    d.text((rx-90, VY+90), 'Complex (C → C)', font=F('serif', 22, True), fill=(16, 185, 129))
    real_facts = ['• differentiable not C-infinity', '• bounded not constant', '• |x| not differentiable', '• no Fund Thm Algebra']
    cx_facts = ['+ analytic implies C-infinity', '+ bounded entire is constant', '+ analytic = Taylor series', '+ every poly factors fully']
    for i, f in enumerate(real_facts):
        d.text((lx-130, VY+140+i*45), f, font=F('sans', 17), fill=(75, 85, 105))
    for i, f in enumerate(cx_facts):
        d.text((rx-150, VY+140+i*45), f, font=F('sans', 17), fill=(6, 95, 70))
    # divider
    d.line([(CX, VY+110), (CX, VY+VH-50)], fill=(200, 210, 220), width=2)

def vis_exp(d, t):
    fill_panel(d)
    draw_axes(d, label=False)
    # periodic strips
    for k in range(-2, 3):
        y = CY - int(k*SCALE*math.pi/2)
        if VY+30 <= y <= VY+VH-30:
            alpha = int(80 + 60*abs(math.sin(t*0.5 + k)))
            d.rectangle([VX+30, y-int(SCALE*math.pi/4), VX+VW-30, y+int(SCALE*math.pi/4)],
                        fill=(220, 235, 255))
    draw_grid(d)
    draw_axes(d)
    # arrows showing periodicity
    for k in range(-1, 2):
        y = CY - int(k*SCALE*math.pi/2)
        d.line([(CX-30, y), (CX+30, y)], fill=(220, 38, 38), width=3)
    txt = 'e^(z+2πi) = e^z'
    bb = d.textbbox((0,0), txt, font=F('serif', 24, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+50), txt, font=F('serif', 24, True), fill=(30, 41, 59))
    sub = 'e^z is periodic with period 2πi'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 18), fill=(220, 38, 38))

def vis_log(d, t):
    fill_panel(d)
    draw_axes(d, label=False)
    # left point z
    zx, zy = plot(2, 0)
    d.ellipse([zx-9, zy-9, zx+9, zy+9], fill=(220, 38, 38))
    d.text((zx+12, zy-30), 'z', font=F('serif', 18, True), fill=(30, 41, 59))
    # right column of log values
    for n in range(-2, 3):
        cy_ = CY + n*45
        col = (50 + (n+2)*40, 100 + n*30, 180)
        d.ellipse([VX+VW-200-7, cy_-7, VX+VW-200+7, cy_+7], fill=col)
        txt = f'log r + {2*n}πi'
        d.text((VX+VW-185, cy_-9), txt, font=F('mono', 16), fill=(30, 41, 59))
        # dashed connector
        ratio = 0
        while ratio < 1:
            x1 = zx + (VX+VW-200-zx) * ratio
            y1 = zy + (cy_-zy) * ratio
            x2 = zx + (VX+VW-200-zx) * min(1, ratio + 0.04)
            y2 = zy + (cy_-zy) * min(1, ratio + 0.04)
            d.line([(x1, y1), (x2, y2)], fill=(150, 160, 180), width=1)
            ratio += 0.08
    sub = 'log z is multi-valued'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 20))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 20), fill=(30, 41, 59))

def vis_branch(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    # branch cut on negative real axis
    d.line([(VX+30, CY), (CX, CY)], fill=(220, 38, 38), width=5)
    # hatching
    x = VX+50
    while x < CX:
        d.line([(x, CY-8), (x+6, CY+8)], fill=(220, 38, 38), width=2)
        x += 10
    # moving point
    ang = math.sin(t*0.6) * 0.8 + 0.6
    r = 2
    px = CX + int(r*SCALE*math.cos(ang))
    py = CY - int(r*SCALE*math.sin(ang))
    draw_arrow(d, CX, CY, px, py, (16, 185, 129), width=3)
    d.ellipse([px-7, py-7, px+7, py+7], fill=(16, 185, 129))
    d.text(((VX+30+CX)//2 - 60, CY+15), 'branch cut', font=F('serif', 18, True), fill=(220, 38, 38))
    sub = 'slit plane: principal log is analytic here'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 20))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 20), fill=(30, 41, 59))

def vis_contour(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    # wavy curve
    pts = []
    for s in range(0, 101):
        s_ = s / 100
        x_ = -2 + 4*s_
        y_ = 0.5 + math.sin(s_*math.pi*3) * 1.2
        pts.append(plot(x_, y_))
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill=(59, 130, 246), width=3)
    # moving point
    s = (t*0.18) % 1
    x_ = -2 + 4*s
    y_ = 0.5 + math.sin(s*math.pi*3) * 1.2
    px, py = plot(x_, y_)
    d.ellipse([px-9, py-9, px+9, py+9], fill=(220, 38, 38))
    d.text((px+12, py-25), 'z(t)', font=F('serif', 18, True), fill=(30, 41, 59))
    sub = 'contour C: z(t) for t in [a, b]'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 20))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 20), fill=(59, 130, 246))

def vis_goursat(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    # closed wavy loop
    N = 80
    pts = []
    for i in range(N+1):
        theta = 2*math.pi*i/N
        r_ = 1.7 + 0.25*math.sin(theta*3)
        pts.append(plot(r_*math.cos(theta), r_*math.sin(theta)))
    d.polygon(pts, fill=(220, 252, 231), outline=(59, 130, 246))
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill=(59, 130, 246), width=3)
    # text in middle
    txt = '∮ f(z) dz = 0'
    bb = d.textbbox((0,0), txt, font=F('serif', 38, True))
    d.text((CX-(bb[2]-bb[0])//2, CY-25), txt, font=F('serif', 38, True), fill=(6, 95, 70))
    sub = 'f analytic inside → integral around loop = 0'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 18), fill=(30, 41, 59))

def vis_oneoverz(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    # red dot at origin (X mark)
    d.line([(CX-14, CY-14), (CX+14, CY+14)], fill=(220, 38, 38), width=3)
    d.line([(CX-14, CY+14), (CX+14, CY-14)], fill=(220, 38, 38), width=3)
    d.ellipse([CX-9, CY-9, CX+9, CY+9], fill=(220, 38, 38))
    # loop
    R = 130
    d.ellipse([CX-R, CY-R, CX+R, CY+R], outline=(59, 130, 246), width=3)
    # moving point with arrow
    ang = t * 0.8
    px = CX + int(R*math.cos(ang))
    py = CY - int(R*math.sin(ang))
    d.ellipse([px-8, py-8, px+8, py+8], fill=(220, 38, 38))
    # formula
    txt = '∮ dz/z = 2πi'
    bb = d.textbbox((0,0), txt, font=F('serif', 32, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-90), txt, font=F('serif', 32, True), fill=(30, 41, 59))
    sub = 'for ANY simple closed loop around 0'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 18), fill=(75, 85, 105))

def vis_cif(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    # closed loop
    N = 80
    pts = []
    for i in range(N+1):
        theta = 2*math.pi*i/N
        r_ = 1.6 + 0.2*math.cos(theta*4)
        pts.append(plot(r_*math.cos(theta), r_*math.sin(theta)))
    d.polygon(pts, fill=(235, 245, 255))
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill=(59, 130, 246), width=3)
    # z0 inside, glowing
    zx, zy = plot(0.3, 0.4)
    glow_r = 12 + int(3*math.sin(t*3))
    d.ellipse([zx-glow_r, zy-glow_r, zx+glow_r, zy+glow_r], fill=(255, 200, 200))
    d.ellipse([zx-7, zy-7, zx+7, zy+7], fill=(220, 38, 38))
    d.text((zx-7, zy-30), 'z₀', font=F('serif', 18, True), fill=(30, 41, 59))
    sub = 'value inside = average of values on boundary'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 18), fill=(30, 41, 59))

def vis_derivatives(d, t):
    fill_panel(d)
    title = 'Analytic → all derivatives exist'
    bb = d.textbbox((0,0), title, font=F('serif', 30, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+50), title, font=F('serif', 30, True), fill=(30, 41, 59))
    labels = ['f(z)', "f'(z)", "f''(z)", "f'''(z)", "f''''(z)", '...', 'f^(n)(z)']
    phase = int(t*1.2) % len(labels)
    for i, lab in enumerate(labels):
        y = VY + 130 + i*42
        active = i <= phase
        col = (59, 130, 246) if active else (200, 210, 220)
        sz = max(18, 28 - i*1)
        bb = d.textbbox((0,0), lab, font=F('serif', sz, True))
        d.text((CX-(bb[2]-bb[0])//2, y), lab, font=F('serif', sz, True), fill=col)
        if active and i < len(labels) - 1:
            d.text((CX-5, y + sz + 4), '↓', font=F('serif', 18), fill=(220, 38, 38))
    sub = 'and all of them are analytic too!'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-30), sub, font=F('serif-it', 18), fill=(75, 85, 105))

def vis_liouville(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    # bounded region
    d.ellipse([CX-200, CY-200, CX+200, CY+200], fill=(255, 220, 220), outline=(220, 38, 38), width=2)
    # dots scattered inside
    for i in range(30):
        ang = i * 0.7 + t * 0.3
        r_ = 30 + 130 * abs(math.sin(i*1.7 + t*0.5))
        px = CX + int(r_*math.cos(ang))
        py = CY + int(r_*math.sin(ang))
        # color based on i
        h = (i*15) % 360
        if h < 60: c = (255, int(255*h/60), 80)
        elif h < 120: c = (int(255*(120-h)/60), 255, 80)
        elif h < 180: c = (80, 255, int(255*(h-120)/60))
        elif h < 240: c = (80, int(255*(240-h)/60), 255)
        elif h < 300: c = (int(255*(h-240)/60), 80, 255)
        else: c = (255, 80, int(255*(360-h)/60))
        d.ellipse([px-5, py-5, px+5, py+5], fill=c)
    txt = '|f| ≤ M everywhere'
    bb = d.textbbox((0,0), txt, font=F('serif', 28, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+50), txt, font=F('serif', 28, True), fill=(30, 41, 59))
    sub = 'then f must be CONSTANT'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 22, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 22, True), fill=(220, 38, 38))

def vis_fta(d, t):
    fill_panel(d)
    title = 'Fundamental Theorem of Algebra'
    bb = d.textbbox((0,0), title, font=F('serif', 28, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+30), title, font=F('serif', 28, True), fill=(30, 41, 59))
    phase = (t * 0.4) % 2
    if phase < 1:
        eq = 'P(z) = z⁴ - 1'
        col = (30, 41, 59)
    else:
        eq = '= (z-1)(z+1)(z-i)(z+i)'
        col = (59, 130, 246)
    bb = d.textbbox((0,0), eq, font=F('serif', 32, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+90), eq, font=F('serif', 32, True), fill=col)
    draw_axes(d, label=False)
    r_ = 1.5
    angles = [0, math.pi/2, math.pi, 3*math.pi/2]
    labels = ['1', 'i', '-1', '-i']
    for i, th in enumerate(angles):
        px = CX + int(r_*SCALE*math.cos(th))
        py = CY - int(r_*SCALE*math.sin(th))
        h = i * 90
        if h == 0: c = (255, 80, 80)
        elif h == 90: c = (80, 255, 80)
        elif h == 180: c = (80, 80, 255)
        else: c = (200, 100, 200)
        d.ellipse([px-10, py-10, px+10, py+10], fill=c)
        d.text((px + int(20*math.cos(th)) - 5, py - int(20*math.sin(th)) - 8),
               labels[i], font=F('serif', 18, True), fill=(30, 41, 59))
    sub = 'every poly factors completely in C'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 18), fill=(75, 85, 105))

def vis_series(d, t):
    fill_panel(d)
    draw_axes(d, label=False)
    R = 130
    d.ellipse([CX-R, CY-R, CX+R, CY+R], fill=(220, 235, 255), outline=(59, 130, 246), width=3)
    d.ellipse([CX-7, CY-7, CX+7, CY+7], fill=(220, 38, 38))
    d.text((CX+12, CY-5), 'z₀', font=F('serif', 18, True), fill=(30, 41, 59))
    txt = 'f(z) = a₀ + a₁(z-z₀) + a₂(z-z₀)² + ...'
    bb = d.textbbox((0,0), txt, font=F('serif', 22, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+50), txt, font=F('serif', 22, True), fill=(30, 41, 59))
    sub1 = 'converges in disk |z-z₀| < R'
    bb = d.textbbox((0,0), sub1, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-60), sub1, font=F('serif-it', 18), fill=(59, 130, 246))
    sub2 = 'R = radius of convergence'
    bb = d.textbbox((0,0), sub2, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-30), sub2, font=F('serif-it', 18), fill=(220, 38, 38))

def vis_singularities(d, t):
    fill_panel(d)
    title = 'Three types of isolated singularities'
    bb = d.textbbox((0,0), title, font=F('serif', 26, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+40), title, font=F('serif', 26, True), fill=(30, 41, 59))
    types = [
        (VX + VW//6, 'Removable', 'no neg powers', '(sin z)/z', (16, 185, 129)),
        (CX, 'Pole order m', 'finite neg powers', '1/(z-z₀)^m', (245, 158, 11)),
        (VX + 5*VW//6, 'Essential', '∞ neg powers', 'e^(1/z)', (220, 38, 38))
    ]
    for i, (x_, name, desc, ex, col) in enumerate(types):
        bb = d.textbbox((0,0), name, font=F('serif', 22, True))
        d.text((x_-(bb[2]-bb[0])//2, VY+110), name, font=F('serif', 22, True), fill=col)
        bb = d.textbbox((0,0), desc, font=F('sans', 16))
        d.text((x_-(bb[2]-bb[0])//2, VY+145), desc, font=F('sans', 16), fill=(75, 85, 105))
        # dot pulsing
        pulse = 14 + int(4*math.sin(t*2 + i))
        d.ellipse([x_-pulse, VY+205-pulse, x_+pulse, VY+205+pulse], fill=col)
        bb = d.textbbox((0,0), ex, font=F('serif-it', 18))
        d.text((x_-(bb[2]-bb[0])//2, VY+260), ex, font=F('serif-it', 18), fill=(30, 41, 59))
    sub = 'classified by principal part of Laurent series'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), sub, font=F('serif-it', 18), fill=(75, 85, 105))

def vis_residue(d, t):
    fill_panel(d)
    title = 'Laurent series at singularity z₀:'
    bb = d.textbbox((0,0), title, font=F('serif', 24, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+50), title, font=F('serif', 24, True), fill=(30, 41, 59))
    eq1 = 'f(z) = a₀ + a₁(z-z₀) + a₂(z-z₀)² + ...'
    bb = d.textbbox((0,0), eq1, font=F('serif', 22, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+130), eq1, font=F('serif', 22, True), fill=(30, 41, 59))
    # highlighted residue term
    flash = 0.7 + 0.3*math.sin(t*3)
    col = (int(220*flash), int(38*flash), int(38*flash))
    eq2 = '+ b₁/(z-z₀)'
    bb = d.textbbox((0,0), eq2, font=F('serif', 32, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+200), eq2, font=F('serif', 32, True), fill=(220, 38, 38))
    eq3 = '+ b₂/(z-z₀)² + b₃/(z-z₀)³ + ...'
    bb = d.textbbox((0,0), eq3, font=F('serif', 22, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+270), eq3, font=F('serif', 22, True), fill=(30, 41, 59))
    arrow = '↑ THIS is the residue'
    bb = d.textbbox((0,0), arrow, font=F('serif-it', 24, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+340), arrow, font=F('serif-it', 24, True), fill=(220, 38, 38))
    formula = 'Res_{z=z₀} f = b₁'
    bb = d.textbbox((0,0), formula, font=F('serif', 20, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-50), formula, font=F('serif', 20, True), fill=(75, 85, 105))

def vis_rt(d, t):
    fill_panel(d)
    draw_grid(d)
    draw_axes(d)
    # closed loop
    N = 80
    pts = []
    for i in range(N+1):
        theta = 2*math.pi*i/N
        r_ = 1.9 + 0.3*math.cos(theta*5)
        pts.append(plot(r_*math.cos(theta), r_*math.sin(theta)))
    d.polygon(pts, fill=(235, 245, 255))
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill=(59, 130, 246), width=3)
    # singularities
    sings = [(-0.6, 0.7), (0.8, 0.3), (0.1, -0.7)]
    for i, (sx, sy) in enumerate(sings):
        px, py = plot(sx, sy)
        pulse = 1 + 0.4*math.sin(t*2 + i)
        rr = int(8*pulse)
        d.ellipse([px-rr, py-rr, px+rr, py+rr], fill=(220, 38, 38))
        d.line([(px-12, py-12), (px+12, py+12)], fill=(220, 38, 38), width=2)
        d.line([(px-12, py+12), (px+12, py-12)], fill=(220, 38, 38), width=2)
        d.text((px-22, py-32), f'Res {i+1}', font=F('serif', 14, True), fill=(30, 41, 59))
    formula = '∮_C f dz = 2πi · (Res₁ + Res₂ + Res₃)'
    bb = d.textbbox((0,0), formula, font=F('serif', 22, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-40), formula, font=F('serif', 22, True), fill=(30, 41, 59))

def vis_realint(d, t):
    fill_panel(d)
    draw_axes(d)
    # real line and semicircle UHP
    d.line([(VX+30, CY), (VX+VW-30, CY)], fill=(59, 130, 246), width=3)
    R = 250
    d.arc([CX-R, CY-R, CX+R, CY+R], start=180, end=360, fill=(59, 130, 246), width=3)
    # singularities in UHP
    sings = [(-1.4, 1.0), (0, 1.5), (1.4, 1.0)]
    for i, (sx, sy) in enumerate(sings):
        px, py = plot(sx, sy)
        pulse = 1 + 0.3*math.sin(t*2 + i)
        rr = int(9*pulse)
        d.ellipse([px-rr, py-rr, px+rr, py+rr], fill=(220, 38, 38))
    txt = '∫₀^∞ dx/(x⁶+1) = π/3'
    bb = d.textbbox((0,0), txt, font=F('serif', 26, True))
    d.text((CX-(bb[2]-bb[0])//2, VY+50), txt, font=F('serif', 26, True), fill=(30, 41, 59))
    sub = 'extend to UHP semicircle, sum residues'
    bb = d.textbbox((0,0), sub, font=F('serif-it', 16))
    d.text((CX-(bb[2]-bb[0])//2, VY+VH-30), sub, font=F('serif-it', 16), fill=(75, 85, 105))

def vis_closing(d, t):
    d.rounded_rectangle([VX, VY, VX+VW, VY+VH], radius=12, fill=(15, 23, 42))
    # sparkles
    for i in range(80):
        x = VX + ((i*113 + int(t*60)) % VW)
        y = VY + ((i*71) % VH)
        r = max(1, int(2 + 2*abs(math.sin(t + i))))
        bright = int(150 + 100*abs(math.sin(t*3 + i)))
        c = ((i*13) % 256, bright, (255 - (i*7) % 256))
        d.ellipse([x-r, y-r, x+r, y+r], fill=c)
    title = 'You did it!'
    wobble = int(math.sin(t) * 4)
    bb = d.textbbox((0,0), title, font=F('serif', 60, True))
    d.text((CX-(bb[2]-bb[0])//2, CY-60+wobble), title, font=F('serif', 60, True), fill=(251, 191, 36))
    sub = 'Good luck on your final.'
    bb = d.textbbox((0,0), sub, font=F('serif', 24))
    d.text((CX-(bb[2]-bb[0])//2, CY+30), sub, font=F('serif', 24), fill=(220, 230, 245))
    sub2 = '— Your AI tutor'
    bb = d.textbbox((0,0), sub2, font=F('serif-it', 18))
    d.text((CX-(bb[2]-bb[0])//2, CY+80), sub2, font=F('serif-it', 18), fill=(150, 160, 180))

VISUALS = {
    'title': vis_title, 'imaginary': vis_imaginary, 'number': vis_number,
    'plane': vis_plane, 'modulus': vis_modulus, 'conjugate': vis_conjugate,
    'polar': vis_polar, 'euler': vis_euler, 'multiply': vis_multiply,
    'roots': vis_roots, 'func': vis_func, 'derivative': vis_derivative,
    'cr': vis_cr, 'analytic': vis_analytic, 'compare': vis_compare,
    'exp': vis_exp, 'log': vis_log, 'branch': vis_branch,
    'contour': vis_contour, 'goursat': vis_goursat, 'oneoverz': vis_oneoverz,
    'cif': vis_cif, 'derivatives': vis_derivatives, 'liouville': vis_liouville,
    'fta': vis_fta, 'series': vis_series, 'singularities': vis_singularities,
    'residue': vis_residue, 'rt': vis_rt, 'realint': vis_realint,
    'closing': vis_closing,
}

# ============== FRAME COMPOSE ==============
def render_frame(scene_idx, t_in_scene):
    img = Image.new('RGB', (W, H), (15, 23, 42))
    d = ImageDraw.Draw(img)
    sc = SCENES[scene_idx]
    # top bar
    d.rectangle([0, 0, W, TOPBAR_H], fill=(30, 41, 59))
    d.text((24, 17), 'Complex Analysis — AI Tutor',
           font=F('serif', 20, True), fill=(251, 191, 36))
    title_text = f"Scene {scene_idx+1}/{len(SCENES)}: {sc['title']}"
    tb = d.textbbox((0,0), title_text, font=F('sans', 14))
    d.text((W - (tb[2]-tb[0]) - 24, 21), title_text, font=F('sans', 14), fill=(160, 170, 190))
    # left panel bg
    d.rounded_rectangle([AVA_X, AVA_Y, AVA_X + AVA_W, AVA_Y + AVA_H], radius=12,
                        fill=(30, 41, 59))
    draw_avatar(d, t_in_scene, speaking=True)
    # caption box
    d.rounded_rectangle([CAP_X, CAP_Y, CAP_X + CAP_W, CAP_Y + CAP_H], radius=12,
                        fill=(30, 41, 59))
    d.text((CAP_X + 16, CAP_Y + 14), 'NARRATION',
           font=F('sans', 11, True), fill=(251, 191, 36))
    # wrap text
    text = sc['text']
    wrap_width = CAP_W - 32
    words = text.split()
    lines = []
    cur = ''
    f_cap = F('sans', 15)
    for w in words:
        test = (cur + ' ' + w).strip()
        bb = d.textbbox((0,0), test, font=f_cap)
        if bb[2] - bb[0] > wrap_width:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur: lines.append(cur)
    for i, ln in enumerate(lines[:14]):
        d.text((CAP_X + 16, CAP_Y + 40 + i*22), ln, font=f_cap, fill=(220, 230, 245))
    # right side: visual
    visual_fn = VISUALS.get(sc['visual'])
    if visual_fn:
        visual_fn(d, t_in_scene)
    else:
        fill_panel(d)
        d.text((CX-50, CY-20), sc['title'], font=F('serif', 30, True), fill=(30, 41, 59))
    # formula box
    d.rounded_rectangle([FX, FY, FX + FW, FY + FH], radius=12, fill=(30, 41, 59))
    if sc['formula']:
        # simple text formula
        f_form = F('serif', 28)
        bb = d.textbbox((0,0), sc['formula'], font=f_form)
        cx_ = FX + FW // 2
        cy_ = FY + FH // 2
        d.text((cx_-(bb[2]-bb[0])//2, cy_-(bb[3]-bb[1])//2), sc['formula'],
               font=f_form, fill=(245, 250, 255))
    # bottom bar with progress
    d.rectangle([0, H - BOTBAR_H, W, H], fill=(30, 41, 59))
    # progress bar
    d.rectangle([0, H - BOTBAR_H, W, H - BOTBAR_H + 4], fill=(50, 60, 80))
    return img

# ============== MAIN PIPELINE ==============
def render_video(timings, total_dur):
    print(f"[3/4] Rendering video frames @ {FPS}fps for {total_dur:.1f}s ({int(total_dur*FPS)} frames)...")
    proc = subprocess.Popen([
        'ffmpeg', '-y',
        '-f', 'rawvideo', '-vcodec', 'rawvideo',
        '-s', f'{W}x{H}', '-pix_fmt', 'rgb24',
        '-r', str(FPS),
        '-i', '-',
        '-i', str(BUILD / 'full_audio.mp3'),
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '192k',
        '-shortest',
        '-movflags', '+faststart',
        str(OUT)
    ], stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    total_frames = int(total_dur * FPS)
    last_pct = -1
    for f in range(total_frames):
        t = f / FPS
        # Find which scene
        scene_idx = 0
        for i, (start, end) in enumerate(timings):
            if start <= t <= end + 0.001:
                scene_idx = i
                break
            elif t > end:
                scene_idx = i
        # Time within scene (clamped to scene length to avoid drifting visuals during gap)
        if scene_idx < len(timings):
            t_in_scene = min(t - timings[scene_idx][0], timings[scene_idx][1] - timings[scene_idx][0])
        else:
            t_in_scene = 0
        img = render_frame(scene_idx, max(0, t_in_scene))
        proc.stdin.write(img.tobytes())
        pct = int(f * 100 / total_frames)
        if pct != last_pct and pct % 5 == 0:
            print(f"  {pct}% ({f}/{total_frames})")
            last_pct = pct
    proc.stdin.close()
    err = proc.stderr.read().decode('utf-8', errors='ignore')
    rc = proc.wait()
    if rc != 0:
        print("FFMPEG ERROR:", err[-1500:])
        sys.exit(1)
    print(f"[4/4] Wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")

if __name__ == '__main__':
    asyncio.run(gen_audio())
    print("[2/4] Computing scene timings...")
    timings, total = compute_timings()
    for i, (s, e) in enumerate(timings):
        print(f"  scene {i+1:2d}: {s:6.2f}s -> {e:6.2f}s ({e-s:.2f}s) — {SCENES[i]['title']}")
    print(f"  total duration: {total:.2f}s")
    render_video(timings, total)
