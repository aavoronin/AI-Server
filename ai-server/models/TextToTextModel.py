from ModelBase import ModelBase, Modality


class TextToTextModel(ModelBase):
    pass

    def imput_modalities(self):
        return [Modality.TEXT]

    def output_modalities(self):
        return [Modality.TEXT]
