import os
from PIL import Image

SLIDES_DIR = "presentation/slides_minimal"
OUT_ROOT = "CS637_Slide_Contact_Sheet.png"
OUT_PRES = "presentation/CS637_Slide_Contact_Sheet.png"

slide_files = sorted([f for f in os.listdir(SLIDES_DIR) if f.startswith("slide_") and f.endswith(".png")])
print(f"Found {len(slide_files)} slides for contact sheet")

# 18 slides arranged in a 6-column x 3-row grid
cols = 6
rows = 3

# Scale each slide to 960x540 for high-resolution readability
thumb_w = 960
thumb_h = 540

contact_w = cols * thumb_w
contact_h = rows * thumb_h

# Crisp white canvas matching Minimal template
contact = Image.new("RGB", (contact_w, contact_h), color=(255, 255, 255))

for idx, fname in enumerate(slide_files):
    r = idx // cols
    c = idx % cols
    img_path = os.path.join(SLIDES_DIR, fname)
    im = Image.open(img_path)
    im_thumb = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    contact.paste(im_thumb, (c * thumb_w, r * thumb_h))

contact.save(OUT_ROOT, "PNG", quality=95)
contact.save(OUT_PRES, "PNG", quality=95)
print(f"Successfully generated contact sheet at {OUT_ROOT} and {OUT_PRES} ({contact_w}x{contact_h})")
