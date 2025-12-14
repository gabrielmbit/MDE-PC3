from flask import Blueprint, request
from . import controller

bp = Blueprint("main", __name__, url_prefix="/")

@bp.get("/hello")
def hello_view():
	return controller.hello()


@bp.post("/image")
def post_image():
	if not request.is_json:
		return {"description": "Body must be a json"}, 400

	min_confidence = float(request.args.get("min_confidence", "80"))

	try:
		body = controller.post_image(request.json, min_confidence)
	except ValueError as e:
		return {"description": str(e)}, 400
	except RuntimeError as e:
		return {"description": str(e)}, 502

	return body


@bp.get("/images")
def get_images():
	min_date = request.args.get("min_date")
	max_date = request.args.get("max_date")
	tags_str = request.args.get("tags")
	tags = None
	if tags_str is not None:
		tags = [t.strip() for t in tags_str.split(",") if t.strip() != ""]

	body = controller.get_images(min_date=min_date, max_date=max_date, tags=tags)
	return body


@bp.get("/image/<picture_id>")
def get_image(picture_id: str):
	try:
		body = controller.get_image(picture_id)
	except LookupError:
		return {"description": "Not found"}, 404
	return body
