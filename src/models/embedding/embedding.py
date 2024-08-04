import os
import re
import base64
import logging
import json
import socket

import conf
from utils import timeit

logger = logging.getLogger(conf.LOGGER_NAME)


class Embedding(object):
    """
    A class to handle the processing of image embeddings from either file paths or base64 encoded strings.
    """

    def __init__(self, name, use_cache=False):
        """
        Initializes the Embedding object with default values.
        """
        self.path = None
        self.name = name
        self.use_cache = use_cache


    def is_image_path(self) -> bool:
        """
        Checks if the provided path is a valid image file path.

        Returns:
        bool: True if the path is a valid image file and exists, False otherwise.
        """
        if re.match(r'^.*\.(jpg|jpeg|png|gif|bmp)$', self.path, flags=re.IGNORECASE) and os.path.isfile(self.path):
            return True
        return False

    def is_base64(self) -> bool:
        """
        Checks if the provided path is a valid base64 encoded string.

        Returns:
        bool: True if the path is a valid base64 encoded string, False otherwise.
        """
        try:
            decoded = base64.b64decode(self.path)
            if base64.b64encode(decoded) == self.path.encode():
                return True
            else:
                return False
        except Exception as e:
            logger.error(e)
            return False

    @timeit
    def run(self):
        """
        Measures the time taken to run the get_embedding method and returns its result.

        Returns:
        Any: The result of the get_embedding method.
        """
        embedding = self.get_embedding()
        return embedding

    def get_embedding(self, *args, **kwargs):
        """
        Abstract method to be implemented in subclasses to generate embeddings from the image.

        Raises:
        NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @staticmethod
    def get_similarity(embedding_a, embedding_b):
        """
        Abstract method to be implemented in subclasses to compare the embeddings of two images.
        It should return the distance between two images
        """
        raise NotImplementedError

    @staticmethod
    def get_embedding_from_cache(embedding_path_cached):
        with open(embedding_path_cached, 'r') as f:
            embeddings = json.load(f)
            return embeddings

    def save_embedding_to_cache(self, embeddings):
        path_to_save = os.path.join(os.path.dirname(self.path), f'{self.name}.json')
        with open(path_to_save, 'w') as f:
            json.dump(embeddings, f)
        logger.info(f'Embedding saved to {path_to_save}')

    @staticmethod
    def is_internet_connected(host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False