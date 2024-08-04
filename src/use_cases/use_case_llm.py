import logging
import time

import conf
from src.models.llm import get_llm_model, LLM_MODELS

logger = logging.getLogger(conf.LOGGER_NAME)


class UseCaseLLM(object):
    """
    Triggers LooksPhishy analysis in a classic mode with category from LLM

    """

    def __init__(self, llm_model_name: str):
        self.llm_model = get_llm_model(llm_model_name)

    def run(self, html_content):
        before = time.time()
        category = self.llm_model.run(html_content)
        logger.info(f'LLM category generation time: {round(time.time() - before, 3)} s')
        return category

    @staticmethod
    def get_all_llm_model_names():
        return list(LLM_MODELS)
