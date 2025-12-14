from flask import Blueprint
from . import controller

bp = Blueprint("main", __name__, url_prefix="/")

@bp.get("/hello")
def hello_view():
   return controller.hello()
