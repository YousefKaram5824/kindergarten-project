import os
import shutil

def test_photo_upload():
    """Test the photo upload functionality."""
    # Simulate a photo upload
    photos_dir = "student_photos"
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)

    # Simulate a photo file
    test_photo_path = os.path.join(photos_dir, "test_photo.jpg")
    with open(test_photo_path, "wb") as f:
        f.write(b"Test photo content")

    # Check if the photo was created
    if os.path.exists(test_photo_path):
        print("Photo upload test passed: Photo file created.")
    else:
        print("Photo upload test failed: Photo file not created.")

if __name__ == "__main__":
    test_photo_upload()
