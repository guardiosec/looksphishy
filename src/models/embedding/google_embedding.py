import logging
import os.path
import numpy as np
import base64
from src.models.embedding.embedding import Embedding
from vertexai.preview.vision_models import MultiModalEmbeddingModel
from vertexai.preview.vision_models import Image

import conf


logger = logging.getLogger(conf.LOGGER_NAME)
MODEL = None


class GoogleEmbedding(Embedding):
    threshold = 0.7

    def __init__(self, name, use_cache=False):
        super().__init__(name=name, use_cache=use_cache)
        self._init_model()

    def _init_model(self):
        global MODEL
        if MODEL is not None:
            logger.info('Model already loaded')
        else:
            if not self.is_internet_connected():
                logger.error("Internet not connected. If you don't use cache results, the model will not work")
            else:
                MODEL = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")
                logger.info("Model loaded !")

    def get_embedding(self, path):
        self.path = path
        if self.use_cache:
            embedding_path_cached = os.path.join(os.path.dirname(path), f'{self.name}.json')
            if os.path.exists(embedding_path_cached):
                return self.get_embedding_from_cache(embedding_path_cached)
        try:
            embeddings = None
            if self.is_image_path():
                embeddings = MODEL.get_embeddings(image=Image.load_from_file(self.path))
            elif self.is_base64():
                embeddings = MODEL.get_embeddings(image=Image(base64.b64decode(self.path)))
            if self.use_cache and embeddings is not None:
                self.save_embedding_to_cache(embeddings.image_embedding)
            return embeddings.image_embedding
        except Exception as e:
            logger.error(f'Failed extracting embedding for {self.path}. Error {e}')
            return [None]

    @staticmethod
    def get_similarity(embedding_a, embedding_b):
        sample_magnitude = np.linalg.norm(embedding_a)
        magnitude = np.linalg.norm(embedding_b) * sample_magnitude
        distance = np.dot(embedding_a, embedding_b) / magnitude
        return distance
