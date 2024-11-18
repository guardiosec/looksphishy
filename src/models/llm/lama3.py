import ollama
import logging
import requests
import time
from threading import Thread

import conf
from src.models.llm.llm import LLM

logger = logging.getLogger(conf.LOGGER_NAME)

class Llama3(LLM):
    _initialized = False
    MODEL_NAME = "llama3"

    def __init__(self):
        super().__init__()
        self._init_model()
        self.client = ollama.Client(host="http://ollama-app:11434/")  

    @classmethod
    def _init_model(cls):
        if not cls._initialized:
            # Wait for the server to be ready
            max_retries = 30
            retry_delay = 1
            for _ in range(max_retries):
                try:
                    # Try to connect to the ollama server
                    requests.get('http://ollama-app:11434/api/version')
                    break
                except requests.exceptions.ConnectionError:
                    time.sleep(retry_delay)
            else:
                raise RuntimeError("Failed to initialize ollama server after multiple retries")

            # Pull the model
            logger.info(f'Pulling model {cls.MODEL_NAME}...')
            try:
                requests.post('http://ollama-app:11434/api/pull', json={'name': cls.MODEL_NAME})
                cls._initialized = True
                logger.info('Model initialized!')
            except Exception as e:
                logger.error(f'Failed to pull model: {str(e)}')
                raise
        else:
            logger.info('Model already initialized')
            

    def get_category(self):
        response = self.client.chat(
            model=self.MODEL_NAME,
            messages=[{'role': 'user', 'content': f'{self.task}: {self.input_data}'}],
            stream=False
        )
        return response['message']['content']