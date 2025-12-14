from __future__ import annotations
from typing import Dict, Optional
from sqlalchemy import text
from .db import get_engine
from .models import Picture, Tag

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


def insert_tags(picture_id: str, date: str, tags: list[dict]) -> None:
	if not tags:
		return

	engine = get_engine()
	stmt = text(
		"""
		INSERT INTO tags (tag, picture_id, confidence, date)
		VALUES (:tag, :picture_id, :confidence, :date)
		"""
	)
	rows = [
		{
			"tag": t["tag"],
			"picture_id": picture_id,
			"confidence": float(t["confidence"]),
			"date": date,
		}
		for t in tags
	]
	with engine.begin() as conn:
		conn.execute(stmt, rows)


def get_tags(picture_id: str) -> list[Tag]:
	engine = get_engine()
	stmt = text(
		"""
		SELECT tag, confidence
		FROM tags
		WHERE picture_id = :picture_id
		ORDER BY confidence DESC
		"""
	)
	with engine.connect() as conn:
		rows = conn.execute(stmt, {"picture_id": picture_id}).mappings().all()
		return [Tag(tag=r["tag"], confidence=float(r["confidence"])) for r in rows]


def get_picture(picture_id: str) -> Optional[Picture]:
	engine = get_engine()
	stmt = text("SELECT id, path, date FROM pictures WHERE id = :id")
	with engine.connect() as conn:
		row = conn.execute(stmt, {"id": picture_id}).mappings().first()
		if not row:
			return None
		tags = get_tags(row["id"])
		return Picture(id=row["id"], path=row["path"], date=row["date"], tags=tags)


def get_pictures(
	min_date: Optional[str] = None,
	max_date: Optional[str] = None,
	tags: Optional[list[str]] = None,
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

	if tags:
		placeholders = []
		for i, t in enumerate(tags):
			k = f"tag_{i}"
			params[k] = t
			placeholders.append(f":{k}")

		stmt = text(
			f"""
			SELECT p.id, p.path, p.date
			FROM pictures p
			JOIN tags tg ON tg.picture_id = p.id
			WHERE {" AND ".join(base_where)} AND tg.tag IN ({", ".join(placeholders)})
			GROUP BY p.id, p.path, p.date
			HAVING COUNT(DISTINCT tg.tag) = {len(tags)}
			ORDER BY p.date DESC
			"""
		)
	else:
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
		out: list[Picture] = []
		for r in rows:
			pid = r["id"]
			out.append(Picture(id=pid, path=r["path"], date=r["date"], tags=get_tags(pid)))
		return out
