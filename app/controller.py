import base64
from uuid import uuid4
from .db import repository
from .services.imagekit import get_imagekit
from .services.imagga import get_imagga_tags
from .utils import (
	ensure_images_dir,
	file_size_kb,
	file_to_b64,
	now_str,
	picture_path,
)


def hello() -> str:
	return "Hello, World!"


def post_image(body: dict, min_confidence: float = 80) -> dict:
	if "data" not in body:
		raise ValueError("Missing 'data' field")

	img_b64 = body["data"]

	date = now_str()
	picture_id = str(uuid4())

	ik = get_imagekit()
	upload_info = None
	tags: list[dict] = []
	try:
		base64.b64decode(img_b64, validate=True)
		upload_info = ik.upload(file=img_b64, file_name=f"{picture_id}.jpeg")
		tags = get_imagga_tags(upload_info.url, min_confidence=min_confidence)
	finally:
		if upload_info is not None:
			try:
				ik.delete_file(file_id=upload_info.file_id)
			except Exception:
				pass

	ensure_images_dir()
	path = picture_path(picture_id)
	with open(path, "wb") as f:
		f.write(img_b64)

	repository.insert_picture(picture_id=picture_id, path=path, date=date)
	repository.insert_tags(picture_id=picture_id, date=date, tags=tags)

	return {
		"id": picture_id,
		"size": file_size_kb(path),
		"date": date,
		"tags": tags,
		"data": img_b64,
	}


def get_images(min_date: str | None, max_date: str | None, tags: list[str] | None) -> list[dict]:
	if tags is None:
		return []

	pictures = repository.get_pictures(min_date=min_date, max_date=max_date, tags=tags)
	out: list[dict] = []
	for p in pictures:
		out.append(
			{
				"id": p.id,
				"size": file_size_kb(p.path),
				"date": p.date,
				"tags": [{"tag": t.tag, "confidence": t.confidence} for t in p.tags],
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
		"tags": [{"tag": t.tag, "confidence": t.confidence} for t in picture.tags],
		"data": file_to_b64(picture.path),
	}
