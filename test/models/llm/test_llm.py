import os
from unittest.mock import MagicMock, patch

import conf
from src.models.llm.llm import LLM
from src.models.llm.gemini_llm import GeminiLLM
from src.models.llm.lama3 import Llama3
from src.models.llm.chatgpt_llm import ChatGPTLLM

MOCK_TASK_PROPERTY = 'Mocked task'
MOCK_INPUT_DATA = 'Mocked input data'
MOCK_RESPONSE = 'Mocked response text'

def test_get_llm_input():
    llm_input_expected_keys = ['title', 'title_og', 'title_tw', 'description', 'description_og', 'description_tw']
    llm_input_missing_value = ''

    llm_instance = LLM()
    with open(os.path.join(conf.WORKING_DIR, 'test/brands', '1.txt'), 'r', encoding='utf-8') as f:
            html_content = f.read()
    
    llm_instance.get_input_data(html_content)
    llm_input = llm_instance.input_data
    
    assert all(key in llm_input for key in llm_input_expected_keys)
    assert all(value != llm_input_missing_value for value in llm_input.values())

@patch('src.models.llm.gemini_llm.vertexai')
@patch('src.models.llm.gemini_llm.GenerativeModel')
def test_gemini_llm_get_category(mock_generative_model, vertex_ai_init_mock):
    generative_model_mock_instance = MagicMock(name='generative_model_mock_instance')
    mock_generative_model.return_value = generative_model_mock_instance
    
    mock_response = MagicMock(name='mock_generative_model_response')
    mock_response.text = MOCK_RESPONSE
    generative_model_mock_instance.generate_content.return_value = mock_response

    gemini_llm_object = GeminiLLM()
    gemini_llm_object.task = MOCK_TASK_PROPERTY
    gemini_llm_object.input_data = MOCK_INPUT_DATA
    
    result = gemini_llm_object.get_category()
    assert result == MOCK_RESPONSE

@patch('src.models.llm.lama3.ollama')
@patch('src.models.llm.lama3.subprocess')
def test_llama3_llm(mock_subprocess, mock_ollama):
    mock_ollama_instance = MagicMock(name='mock_ollama_instance')
    mock_ollama.chat = mock_ollama_instance

    mock_response = {'message': {'content': MOCK_RESPONSE}}
    mock_ollama_instance.return_value = mock_response
    
    llama3_instance = Llama3()
    llama3_instance.task = MOCK_TASK_PROPERTY
    llama3_instance.input_data = MOCK_INPUT_DATA
    result = llama3_instance.get_category()
    
    assert result == MOCK_RESPONSE

@patch.dict(os.environ, {'OPENAI_API_KEY': 'mock_api_key'})
@patch('src.models.llm.chatgpt_llm.openai.chat.completions.create')
def test_chatgpt_llm(mock_openai_create):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = MOCK_RESPONSE
    mock_openai_create.return_value = mock_response
    
    chatgpt_llm_instance = ChatGPTLLM()
    chatgpt_llm_instance.task = MOCK_TASK_PROPERTY
    chatgpt_llm_instance.input_data = MOCK_INPUT_DATA
    result = chatgpt_llm_instance.get_category()

    assert result == MOCK_RESPONSE
