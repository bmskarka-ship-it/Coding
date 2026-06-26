import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_IMAGE_URL = os.getenv('GOOGLE_IMAGE_URL', 'https://generativelanguage.googleapis.com/v1beta3/images:generate')


def generate_flower_image(count: int):
    prompt = (
        f"A realistic, photo-quality photograph of {count} exotic flowers arranged in a soft bokeh garden. "
        "Use a botanical styling with vivid petals, natural light, dew drops, and dreamy depth of field. "
        "The final image should look detailed, elegant, and very realistic."
    )

    if OPENAI_API_KEY:
        url = 'https://api.openai.com/v1/images/generations'
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': 'gpt-image-1',
            'prompt': prompt,
            'size': '1024x1024',
            'response_format': 'url',
        }
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        data = response.json()
        return data['data'][0].get('url')

    if GOOGLE_API_KEY:
        url = f'{GOOGLE_IMAGE_URL}?key={GOOGLE_API_KEY}'
        payload = {
            'model': 'gpt-image-1',
            'prompt': prompt,
            'size': '1024x1024',
        }
        response = requests.post(url, json=payload, timeout=45)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and data['data']:
            return data['data'][0].get('uri') or data['data'][0].get('url')

    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/generate', methods=['GET'])
def generate():
    try:
        flower_count = int(request.args.get('count', '10'))
    except ValueError:
        flower_count = 10

    flower_count = max(1, min(flower_count, 24))
    image_url = generate_flower_image(flower_count)

    if image_url:
        return jsonify({'image_url': image_url, 'count': flower_count})

    return jsonify({
        'error': 'No image generation API is configured. Set OPENAI_API_KEY or GOOGLE_API_KEY in the environment.',
    }), 503


if __name__ == '__main__':
    app.run(debug=True)
