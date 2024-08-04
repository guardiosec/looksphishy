def get_logo_detection_model(name):
    if name in LOGO_DETECTION_MODELS:
        return LOGO_DETECTION_MODELS[name]()
    raise Exception(f"The model {name} is not registered in the code. Register it first by adding it to "
                    f"the get_logo_detection_model function in src/models/logo_detection/__init__.py")

def create_gemini_logo_detection():
    from src.models.logo_detection.gemini import GeminiLogo
    return GeminiLogo()

LOGO_DETECTION_MODELS = {'gemini-1.5-flash-001': create_gemini_logo_detection}