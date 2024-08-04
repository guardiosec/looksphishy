import os
from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
from src.crawler.crawler import Crawler
from src.use_cases.use_case_llm import UseCaseLLM
from src.use_cases.use_case_embedding import UseCaseEmbedding

import conf

app = Flask(__name__)

predefined_schema = {
    "type": "object",
    "properties": {
        "site": {"type": "string"},
        "embedding_model_name": {"type": "string"},
        "llm_model_name": {"type": "string"}
    },
    "required": ["site","embedding_model_name"]
}

def validate_json(data, schema):
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise ValueError(f"JSON schema is invalid: {e.message}")

def get_values(data):
    site = data['site']
    embedding_model_name = data['embedding_model_name'].split(" ")[0]
    llm_model_name = data.get('llm_model_name')
    return site, embedding_model_name, llm_model_name

def get_html_bool(llm_model_name):
    return bool(llm_model_name)

@app.route('/calculate_similarity', methods=['POST'])
def process_request():
    data = request.json
    result = {}

    try:
        validate_json(data, predefined_schema)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    site, embedding_model_name, llm_model_name = get_values(data)
    crawler = Crawler(use_cache=True)
    html_content_bool = get_html_bool(llm_model_name)

    try:
        url = f'https://{site}'
        path_to_save = os.path.join(conf.URLS_SCANNED, f'{site}.png')
        html_content = crawler.run(url, path_to_save, html_content_bool)
        similarities = UseCaseEmbedding(embedding_model_name).run_embedding(path_to_save).to_dict(orient='records')
        result['similarities'] = similarities
        if llm_model_name:
            category = UseCaseLLM(llm_model_name).run(html_content)
            if category:
                result['category'] = category
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
