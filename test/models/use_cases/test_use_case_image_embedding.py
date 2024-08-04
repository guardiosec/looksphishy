import os
import pytest
from pandas import DataFrame

import conf
from src.use_cases.use_case_embedding import UseCaseEmbedding

def test_use_case_embedding_normal_flow():
    image_path = os.path.join(conf.WORKING_DIR, 'test/brands', '1.jpg')
    use_case = UseCaseEmbedding(embedding_model_name='CLIP')
    
    result = use_case.run_embedding(image_path)
    assert isinstance(result, DataFrame)
    
    min_distance = result['distance'].min()
    assert min_distance >= use_case.embedding_model.threshold


def test_use_case_embedding_non_registered_model_flow():
    expected_message_part = 'The model foo is not registered in the code.'
    with pytest.raises(Exception, match=expected_message_part):
        UseCaseEmbedding(embedding_model_name='foo')
