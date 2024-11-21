# import cloudinary
# import cloudinary.uploader
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env
# load_dotenv()

# # Configure Cloudinary with environment variables
# cloudinary.config(
#     cloud_name=os.getenv("CLOUD_NAME"),
#     api_key=os.getenv("API_KEY"),
#     api_secret=os.getenv("API_SECRET")
# )

# def test_cloudinary_upload(image_path):
#     try:
#         # Upload the image to Cloudinary
#         response = cloudinary.uploader.upload(image_path)
#         print(f"Image uploaded successfully! URL: {response['secure_url']}")
#     except Exception as e:
#         print(f"Error uploading image: {e}")

# if __name__ == "__main__":
#     # Provide a valid path to an image you want to test with
#     test_image_path = './path/to/your/test/image.jpg'
    
#     # Run the test
#     test_cloudinary_upload(test_image_path)
import cloudinary
import cloudinary.uploader

# Configure Cloudinary
cloudinary.config(
    cloud_name="duljg3j2l",
    api_key="926499949357289",
    api_secret="2SNBQ5QhU8uywqzZgGHO6tTNCjg"
)

# Test image upload
try:
    response = cloudinary.uploader.upload("test_image.jpg")  # Replace with the path to a local image
    print("Upload successful!")
    print("Image URL:", response['secure_url'])  # Get the URL of the uploaded image
except Exception as e:
    print("Error uploading image:", e)