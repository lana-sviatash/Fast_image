import hashlib

import cloudinary
import cloudinary.uploader

from src.conf.config import settings
from src.conf import messages


class CloudImage:
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    @staticmethod
    def generate_name_image(email: str) -> str:
        name = hashlib.sha256(email.encode('utf-8')).hexdigest()[:12]
        return f"fast_image/{name}"

    @staticmethod
    def upload_image(file, public_id: str) -> dict:
        upload_file = cloudinary.uploader.upload(file, public_id=public_id)
        return upload_file

    @staticmethod
    def get_url_for_image(public_id, upload_file) -> str:
        src_url = cloudinary.CloudinaryImage(public_id) \
            .build_url(width=250, height=250, crop='fill', version=upload_file.get('version'))
        return src_url

    def delete_img(self, public_id: str):
        
        cloudinary.uploader.destroy(public_id, resource_type="image")
        return f'{public_id} deleted'

    
    async def change_size(self, public_id: str, width: int) -> str:
        try:
            img = cloudinary.CloudinaryImage(public_id).image(
                transformation=[{"width": width, "crop": "pad"}])
            url = img.split('"')
            upload_image = cloudinary.uploader.upload(url[1], folder="fast_image")
            return upload_image['url'], upload_image['public_id']
        except cloudinary.api.Error as e:
            print(messages.CLOUDINARY_API_ERROR, e.message)
            return None, None
        except cloudinary.exceptions.Error as e:
            print(messages.CLOUDINARY_ERROR, e)
            return None, None
        except Exception as e:
            print(messages.UNEXPECTED_ERROR, str(e))
            return None, None
        
    async def fade_edges_image(self, public_id: str, effect: str = "vignette") -> str:
        try:
            img = cloudinary.CloudinaryImage(public_id).image(effect=effect)
            url = img.split('"')
            upload_image = cloudinary.uploader.upload(url[1], folder="fast_image")
            return upload_image['url'], upload_image['public_id']
        except cloudinary.api.Error as e:
            print(messages.CLOUDINARY_API_ERROR, e.message)
            return None, None
        except cloudinary.exceptions.Error as e:
            print(messages.CLOUDINARY_ERROR, e)
            return None, None
        except Exception as e:
            print(messages.UNEXPECTED_ERROR, str(e))
            return None, None

    async def make_black_white_image(self, public_id: str, effect: str = "art:audrey") -> str:
        try:
            img = cloudinary.CloudinaryImage(public_id).image(effect=effect)
            url = img.split('"')
            upload_image = cloudinary.uploader.upload(url[1], folder="fast_image")
            return upload_image['url'], upload_image['public_id']
        except cloudinary.api.Error as e:
            print(messages.CLOUDINARY_API_ERROR, e.message)
            return None, None
        except cloudinary.exceptions.Error as e:
            print(messages.CLOUDINARY_ERROR, e)
            return None, None
        except Exception as e:
            print(messages.UNEXPECTED_ERROR, str(e))
            return None, None

image_cloudinary = CloudImage()