import logging
import base64
import clip
import torch
import numpy as np
from io import BytesIO
from PIL import Image
from scipy.spatial.distance import cosine

import conf
from src.models.embedding.embedding import Embedding

logger = logging.getLogger(conf.LOGGER_NAME)
PREPROCESS = None
MODEL = None
DEVICE = None

class ClipEmbedding(Embedding):
    threshold = 0.85

    def __init__(self, name, use_cache=False):
        super().__init__(name=name, use_cache=use_cache)
        self._init_model()
        self.name = name

    @staticmethod
    def _init_model():
        global PREPROCESS, MODEL, DEVICE
        if MODEL is None or PREPROCESS is None or DEVICE is None:
            DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            MODEL, PREPROCESS = clip.load("ViT-B/32", device=DEVICE)
            logger.info("Model loaded !")
        else:
            logger.info('Model already loaded')

    def get_embedding(self, path):
        self.path = path
        try:
            if self.is_image_path():
                image = Image.open(self.path).convert('RGB')
            elif self.is_base64():
                decoded_image = base64.b64decode(self.path)
                image = Image.open(BytesIO(decoded_image)).convert('RGB')
            else:
                logger.error(f'Invalid input: not an image file path or base64 string.')
                return [None]

            image = PREPROCESS(image).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                image_features = MODEL.encode_image(image)

            # Normalize embeddings
            embeddings = image_features / image_features.norm(dim=-1, keepdim=True)
            embeddings = embeddings.cpu().numpy().tolist()[0]
            return embeddings

        except Exception as e:
            logger.error(f'Failed extracting embedding for {self.path}. Error: {e}')
            return [None]
        
    @staticmethod
    def get_similarity(x, y):
        return 1 - cosine(
            np.array(x).reshape(1, -1).flatten(),
            np.array(y).reshape(1, -1).flatten()
        )
