import json
import os
from typing import Optional

from imagekitio import ImageKit

_client: Optional[ImageKit] = None

def get_imagekit() -> ImageKit:
	global _client
	if _client is not None:
		return _client

	credentials_path = os.getenv("CREDENTIALS_PATH", "/opt/app/credentials.json")
	with open(credentials_path, "r", encoding="utf-8") as f:
		creds = json.load(f)

	ik = creds["imagekit"]
	try:
		url_endpoint = ik["endpoint"]
		public_key = ik["api_key"]
		private_key = ik["secret_key"]
	except KeyError as e:
		raise RuntimeError("credentials.json must contain: imagekit.endpoint, imagekit.api_key, imagekit.secret_key") from e

	_client = ImageKit(
		public_key=public_key,
		private_key=private_key,
		url_endpoint=url_endpoint,
	)
	return _client


