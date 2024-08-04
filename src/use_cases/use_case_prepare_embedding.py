import os
import json
import logging

from src.models.embedding import get_embedding_model
import conf

logger = logging.getLogger(conf.LOGGER_NAME)


class UseCasePrepareEmbedding(object):

    def run(self, embedding_name, one_brand):
        my_model = get_embedding_model(embedding_name)
        if one_brand:
            logger.info('Preprocessing one brand only')
            self.scan_brand(one_brand, my_model, embedding_name)
        else:
            for brand in os.listdir(conf.BRAND_FOLDER):
                self.scan_brand(brand, embedding_name, embedding_name)

    @staticmethod
    def scan_brand(brand, embedding_model, embedding_name):
        brand_path = os.path.join(conf.BRAND_FOLDER, brand)
        print('Processing', brand_path)
        if os.path.isdir(brand_path):
            embeddings = dict()
            for image in os.listdir(brand_path):
                image_path = os.path.join(brand_path, image)
                if os.path.isfile(image_path) and not image_path.endswith('.json'):
                    embedding = embedding_model.get_embedding(image_path)
                    embeddings[image] = embedding
            with open(os.path.join(brand_path, f'{embedding_name}.json'), 'w') as f:
                json.dump(embeddings, f)
