import cv2
import numpy as np
import base64
import logging
import torch
import torchvision.models as models
from torchvision import transforms
from io import BytesIO
from PIL import Image

import conf
from src.models.embedding.embedding import Embedding


logger = logging.getLogger(conf.LOGGER_NAME)

TENSOR_TRANSFORMER = None
RESNET101 = None
EMBEDDER = None


class ImageProcessor:
    @staticmethod
    def mask_white_pixels(image):
        image_rgb = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        _, white_mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        white_mask_inv = cv2.bitwise_not(white_mask)
        mean_color = cv2.mean(image_rgb, mask=white_mask_inv)[:3]
        result = np.where(white_mask[..., None], mean_color, image_rgb)
        return Image.fromarray(result.astype('uint8'), 'RGB')

    def process_image(self, image):
        image = self.mask_white_pixels(image)
        tensor = TENSOR_TRANSFORMER(image).unsqueeze(0)
        return tensor


class ResnetEmbedding(Embedding):
    threshold = 0.9

    def __init__(self, name, use_cache=False):
        super().__init__(name=name, use_cache=use_cache)
        self._init_model()
        self.image_processor = ImageProcessor()
        self.name = name

    @staticmethod
    def _init_model():
        global TENSOR_TRANSFORMER, RESNET101, EMBEDDER
        if TENSOR_TRANSFORMER is None or RESNET101 is None or EMBEDDER is None:
            TENSOR_TRANSFORMER = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
            RESNET101 = models.resnet101(weights='DEFAULT').eval()
            EMBEDDER = torch.nn.Sequential(*(list(RESNET101.children())[:-1]))
            logger.info("ResNet initialized!")
        else:
            logger.info('ResNet already initialized')

    def get_embedding(self, path):
        self.path = path
        try:
            if self.is_image_path():
                image = cv2.imread(path)
            elif self.is_base64():
                decoded_image = base64.b64decode(self.path)
                image = Image.open(BytesIO(decoded_image))
            else:
                logger.error(f'Invalid input: not an image file path or base64 string')
                return [None]

            tensor = self.image_processor.process_image(image)
            with torch.no_grad():
                embedding = EMBEDDER(tensor)
                return embedding.numpy().tolist()  # Convert to list for JSON serialization

        except Exception as e:
            logger.error(f'Failed extracting embedding for {self.path}. Error: {e}')
            return [None]

    @staticmethod
    def get_similarity(x, y):
        """
        Returns cosine similarity for Resnet embeddings
        Parameters
        ----------
        x: embedding array of a brand image
        y: embedding array of an analyzed image

        Returns
        -------
        Float
            The distances of brand images and the analyzed image
        """
        return torch.nn.functional.cosine_similarity(torch.tensor(x), torch.tensor(y)).item()
