from __future__ import annotations
from typing import Dict, Optional
from sqlalchemy import text
from .db import get_engine
from .models import Picture

def insert_picture(picture_id: str, path: str, date: str) -> None:
	engine = get_engine()
	stmt = text(
		"""
		INSERT INTO pictures (id, path, date)
		VALUES (:id, :path, :date)
		"""
	)
	with engine.begin() as conn:
		conn.execute(stmt, {"id": picture_id, "path": path, "date": date})


def get_picture(picture_id: str) -> Optional[Picture]:
	engine = get_engine()
	stmt = text("SELECT id, path, date FROM pictures WHERE id = :id")
	with engine.connect() as conn:
		row = conn.execute(stmt, {"id": picture_id}).mappings().first()
		if not row:
			return None
		return Picture(id=row["id"], path=row["path"], date=row["date"])


def get_pictures(
	min_date: Optional[str] = None,
	max_date: Optional[str] = None,
) -> list[Picture]:
	engine = get_engine()

	base_where = ["1=1"]
	params: Dict = {}

	if min_date:
		base_where.append("p.date >= :min_date")
		params["min_date"] = min_date
	if max_date:
		base_where.append("p.date <= :max_date")
		params["max_date"] = max_date

	stmt = text(
		f"""
		SELECT p.id, p.path, p.date
		FROM pictures p
		WHERE {" AND ".join(base_where)}
		ORDER BY p.date DESC
		"""
	)

	with engine.connect() as conn:
		rows = conn.execute(stmt, params).mappings().all()
		return [Picture(id=r["id"], path=r["path"], date=r["date"]) for r in rows]
