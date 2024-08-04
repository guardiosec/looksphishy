import os
import openai
import logging

from src.models.llm.llm import LLM
import conf

logger = logging.getLogger(conf.LOGGER_NAME)

class ChatGPTLLM(LLM):
    _initialized = False

    def __init__(self):
        super().__init__()
        self._init_model()

    @classmethod
    def _init_model(cls):
        if not cls._initialized:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
            cls._initialized = True
            logger.info('Model initialized!')
        else:
            logger.info('Model already initialized')

    def get_category(self):
        response = openai.chat.completions.create(
            model='gpt-4',
            messages=[{"role": "user", "content": f'{self.task}: {self.input_data}'}]
        )
        return response.choices[0].message.content
