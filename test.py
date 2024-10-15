import os
import qrcode
from urllib.parse import quote

def generate_qr_codes(root_folder):
    # File extensions for both videos and images
    valid_extensions = ('.mp4', '.avi', '.mov', '.jpg', '.jpeg', '.png', '.gif', '.bmp')

    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            qr_folder = f"{folder_name}_QR"
            qr_folder_path = os.path.join(root_folder, qr_folder)
            os.makedirs(qr_folder_path, exist_ok=True)

            for filename in os.listdir(folder_path):
                if filename.lower().endswith(valid_extensions):
                    file_path = os.path.join(folder_path, filename)
                    
                    # URL encode the entire path
                    encoded_path = quote(f"{folder_name}/{filename}")
                    url = f"http://localhost:8000/{encoded_path}"

                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(url)
                    qr.make(fit=True)

                    img = qr.make_image(fill='black', back_color='white')
                    qr_filename = f"{os.path.splitext(filename)[0]}_qr.png"
                    qr_file_path = os.path.join(qr_folder_path, qr_filename)
                    img.save(qr_file_path)

# Usage
root_folder = r"C:\Users\PC\Downloads\QR CODE SCANNER"
generate_qr_codes(root_folder)
