import vertexai
from vertexai.generative_models import Image, GenerativeModel

MODEL_NAME = 'gemini-1.5-flash-001'
vertexai.init()
MODEL = GenerativeModel(MODEL_NAME)


class GeminiLogo(object):
    name = MODEL_NAME
    task = (
        'Following is a website screenshot. '
        'Identify whether the screenshot includes the website logo and determine the brand associated with it. '
        'In your answer specify only the name of this brand.'
    )

    def run(self, path):
        response = MODEL.generate_content([Image.load_from_file(path), self.task])
        return response.text
