import json
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "http://127.0.0.1:8000"


class ModelClientBase:
    """Base client for interacting with the AI Model Server API."""

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def _request(self, method, endpoint, data=None, timeout=600):
        """Helper method to perform HTTP requests and parse JSON response."""
        url = self.base_url + endpoint
        req = urllib.request.Request(url, method=method)
        if data:
            req.add_header('Content-Type', 'application/json')
            req.data = json.dumps(data).encode('utf-8')
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        except urllib.error.URLError as e:
            raise Exception(f"URL Error: {e.reason}")

    def cache_model(self, model_id: str):
        """Request the server to cache a specific model."""
        encoded_id = urllib.parse.quote(model_id, safe='')
        return self._request("POST", f"/models/{encoded_id}/cache")

    def uncache_model(self, model_id: str):
        """Request the server to uncache a specific model."""
        encoded_id = urllib.parse.quote(model_id, safe='')
        return self._request("POST", f"/models/{encoded_id}/uncache")

    def list_cached_models(self):
        """Request the server to list all cached models."""
        return self._request("GET", "/models/cached")

    def get_model_stats(self, model_id: str):
        """Get model statistics from server."""
        encoded_id = urllib.parse.quote(model_id, safe='')
        return self._request("GET", f"/models/{encoded_id}/stats")


class TextToTextClient(ModelClientBase):
    """Client specialized for text-to-text generation requests."""

    def generate(self, model_id: str, prompt: str, max_new_tokens: int = None, temperature: float = 0.7, model_limit_seconds: int = 60):
        """Send a text-to-text generation request to the server."""
        encoded_id = urllib.parse.quote(model_id, safe='')
        data = {
            "prompt": prompt,
            "temperature": temperature,
            "model_limit_seconds": model_limit_seconds
        }
        if max_new_tokens is not None:
            data["max_new_tokens"] = max_new_tokens

        return self._request("POST", f"/models/{encoded_id}/generate", data=data, timeout=model_limit_seconds + 60)