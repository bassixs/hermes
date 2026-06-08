from __future__ import annotations

import os
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from common import require


DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]


def drive_service():
    credentials_path = require(os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""), "GOOGLE_APPLICATION_CREDENTIALS")
    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=DRIVE_SCOPES)
    return build("drive", "v3", credentials=credentials)


def upload_public_image(path: str) -> str:
    folder_id = require(os.getenv("GOOGLE_DRIVE_SCREENSHOT_FOLDER_ID", ""), "GOOGLE_DRIVE_SCREENSHOT_FOLDER_ID")
    file_path = Path(path)
    service = drive_service()

    metadata = {
        "name": file_path.name,
        "parents": [folder_id],
    }
    media = MediaFileUpload(str(file_path), mimetype="image/png", resumable=False)
    created = (
        service.files()
        .create(body=metadata, media_body=media, fields="id", supportsAllDrives=True)
        .execute()
    )
    file_id = created["id"]

    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
        fields="id",
        supportsAllDrives=True,
    ).execute()

    return f"https://drive.google.com/uc?export=view&id={file_id}"
