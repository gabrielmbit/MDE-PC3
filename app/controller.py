from uuid import uuid4

from . import repository
from .utils import (
	b64_to_bytes,
	ensure_images_dir,
	file_size_kb,
	file_to_b64,
	now_str,
	picture_path,
)


def hello() -> str:
	return "Hello, World!"


def post_image(body: dict) -> dict:
	if "data" not in body:
		raise ValueError("Missing 'data' field")

	picture_id = str(uuid4())
	img_b64 = body["data"]

	date = now_str()
	img_bytes = b64_to_bytes(img_b64)

	ensure_images_dir()
	path = picture_path(picture_id)
	with open(path, "wb") as f:
		f.write(img_bytes)

	repository.insert_picture(picture_id=picture_id, path=path, date=date)

	return {
		"id": picture_id,
		"size": file_size_kb(path),
		"date": date,
		"tags": [],
		"data": img_b64,
	}


def get_images(min_date: str | None, max_date: str | None) -> list[dict]:
	pictures = repository.get_pictures(min_date=min_date, max_date=max_date)
	out: list[dict] = []
	for p in pictures:
		out.append(
			{
				"id": p.id,
				"size": file_size_kb(p.path),
				"date": p.date,
				"tags": [],
			}
		)
	return out


def get_image(picture_id: str) -> dict:
	picture = repository.get_picture(picture_id)
	if picture is None:
		raise LookupError("Not found")

	return {
		"id": picture.id,
		"size": file_size_kb(picture.path),
		"date": picture.date,
		"tags": [],
		"data": file_to_b64(picture.path),
	}
