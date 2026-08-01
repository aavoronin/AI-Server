import json
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "http://127.0.0.1:8000"


class ServerTester:
    """Test suite for the AI Model Server API."""

    def __init__(self):
        self.base_url = BASE_URL
        self.passed = 0
        self.failed = 0

    def _get(self, endpoint, params=None):
        """Helper method to perform GET requests and parse JSON response."""
        url = self.base_url + endpoint
        if params:
            query_string = urllib.parse.urlencode(params)
            url += f"?{query_string}"

        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        except urllib.error.URLError as e:
            raise Exception(f"URL Error: {e.reason}")

    def _assert(self, condition, message):
        if condition:
            print(f"  [PASS] {message}")
            self.passed += 1
        else:
            print(f"  [FAIL] {message}")
            self.failed += 1

    def wait_for_server(self, retries=15, delay=2):
        """Wait for the server to be online."""
        print("Waiting for server to start...")
        for i in range(retries):
            try:
                data = self._get("/")
                if data.get("status") == "online":
                    print("Server is online and ready.")
                    return True
            except Exception:
                pass
            time.sleep(delay)
        print("Server failed to start within the expected time.")
        return False

    def test_server_online(self):
        print("Testing: Server online")
        try:
            data = self._get("/")
            self._assert(data.get("status") == "online", "Status is online")
            self._assert("message" in data, "Message is present")
        except Exception as e:
            self._assert(False, str(e))

    def test_health_check(self):
        print("Testing: Health check")
        try:
            data = self._get("/health")
            self._assert(data.get("status") == "healthy", "Status is healthy")
            self._assert(data.get("models_loaded") is True, "Models are loaded")
            self._assert(data.get("total_models", 0) > 0, "Total models > 0")
        except Exception as e:
            self._assert(False, str(e))

    def test_text_to_text_1_to_5_gb(self):
        print("Testing: Text-to-text models (1-5 GB)")
        try:
            params = {"input_modalities": "Text", "output_modalities": "Text", "size_b_from": 1, "size_b_to": 5}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
            valid_sizes = all(1 <= m.get("SizeB", 1) <= 5 for m in data["models"] if m.get("SizeB") is not None)
            self._assert(valid_sizes, "All returned models are within 1-5 GB")
        except Exception as e:
            self._assert(False, str(e))

    def test_text_to_text_5_to_20_gb(self):
        print("Testing: Text-to-text models (5-20 GB)")
        try:
            params = {"input_modalities": "Text", "output_modalities": "Text", "size_b_from": 5, "size_b_to": 20}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
            valid_sizes = all(5 <= m.get("SizeB", 5) <= 20 for m in data["models"] if m.get("SizeB") is not None)
            self._assert(valid_sizes, "All returned models are within 5-20 GB")
        except Exception as e:
            self._assert(False, str(e))

    def test_text_to_image(self):
        print("Testing: Text-to-image models")
        try:
            params = {"input_modalities": "Text", "output_modalities": "Image"}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
        except Exception as e:
            self._assert(False, str(e))

    def test_image_to_text(self):
        print("Testing: Image-to-text models")
        try:
            params = {"input_modalities": "Image", "output_modalities": "Text"}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
        except Exception as e:
            self._assert(False, str(e))

    def test_image_text_to_text(self):
        print("Testing: Image-text-to-text models")
        try:
            params = {"input_modalities": "Image,Text", "output_modalities": "Text"}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
        except Exception as e:
            self._assert(False, str(e))

    def test_text_to_audio(self):
        print("Testing: Text-to-audio models")
        try:
            params = {"input_modalities": "Text", "output_modalities": "Audio"}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
        except Exception as e:
            self._assert(False, str(e))

    def test_audio_to_text(self):
        print("Testing: Audio-to-text models")
        try:
            params = {"input_modalities": "Audio", "output_modalities": "Text"}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
        except Exception as e:
            self._assert(False, str(e))

    def test_text_to_video(self):
        print("Testing: Text-to-video models")
        try:
            params = {"input_modalities": "Text", "output_modalities": "Video"}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
        except Exception as e:
            self._assert(False, str(e))

    def test_filter_by_likes(self):
        print("Testing: Filter by likes")
        try:
            params = {"likes_from": 100}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
            valid_likes = all(m.get("likes", 100) >= 100 for m in data["models"] if m.get("likes") is not None)
            self._assert(valid_likes, "All returned models have >= 100 likes")
        except Exception as e:
            self._assert(False, str(e))

    def test_filter_by_downloads(self):
        print("Testing: Filter by downloads")
        try:
            params = {"downloads_from": 1000}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
            valid_downloads = all(
                m.get("downloads", 1000) >= 1000 for m in data["models"] if m.get("downloads") is not None)
            self._assert(valid_downloads, "All returned models have >= 1000 downloads")
        except Exception as e:
            self._assert(False, str(e))

    def test_filter_by_model_size(self):
        print("Testing: Filter by model size")
        try:
            params = {"model_size_from": 100000, "model_size_to": 10000000}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
        except Exception as e:
            self._assert(False, str(e))

    def test_filter_by_input_tokens(self):
        print("Testing: Filter by input tokens")
        try:
            params = {"input_tokens_from": 1000, "input_tokens_to": 8000}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
        except Exception as e:
            self._assert(False, str(e))

    def test_filter_by_output_tokens(self):
        print("Testing: Filter by output tokens")
        try:
            params = {"output_tokens_from": 100, "output_tokens_to": 2000}
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
        except Exception as e:
            self._assert(False, str(e))

    def test_combined_filters(self):
        print("Testing: Combined filters")
        try:
            params = {
                "input_modalities": "Text",
                "output_modalities": "Text",
                "size_b_from": 1,
                "size_b_to": 10,
                "likes_from": 50,
                "downloads_from": 500
            }
            data = self._get("/models/filter", params)
            self._assert(data["count"] >= 0, "Count is valid")
        except Exception as e:
            self._assert(False, str(e))

    def test_get_all_models(self):
        print("Testing: Get all models")
        try:
            data = self._get("/models")
            self._assert(data["count"] > 0, "Count is greater than 0")
            self._assert(isinstance(data["models"], list), "Models is a list")
        except Exception as e:
            self._assert(False, str(e))

    def test_get_model_by_id(self):
        print("Testing: Get model by ID")
        try:
            all_models = self._get("/models")
            if all_models["count"] > 0:
                model_id = all_models["models"][0]["model_id"]
                encoded_id = urllib.parse.quote(model_id, safe='')
                data = self._get(f"/models/{encoded_id}")
                self._assert(data["model_id"] == model_id, "Returned model ID matches")
            else:
                self._assert(False, "No models available to test")
        except Exception as e:
            self._assert(False, str(e))

    def test_get_model_not_found(self):
        print("Testing: Get model not found (404)")
        try:
            url = f"{self.base_url}/models/non_existent_model_id_12345"
            req = urllib.request.Request(url)
            try:
                urllib.request.urlopen(req, timeout=5)
                self._assert(False, "Expected HTTPError 404")
            except urllib.error.HTTPError as e:
                self._assert(e.code == 404, f"Received 404, got {e.code}")
        except Exception as e:
            self._assert(False, str(e))

    def run_all(self):
        print("\n" + "=" * 50)
        print("Starting AI Server Tests")
        print("=" * 50 + "\n")

        if not self.wait_for_server():
            print("Aborting tests because server is not reachable.")
            return

        self.test_server_online()
        self.test_health_check()
        self.test_text_to_text_1_to_5_gb()
        self.test_text_to_text_5_to_20_gb()
        self.test_text_to_image()
        self.test_image_to_text()
        self.test_image_text_to_text()
        self.test_text_to_audio()
        self.test_audio_to_text()
        self.test_text_to_video()
        self.test_filter_by_likes()
        self.test_filter_by_downloads()
        self.test_filter_by_model_size()
        self.test_filter_by_input_tokens()
        self.test_filter_by_output_tokens()
        self.test_combined_filters()
        self.test_get_all_models()
        self.test_get_model_by_id()
        self.test_get_model_not_found()

        print("\n" + "=" * 50)
        print(f"Tests finished: {self.passed} passed, {self.failed} failed")
        print("=" * 50 + "\n")


#if __name__ == "__main__":
#    tester = ServerTester()
#    tester.run_all()