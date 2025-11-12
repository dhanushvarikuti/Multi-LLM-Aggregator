import os
import json
from google import generativeai as genai
import requests

class MultiLLMApp:
    def __init__(self):
        # API Keys # add your keys
        os.environ['GEMINI_API_KEY'] = '**************************************'
        self.openrouter_api_key = '**************************************'
        self.llama_api_key = '**************************************'
        self.qwen_api_key = '**************************************'
        
        # Configure Gemini
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')

    def query_gemini(self, prompt, image_data=None):
        import contextlib
        import os
        try:
            with open(os.devnull, 'w') as fnull, contextlib.redirect_stderr(fnull):
                if image_data:
                    response = self.gemini_model.generate_content(
                        contents=[prompt, image_data],
                        generation_config={
                            "temperature": 0.7,
                            "max_output_tokens": 2048,
                        }
                    )
                else:
                    response = self.gemini_model.generate_content(
                        contents=prompt,
                        generation_config={
                            "temperature": 0.7,
                            "max_output_tokens": 2048,
                        }
                    )
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"

    def query_openrouter(self, prompt, image_data=None):
        url = 'https://openrouter.ai/api/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.openrouter_api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:3000',
            'X-Title': 'MultiLLMApp'
        }
        data = {
            'model': 'openai/gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}]
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            error_text = ''
            if hasattr(e, 'response') and e.response:
                error_text = e.response.text
            return f"OpenRouter Error: {e}\nResponse: {error_text}"

    def query_llama(self, prompt, image_data=None):
        url = 'https://openrouter.ai/api/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.llama_api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://github.com/llm-app',  # A fixed, valid referrer
            'X-Title': 'MultiLLMApp'
        }
        data = {
            'model': 'openai/gpt-4',  # Start with a well-supported model
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 404:
                return f"Llama Error: API endpoint not found. Check the API URL and your internet connection."
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response:
                try:
                    error_detail = e.response.json()
                    error_msg = f"{error_msg}\nAPI Error Details: {json.dumps(error_detail, indent=2)}"
                except:
                    error_msg = f"{error_msg}\nResponse Text: {e.response.text}"
            return f"Llama Error: {error_msg}"

    def query_qwen(self, prompt, image_data=None):
        url = 'https://openrouter.ai/api/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.qwen_api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:5000',
            'X-Title': 'MultiLLMApp'
        }
        data = {
            'model': 'mistralai/mixtral-8x7b-instruct',  # Using a well-supported model first
            'messages': [{'role': 'user', 'content': prompt}]
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            error_text = ''
            if hasattr(e, 'response') and e.response:
                try:
                    error_text = e.response.json()
                except:
                    error_text = e.response.text
            return f"Qwen Error: {str(e)}\nResponse: {error_text}"

    def run(self):
        query = input("Enter your query: ")
        print("\n--- Gemini Output ---")
        print(self.query_gemini(query))
        print("\n--- OpenRouter Output ---")
        print(self.query_openrouter(query))
        print("\n--- Llama Output ---")
        print(self.query_llama(query))
        print("\n--- Qwen Output ---")
        print(self.query_qwen(query))

if __name__ == "__main__":
    app = MultiLLMApp()
    app.run()
