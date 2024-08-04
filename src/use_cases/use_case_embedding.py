import time
import os
import json
import pandas as pd
import logging


import conf
from src.models.embedding import get_embedding_model, EMBEDDING_MODELS


logger = logging.getLogger(conf.LOGGER_NAME)


class UseCaseEmbedding(object):
    """
    Triggers LooksPhishy analysis in a classic mode

    Methods
    -------
    run(image_path):
        Initiates the entire image comparison flow.
    is_embedding_model_valid():
        Checks if the embedding model is valid. If not, return False
    load_db(model_name):
        Loads the pre-saved embeddings of the brands DB
    get_similarity_resnet(embd1,embd2):
        Returns cosine similarity for Resnet embeddings
    get_similarity_vit(embd1,embd2):
        Returns cosine similarity for ViT embeddings
    check_image(embedding):
        Returns the distance with the given image and all the phishing images in the db
    """

    def __init__(self, embedding_model_name: str, use_cache: bool = False):
        self.use_cache = use_cache
        self.embedding_model = get_embedding_model(embedding_model_name, use_cache=use_cache)
        if not self.is_embedding_model_valid(embedding_model_name):
            raise Exception(f"Compute first the embedding of the brands for the model {embedding_model_name}")
        self.embedding_db = self.load_db(embedding_model_name)

    def run_embedding(self, image_path):
        """
        Initiates the entire image comparison flow.
        Parameters
        ----------
        image_path: str
            Path of the analyzed image

        Returns
        -------
        DataFrame
            The distances of brand images and the analyzed image which exceeded the similarity threshold of the selected model 
        """
        before = time.time()
        embedding_image = self.embedding_model.get_embedding(image_path)
        logger.info(f'Embedding of the image computed in {round(time.time() - before, 3)} s')
        df = self.check_image(embedding=embedding_image)
        logger.info('Image compared with all the DB !. The max similarity is : ' + str(df['distance'].max()))
        df = df[df['distance'] >= self.embedding_model.threshold]
        return df

    @staticmethod
    def is_embedding_model_valid(embedding_model_name):
        """
        Checks if the embedding model is valid. If not, returns False
        """
        status = False
        for brand in os.listdir(conf.BRAND_FOLDER):
            brand_path = os.path.join(conf.BRAND_FOLDER, brand)
            status_brand = False
            if os.path.isdir(brand_path):
                for image in os.listdir(brand_path):
                    if embedding_model_name in image:
                        status = True
                        status_brand = True
                if not status_brand:
                    print(f'WARNING - No embedding computed for {brand}')
        if not status:
            logger.error(
                f'No embedding computed for any brand. Run prepare_embedding.py to compute the embeddings first')
        return status

    @staticmethod
    def load_db(model_name):
        """
        Loads the pre-saved embeddings of the brands DB
        Parameters
        ----------
        model_name: str
            Name of the selected model name

        Returns
        -------
        dict
            Selected model embeddings of the brands DB
        """
        embeddings_dict = {}

        for brand in os.listdir(conf.BRAND_FOLDER):
            brand_path = os.path.join(conf.BRAND_FOLDER, brand)
            if os.path.isdir(brand_path):
                json_file = os.path.join(brand_path, f'{model_name}.json')
                if os.path.isfile(json_file):
                    with open(json_file, 'r') as f:
                        embeddings = json.load(f)
                    for i, key in enumerate(embeddings):
                        embeddings_dict[f"{brand}_{key}"] = embeddings[key]
        return embeddings_dict

    def check_image(self, embedding):
        """
        Returns the distance of the analyzed image and all the brand images in the db
        Parameters
        ----------
        embedding : embedding array of the analyzed image

        Returns
        -------
        DataFrame
            The distances of brand images and the analyzed image
        """
        result = []
        for brand_image in list(self.embedding_db):
            distance = self.embedding_model.get_similarity(self.embedding_db[brand_image], embedding)
            result.append(
                {"brand_image": brand_image.split('_')[0], "file": brand_image.split('_')[-1], "distance": distance})
        df = pd.DataFrame(result).sort_values('distance', ascending=False)
        return df

    @staticmethod
    def get_all_embedding_model_names():
        return list(EMBEDDING_MODELS)
