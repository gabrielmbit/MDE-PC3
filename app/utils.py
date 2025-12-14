import base64
import os
from datetime import datetime

BASE64_REGEX = re.compile(r'^data:image\/[a-zA-Z]+;base64,')

def now_str() -> str:
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def images_dir() -> str:
	return os.getenv("IMAGES_DIR", "/opt/app/images")


def picture_path(picture_id: str) -> str:
	return os.path.join(images_dir(), f"{picture_id}.jpg")


def ensure_images_dir() -> None:
	os.makedirs(images_dir(), exist_ok=True)


def file_size_kb(path: str) -> int:
	return int(os.path.getsize(path) / 1024)


def b64encode(b64_str: str) -> bytes:
	try:
		return base64.b64encode(b64_str)
	except Exception as e:
		raise ValueError("Invalid base64 in 'data'") from e


def file_to_b64(path: str) -> str:
	with open(path, "rb") as f:
		return base64.b64encode(f.read()).decode("utf-8")


