import os
from typing import Optional

from sqlalchemy import Engine, create_engine

_engine: Optional[Engine] = None


def get_engine() -> Engine:
	global _engine
	if _engine is not None:
		return _engine

	host = os.getenv("MYSQL_HOST")
	port = int(os.getenv("MYSQL_PORT"))
	db = os.getenv("MYSQL_DATABASE")
	user = os.getenv("MYSQL_USER")
	password = os.getenv("MYSQL_PASSWORD")

	_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
	return _engine


