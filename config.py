# config.py
import openai

def load_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

API_KEY = load_api_key(r"API_KEY.txt")
openai.api_key = API_KEY