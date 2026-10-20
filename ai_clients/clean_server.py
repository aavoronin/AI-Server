from ai_clients.model_client_base import ModelClientBase


class CleanServerClient(ModelClientBase):
    """Client for triggering server-side cache analysis and cleaning."""

    def clean_server(self):
        """Call the server endpoint to analyze and print cache status."""
        return self._request("GET", "/clean_server")