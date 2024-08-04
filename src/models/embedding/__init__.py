from functools import partial

def get_embedding_model(name, use_cache=False):
    if name in EMBEDDING_MODELS:
        return EMBEDDING_MODELS[name](use_cache=use_cache)
    raise Exception(f"The model {name} is not registered in the code. Register it first by adding it to "
                    f"the get_embedding_model function in src/models/embedding/__init__.py")

def create_google_embedding(name, use_cache=False):
    from src.models.embedding.google_embedding import GoogleEmbedding
    return GoogleEmbedding(name, use_cache=use_cache)

def create_clip_embedding(name, use_cache=False):
    from src.models.embedding.clip_embedding import ClipEmbedding
    return ClipEmbedding(name, use_cache=use_cache)

def create_resnet101_embedding(name, use_cache=False):
    from src.models.embedding.resnet_embedding import ResnetEmbedding
    return ResnetEmbedding(name, use_cache=use_cache)

def create_vit_embedding(name, use_cache=False):
    from src.models.embedding.vit_embedding import VitEmbedding
    return VitEmbedding(name, use_cache=use_cache)

EMBEDDING_MODELS_MAP = {
    'multimodalembedding@001-Google': create_google_embedding,
    'CLIP': create_clip_embedding,
    'Resnet101':create_resnet101_embedding,
    'ViT': create_vit_embedding
    }

EMBEDDING_MODELS = {key: partial(func, key) for key, func in EMBEDDING_MODELS_MAP.items()}
