from enum import Enum

class Modality(str, Enum):
    """Standard AI model modalities."""
    TEXT = "Text"
    IMAGE = "Image"
    AUDIO = "Audio"
    VIDEO = "Video"
    THREE_D = "3D"
    CODE = "Code"
    METADATA = "Metadata"

class ModelBase:
    def __init__(self):
        pass

    def process_text_to_text(self):
        pass

    def imput_modalities(self):
        return []

    def output_modalities(self):
        return []

    def process_modalities(self):
        return