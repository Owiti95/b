import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Correctly named dictionary with dynamic environment variable substitution
Cloudinary_config = {
    "CLOUD_NAME": os.getenv("CLOUD_NAME"),
    "API_KEY": os.getenv("API_KEY"),
    "API_SECRET": os.getenv("API_SECRET"),
}












# import cloudinary
# import os

# Cloudinary_config = {
#     "cloud_name": os.getenv("CLOUDINARY_CLOUD_NAME", "your_cloud_name"),
#     "api_key": os.getenv("CLOUDINARY_API_KEY", "your_api_key"),
#     "api_secret": os.getenv("CLOUDINARY_API_SECRET", "your_api_secret"),
# }

# import cloudinary
# import os

# cloudinary.config(
#     cloud_name=os.getenv("CLOUD_NAME"),
#     api_key=os.getenv("API_KEY"),
#     api_secret=os.getenv("API_SECRET")
# )


# my_cloudinary_config.py

# cloudinary_config = {
#     "cloud_name": "CLOUD_NAME",
#     "api_key": "API_KEY",
#     "api_secret": "API_SECRET",
# }
# CLOUD_NAME=duljg3j2l
# API_KEY=926499949357289
# API_SECRET=2SNBQ5QhU8uywqzZgGHO6tTNCjg



