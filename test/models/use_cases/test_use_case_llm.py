import pytest
from unittest.mock import patch, MagicMock
from src.use_cases.use_case_llm import UseCaseLLM

@patch('src.use_cases.use_case_llm.get_llm_model')
def test_use_case_llm_normal_flow(mock_get_llm_model):
    mock_category = 'mock_category'
    
    mock_llama3 = MagicMock()
    mock_llama3.run.return_value = mock_category
    mock_get_llm_model.return_value = mock_llama3

    use_case_llm = UseCaseLLM(llm_model_name='llama3')
    category = use_case_llm.run(html_content='<html><body>Mock HTML content</body></html>')

    assert category == 'mock_category'

def test_use_case_llm_non_registered_model_flow():
    expected_message_part = 'The model foo is not registered in the code'
    with pytest.raises(Exception, match=expected_message_part):
        UseCaseLLM(llm_model_name='foo')
