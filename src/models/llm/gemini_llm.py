import logging
import vertexai
from vertexai.generative_models import GenerativeModel

import conf
from src.models.llm.llm import LLM

logger = logging.getLogger(conf.LOGGER_NAME)

MODEL = None

class GeminiLLM(LLM):

    def __init__(self):
        super().__init__()
        self._init_model()

    @staticmethod
    def _init_model():
        global MODEL
        if MODEL is None:
            vertexai.init()
            MODEL = GenerativeModel('gemini-1.5-flash-001')
            logger.info("Model loaded!")
        else:
            logger.info("Model already loaded")

    def get_category(self):
        response = MODEL.generate_content(f'{self.task}: {self.input_data}')
        return response.text
