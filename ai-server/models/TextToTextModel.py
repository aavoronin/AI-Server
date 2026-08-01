from .ModelBase import ModelBase


class TextToTextModel(ModelBase):
    """Base class for Text-to-Text models."""

    def get_modality(self):
        return "Text", "Text"