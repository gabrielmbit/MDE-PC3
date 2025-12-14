import json
import os

import requests


def get_imagga_tags(image_url: str, min_confidence: float) -> list[dict]:
	credentials_path = os.getenv("CREDENTIALS_PATH", "/opt/app/credentials.json")
	with open(credentials_path, "r", encoding="utf-8") as f:
		creds = json.load(f)

	imagga = creds["imagga"]
	endpoint = imagga["endpoint"]
	api_key = imagga["api_key"]
	api_secret = imagga["api_secret"]

	resp = requests.get(
		f"{endpoint}/tags?image_url={image_url}",
		auth=(api_key, api_secret),
		timeout=30,
	)
	resp.raise_for_status()

	raw_tags = resp.json()["result"]["tags"]
	return [
		{"tag": t["tag"]["en"], "confidence": t["confidence"]}
		for t in raw_tags
		if t["confidence"] > min_confidence
	]


