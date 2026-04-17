from PIL import Image, ImageChops
import os

sizes = {
    '16x16': 16,
    '32x32': 32,
    '48x48': 48,
    '180x180': 180,
    '192x192': 192,
    '512x512': 512
}

def generate_favicons(source_path, mode):
    print(f"Generating {mode} mode favicons from {source_path}")
    img = Image.open(source_path)
    
    # Identify non-background content
    bg_color = img.getpixel((0,0))
    bg = Image.new(img.mode, img.size, bg_color)
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    
    if not bbox:
        print("Failed to find content bounds")
        return
        
    cropped = img.crop(bbox)
    
    w, h = cropped.size
    size = max(w, h)
    padding = int(size * 0.1) # 10% padding
    new_size = size + padding * 2
    
    # Create perfect square wrapper
    square_img = Image.new(img.mode, (new_size, new_size), bg_color)
    x_offset = (new_size - w) // 2
    y_offset = (new_size - h) // 2
    square_img.paste(cropped, (x_offset, y_offset))
    
    os.makedirs("assets/favicons", exist_ok=True)
    
    ico_imgs = []
    
    for name, dim in sizes.items():
        resized = square_img.resize((dim, dim), Image.Resampling.LANCZOS)
        filename = f"assets/favicons/favicon-{mode}-{name}.png"
        resized.save(filename)
        print(f"Saved {filename}")
        
        # Keep 16, 32, and 48 for ICO packing
        if dim in [16, 32, 48]:
            ico_imgs.append(resized)
            
    # Save master favicon.ico
    if ico_imgs:
        ico_filename = f"assets/favicons/favicon-{mode}.ico"
        # We need to sort by largest to smallest for PIL ico saving, though PIL handles it
        ico_imgs = sorted(ico_imgs, key=lambda x: x.size[0], reverse=True)
        ico_imgs[0].save(ico_filename, format='ICO', sizes=[(i.size[0], i.size[1]) for i in ico_imgs])
        print(f"Saved {ico_filename}")

generate_favicons("assets/logos/logo.2.jpg", "light")
generate_favicons("assets/logos/logo.8.jpg", "dark")
