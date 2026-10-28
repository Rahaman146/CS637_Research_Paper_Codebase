import os
from PIL import Image

SLIDES_DIR = "presentation/slides_canva"
OUT_CONTACT = "presentation/contact_sheet.png"

slide_files = sorted([f for f in os.listdir(SLIDES_DIR) if f.startswith("slide_") and f.endswith(".png")])
print(f"Found {len(slide_files)} slides for contact sheet")

# We have 16 slides, make a 4x4 grid
cols = 4
rows = 4

# Scale each slide to 960x540 for the contact sheet
thumb_w = 960
thumb_h = 540

contact_w = cols * thumb_w
contact_h = rows * thumb_h

contact = Image.new("RGB", (contact_w, contact_h), color=(15, 23, 42))

for idx, fname in enumerate(slide_files):
    r = idx // cols
    c = idx % cols
    img_path = os.path.join(SLIDES_DIR, fname)
    im = Image.open(img_path)
    im_thumb = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    contact.paste(im_thumb, (c * thumb_w, r * thumb_h))

contact.save(OUT_CONTACT, "PNG", quality=90)
print(f"Successfully generated contact sheet at {OUT_CONTACT} ({contact_w}x{contact_h})")
