import pytest
from flask import json
from unittest.mock import patch

from api import app

MOCKED_CRAWLER_HTML = '<html>mocked html content</html>'
MOCKED_USECASE_EMBEDDINGS_RESULT = [{"brand_image": "mock_brand", "distance": 0.75, "file": "1.jpg"}]
MOCKED_USECASE_LLM_RESULT = 'mocked category'

API_EMBEDDINGS_RESULT_KEY = 'similarities'
API_LLM_CATEGORY_RESULT_KEY = 'category'


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def mock_common_dependencies(mock_crawler, mock_use_case_embedding, mock_use_case_llm=None):
    mock_crawler = mock_crawler.return_value
    mock_use_case_embedding = mock_use_case_embedding.return_value

    mock_crawler.run.return_value = MOCKED_CRAWLER_HTML
    mock_use_case_embedding.run_embedding.return_value.to_dict.return_value = MOCKED_USECASE_EMBEDDINGS_RESULT
    
    if mock_use_case_llm:
        mock_use_case_llm = mock_use_case_llm.return_value
        mock_use_case_llm.run.return_value = MOCKED_USECASE_LLM_RESULT

@patch('api.UseCaseLLM')
@patch('api.UseCaseEmbedding')
@patch('api.Crawler')
def test_full_process_request(mock_crawler, mock_use_case_embedding, mock_use_case_llm, client):
    mock_common_dependencies(mock_crawler, mock_use_case_embedding, mock_use_case_llm)
    
    payload = {"site": "site.com", "embedding_model_name": "model1", "llm_model_name": "model2"}
    response = client.post('/calculate_similarity', data=json.dumps(payload), content_type='application/json')
    response_data = response.json
    
    assert response.status_code == 200
    assert API_EMBEDDINGS_RESULT_KEY in response_data
    assert response_data[API_EMBEDDINGS_RESULT_KEY] == MOCKED_USECASE_EMBEDDINGS_RESULT
    assert API_LLM_CATEGORY_RESULT_KEY in response_data
    assert response_data[API_LLM_CATEGORY_RESULT_KEY] == MOCKED_USECASE_LLM_RESULT


@patch('api.Crawler')
@patch('api.UseCaseEmbedding')
def test_process_request_no_llm(mock_use_case_embedding, mock_crawler, client):
    mock_common_dependencies(mock_crawler, mock_use_case_embedding)
    
    payload = {"site": "example.com", "embedding_model_name": "model1"}
    response = client.post('/calculate_similarity', data=json.dumps(payload), content_type='application/json')
    response_data = response.json

    assert response.status_code == 200
    assert API_EMBEDDINGS_RESULT_KEY in response_data
    assert response_data[API_EMBEDDINGS_RESULT_KEY] == MOCKED_USECASE_EMBEDDINGS_RESULT
    assert API_LLM_CATEGORY_RESULT_KEY not in response_data


def test_process_request_invalid_json(client):
    payload = {"site": "example.com"}
    response = client.post('/calculate_similarity', data=json.dumps(payload), content_type='application/json')
    response_data = response.json

    assert response.status_code == 400
    assert 'error' in response_data
    assert 'JSON schema is invalid' in response_data['error']


@patch('api.Crawler')
def test_process_request_internal_error(mock_crawler, client):
    mock_crawler = mock_crawler.return_value
    mock_crawler.run.side_effect = Exception('Internal server error')

    payload = {"site": "example.com", "embedding_model_name": "model1"}
    response = client.post('/calculate_similarity', data=json.dumps(payload), content_type='application/json')
    response_data = response.json

    assert response.status_code == 500
    assert 'error' in response_data
    assert response_data['error'] == 'Internal server error'
