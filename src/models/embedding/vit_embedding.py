import logging
import base64
import numpy as np
import torch

from io import BytesIO
from scipy.spatial.distance import cosine
from transformers import logging as transformers_logging
from PIL import Image
from transformers import ViTImageProcessor, ViTModel

import conf
from src.models.embedding.embedding import Embedding

transformers_logging.set_verbosity_error()

logger = logging.getLogger(conf.LOGGER_NAME)

FEATURE_EXTRACTOR = None
MODEL = None
DEVICE = None

class VitEmbedding(Embedding):
    threshold = 0.9

    def __init__(self, name, use_cache=False):
        super().__init__(name=name, use_cache=use_cache)
        self._init_model()
        self.name = name

    @staticmethod
    def _init_model():
        global FEATURE_EXTRACTOR, MODEL, DEVICE
        if MODEL is None or FEATURE_EXTRACTOR is None or DEVICE is None:
            model_name = 'google/vit-large-patch32-384'
            FEATURE_EXTRACTOR = ViTImageProcessor.from_pretrained(
                model_name,
                do_resize=True,
                size=384,
                do_center_crop=True,
                crop_size=384,
            )
            MODEL = ViTModel.from_pretrained(model_name)
            DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            MODEL.to(DEVICE)
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

            inputs = FEATURE_EXTRACTOR(images=image, return_tensors='pt')
            with torch.no_grad():
                outputs = MODEL(**inputs)

            embeddings = outputs.last_hidden_state[:, 0, :].squeeze()  # Taking [CLS]
            embeddings = embeddings / embeddings.norm(p=2, dim=-1, keepdim=True)  # Normalize embeddings
            embeddings = embeddings.cpu().numpy().tolist()
            return embeddings

        except Exception as e:
            logger.error(f'Failed extracting embedding for {self.path}. Error: {e}')
            return [None]

    @staticmethod
    def get_similarity(x, y):
        """
        Returns cosine similarity for ViT embeddings
        Parameters
        ----------
        x: embedding array of a brand image
        y: embedding array of an analyzed image

        Returns
        -------
        Float
            The distances of brand images and the analyzed image
        """
        return 1 - cosine(
            np.array(x).reshape(1, -1).flatten(),
            np.array(y).reshape(1, -1).flatten()
        )
