from flask import Flask, render_template, request, jsonify
from multi_llm_app import MultiLLMApp
from PIL import Image
import io

app = Flask(__name__)
llm_app = MultiLLMApp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    prompt = request.form.get('prompt', '')
    image = request.files.get('image')
    
    image_data = None
    if image:
        try:
            img = Image.open(image.stream)
            # Convert to RGB if needed
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            image_data = img
        except Exception as e:
            return jsonify({'error': f'Invalid image: {str(e)}'}), 400
    
    try:
        responses = {
            'gemini': llm_app.query_gemini(prompt, image_data),
            'openrouter': llm_app.query_openrouter(prompt, image_data),
            'llama': llm_app.query_llama(prompt, image_data),
            'qwen': llm_app.query_qwen(prompt, image_data)
        }
        return jsonify(responses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)