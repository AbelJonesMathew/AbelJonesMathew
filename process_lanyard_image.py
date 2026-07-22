import os
import sys
import base64
from datetime import datetime, timedelta

def find_recent_image():
    """
    Searches for PNG/JPG files in the current folder, user's Desktop, and Downloads
    that were modified or created recently (within the last 20 minutes).
    """
    search_dirs = [
        os.getcwd(),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Downloads")
    ]
    
    recent_files = []
    now = datetime.now()
    time_limit = now - timedelta(minutes=20)
    
    for directory in search_dirs:
        if not os.path.exists(directory):
            continue
        try:
            for file in os.listdir(directory):
                if file.lower().endswith(".png") or file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
                    path = os.path.join(directory, file)
                    mtime = datetime.fromtimestamp(os.path.getmtime(path))
                    if mtime > time_limit:
                        recent_files.append((path, mtime))
        except Exception as e:
            print(f"Skipping directory {directory} due to error: {e}")
            
    if not recent_files:
        return None
        
    recent_files.sort(key=lambda x: x[1], reverse=True)
    return recent_files[0][0]

def main():
    print("Starting lanyard image processing script...")
    
    input_path = None
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        print("Scanning for recently added images on Desktop, Downloads, or current folder...")
        input_path = find_recent_image()
        
    if not input_path or not os.path.exists(input_path):
        print("\n[!] Error: No input image found.")
        print("Please drag the lanyard sticker image into this folder and run: ")
        print("   python process_lanyard_image.py <image_filename>")
        return

    print(f"Selected image: {input_path}")
    
    # Load Pillow
    try:
        from PIL import Image
    except ImportError:
        print("\n[!] Required library 'Pillow' is missing. Installing...")
        os.system("pip install pillow opencv-python")
        from PIL import Image

    img_orig = Image.open(input_path)
    W, H = img_orig.size
    face_crop_path = "face_crop_temp.png"
    face_cropped = False
    
    # Try face detection with OpenCV
    try:
        import cv2
        import numpy as np
        
        print("Attempting automatic face detection using OpenCV...")
        cv_img = cv2.imread(input_path)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
            fx, fy, fw, fh = faces[0]
            
            # Expand bounding box slightly for head/hair/neck
            padding_x = int(fw * 0.35)
            padding_y = int(fh * 0.45)
            
            x1 = max(0, fx - padding_x)
            y1 = max(0, fy - padding_y)
            x2 = min(W, fx + fw + padding_x)
            y2 = min(H, fy + fh + padding_y)
            
            # Make it square
            side = min(x2 - x1, y2 - y1)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            x1 = max(0, cx - side // 2)
            y1 = max(0, cy - side // 2)
            x2 = min(W, x1 + side)
            y2 = min(H, y1 + side)
            
            face_box = (x1, y1, x2, y2)
            img_orig.crop(face_box).save(face_crop_path)
            face_cropped = True
            print("Face detected and cropped using OpenCV.")
    except Exception as e:
        print(f"OpenCV face detection skipped/failed: {e}")
        
    if not face_cropped:
        print("Using default crop coordinates customized for a centered avatar...")
        # Since the sticker character is centered in the image
        x_center = W * 0.50
        y_center = H * 0.45
        crop_size = min(W, H) * 0.65
        
        x1 = max(0, int(x_center - crop_size / 2))
        y1 = max(0, int(y_center - crop_size / 2))
        x2 = min(W, int(x_center + crop_size / 2))
        y2 = min(H, int(y_center + crop_size / 2))
        
        img_orig.crop((x1, y1, x2, y2)).save(face_crop_path)
        print("Default crop coordinates applied.")
        
    # Resize face crop to 200x200 and save base64
    img_face = Image.open(face_crop_path)
    img_face = img_face.resize((200, 200), Image.Resampling.LANCZOS)
    img_face.save("face_crop_temp_final.png", format="PNG")
    
    with open("face_crop_temp_final.png", "rb") as image_file:
        face_b64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    with open("face_crop_base64.txt", "w", encoding="utf-8") as f:
        f.write(face_b64)
    print("face_crop_base64.txt successfully updated.")

    # Clean up temp files
    for temp_f in [face_crop_path, "face_crop_temp_final.png"]:
        if os.path.exists(temp_f):
            try:
                os.remove(temp_f)
            except:
                pass
                
    # Run assemble_assets.py to compile SVG assets
    print("\nRunning assemble_assets.py to regenerate SVGs in new theme...")
    import assemble_assets
    assemble_assets.main()
    print("\n[+] SUCCESS! Lanyard badge image updated in lanyard.svg.")

if __name__ == "__main__":
    main()
