from pydantic import BaseModel
from typing import Optional


class ServerConfig(BaseModel):
    """Server configuration"""
    host: str = "0.0.0.0"
    port: int = 8000
    models_csv_path: str = "/mnt/d/AIs/Info/models_summary.csv"
    cache_folder_path: str = "/mnt/d/AIs/Cache"
    hf_token_path: str = "/mnt/d/AIs/token.txt"
    debug: bool = True