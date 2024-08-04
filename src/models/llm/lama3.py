import ollama
import subprocess
import logging

import conf
from src.models.llm.llm import LLM

logger = logging.getLogger(conf.LOGGER_NAME)

class Llama3(LLM):
    _initialized = False

    def __init__(self):
        super().__init__()
        self._init_model()

    @classmethod
    def _init_model(cls):
        if not cls._initialized:
            subprocess.run(['ollama', 'serve'])
            cls._initialized = True
            logger.info('Model initialized!')
        else:
            logger.info('Model already initialized')

    def get_category(self):
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': f'{self.task}: {self.input_data}'}]
        )
        return response['message']['content']
