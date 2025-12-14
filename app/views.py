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

	try:
		body = controller.post_image(request.json)
	except ValueError as e:
		return {"description": str(e)}, 400

	return body


@bp.get("/images")
def get_images():
	min_date = request.args.get("min_date")
	max_date = request.args.get("max_date")

	body = controller.get_images(min_date=min_date, max_date=max_date)
	return body


@bp.get("/image/<picture_id>")
def get_image(picture_id: str):
	try:
		body = controller.get_image(picture_id)
	except LookupError:
		return {"description": "Not found"}, 404
	return body
