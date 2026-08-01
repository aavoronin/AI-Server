from pydantic import BaseModel
from typing import Optional


class ModelFilter(BaseModel):
    """Filter parameters for model search"""
    # Modality filters
    input_modalities: Optional[str] = None
    output_modalities: Optional[str] = None

    # Numeric range filters
    model_size_from: Optional[int] = None
    model_size_to: Optional[int] = None

    input_tokens_from: Optional[int] = None
    input_tokens_to: Optional[int] = None

    output_tokens_from: Optional[int] = None
    output_tokens_to: Optional[int] = None

    downloads_from: Optional[int] = None
    downloads_to: Optional[int] = None

    likes_from: Optional[int] = None
    likes_to: Optional[int] = None

    size_b_from: Optional[int] = None
    size_b_to: Optional[int] = None