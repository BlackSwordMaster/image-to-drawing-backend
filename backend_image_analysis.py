from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app, resources={r"/analyze-image": {"origins": "*"}})

# Set your API key from .env or environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    data = request.json
    image_data = data.get('image')

    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        # Send image to GPT-4 Vision
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe step-by-step how to draw this image scientifically."},
                        {"type": "image_url", "image_url": {"url": image_data}}
                    ]
                }
            ],
            max_tokens=800
        )

        result = response.choices[0].message.content
        return jsonify({'instructions': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
