from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class Tag:
	tag: str
	confidence: float

@dataclass
class Picture:
	id: str
	path: str
	date: str
	tags: List[Tag]
