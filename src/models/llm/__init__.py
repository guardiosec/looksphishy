def get_llm_model(name):
    if name in LLM_MODELS:
        return LLM_MODELS[name]()
    raise Exception(f"The model {name} is not registered in the code. Register it first by adding it to "
                    f"the get_llm_model function in src/models/llm/__init__.py")

def create_gemini_llm():
    from src.models.llm.gemini_llm import GeminiLLM
    return GeminiLLM()

def create_gpt4_llm():
    from src.models.llm.chatgpt_llm import ChatGPTLLM
    return ChatGPTLLM()

def create_llama3_llm():
    from src.models.llm.lama3 import Llama3
    return Llama3()

LLM_MODELS = {
    'gemini-1.5-flash-001': create_gemini_llm,
    'gpt4': create_gpt4_llm,
    'llama3': create_llama3_llm
    }
