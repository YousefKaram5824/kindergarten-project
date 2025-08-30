import os
import shutil

UPLOAD_DIR = "uploads/children"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_child_image(file_path: str) -> str:
    """ينسخ الصورة للمجلد ويرجع المسار الجديد"""
    filename = os.path.basename(file_path)
    dest_path = os.path.join(UPLOAD_DIR, filename)
    shutil.copy(file_path, dest_path)
    return dest_path


def delete_child_image(path: str):
    if path and os.path.exists(path):
        os.remove(path)
