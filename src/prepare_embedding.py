import os
import json
import conf
from src.models.embedding import get_embedding_model
import logging

logger = logging.getLogger(conf.LOGGER_NAME)

def run(embedding_name):
    my_model = get_embedding_model(embedding_name)

    for brand in os.listdir(conf.BRAND_FOLDER):
        brand_path = os.path.join(conf.BRAND_FOLDER, brand)
        logger.info('Processing', brand_path)
        if os.path.isdir(brand_path):
            embeddings = dict()
            for image in os.listdir(brand_path):
                image_path = os.path.join(brand_path, image)
                if os.path.isfile(image_path) and not image_path.endswith('.json'):
                    embedding = my_model.get_embedding(image_path)
                    embeddings[image] = embedding
            with open(os.path.join(brand_path, f'{embedding_name}.json'), 'w') as f:
                json.dump(embeddings, f)


if __name__ == "__main__":
    my_embedding_model = "multimodalembedding@001-Google"
    run(embedding_name=my_embedding_model)