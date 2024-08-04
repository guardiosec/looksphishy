import os
import json
import base64
from unittest.mock import patch, MagicMock

import conf
from src.models.embedding.embedding import Embedding
from src.models.embedding.google_embedding import GoogleEmbedding
from src.models.embedding.clip_embedding import ClipEmbedding
from src.models.embedding.vit_embedding import VitEmbedding
from src.models.embedding.resnet_embedding import ResnetEmbedding

TEST_OBJ_PATH = os.path.join(conf.WORKING_DIR, 'test/brands')
IMAGE_FILE_PATH = os.path.join(TEST_OBJ_PATH, '1.jpg')

class SampleGoogleEmbedding(object):
    def __init__(self):
        with open(os.path.join(TEST_OBJ_PATH, 'multimodalembedding@001-Google.json'), 'r') as file:
            self.image_embedding =  json.load(file)

def test_embedding_image_path_case():
    embedding_instance = Embedding(name='test')
    embedding_instance.path = IMAGE_FILE_PATH
    assert embedding_instance.is_image_path()

def test_embedding_base64_case():
    embedding_instance = Embedding(name='test')
    with open(IMAGE_FILE_PATH, 'rb') as image_file:
        base64_encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        embedding_instance.path = base64_encoded_image
    assert embedding_instance.is_base64()
    
@patch('src.models.embedding.google_embedding.MultiModalEmbeddingModel')
def test_get_google_embedding_model(mock_multi_model_embedding):
    mock_mm_model_instance = MagicMock()
    mock_multi_model_embedding.from_pretrained.return_value = mock_mm_model_instance
    mock_mm_model_instance.get_embeddings.return_value = SampleGoogleEmbedding()
    output = GoogleEmbedding(name='multimodalembedding@001-Google').get_embedding(IMAGE_FILE_PATH)
    assert len(output) == len(SampleGoogleEmbedding().image_embedding)

def test_get_clip_embedding():
    expected_embeddings_size = 512
    embeddings = ClipEmbedding(name='CLIP').get_embedding(IMAGE_FILE_PATH)
    assert len(embeddings) == expected_embeddings_size

def test_get_vit_embedding():
    expected_embeddings_size = 1024
    embeddings = VitEmbedding(name='ViT').get_embedding(IMAGE_FILE_PATH)
    assert len(embeddings) == expected_embeddings_size

def test_get_resnet_embedding():
    import torch
    expected_embeddings_size = torch.Size([1, 2048, 1, 1])
    embeddings = ResnetEmbedding(name='Resnet101').get_embedding(IMAGE_FILE_PATH)
    assert torch.tensor(embeddings).size() == expected_embeddings_size
