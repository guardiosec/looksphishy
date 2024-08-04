import logging

import conf
from src.models.logo_detection import get_logo_detection_model, LOGO_DETECTION_MODELS


logger = logging.getLogger(conf.LOGGER_NAME)


class UseCaseLogo(object):
    def __init__(self, logo_model_name: str):
        self.logo_model = get_logo_detection_model(logo_model_name)

    def run(self, image_path):
        """
        Return logo name
        """
        return self.logo_model.run(image_path)

    @staticmethod
    def get_all_logo_model_names():
        return list(LOGO_DETECTION_MODELS)
