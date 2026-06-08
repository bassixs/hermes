from __future__ import annotations

import os
from pathlib import Path

import cloudinary
import cloudinary.uploader

from common import require


def configure() -> None:
    cloudinary.config(
        cloud_name=require(os.getenv("CLOUDINARY_CLOUD_NAME", ""), "CLOUDINARY_CLOUD_NAME"),
        api_key=require(os.getenv("CLOUDINARY_API_KEY", ""), "CLOUDINARY_API_KEY"),
        api_secret=require(os.getenv("CLOUDINARY_API_SECRET", ""), "CLOUDINARY_API_SECRET"),
        secure=True,
    )


def upload_image(path: str) -> str:
    configure()
    file_path = Path(path)
    folder = os.getenv("CLOUDINARY_FOLDER", "hermes-screenshots")
    result = cloudinary.uploader.upload(
        str(file_path),
        folder=folder,
        resource_type="image",
        public_id=file_path.stem,
        overwrite=True,
    )
    return result["secure_url"]

