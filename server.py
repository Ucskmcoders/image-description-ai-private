import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import requests
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential
import io
import json
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

PORT = 8000
SECRET_KEY = os.getenv("SECRET_KEY")
API_KEYS_FILE = "api_keys.json"

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for application. Did you forget to add it to a .env file?")

base_model = InceptionV3(weights='imagenet')
model = Model(base_model.input, base_model.layers[-2].output)

tokenizer = {'word_index': {'startseq': 1, 'endseq': 2}}
max_length = 34
vocab_size = 3

rnn_model = Sequential([
    Embedding(vocab_size, 256, mask_zero=True),
    LSTM(256),
    Dense(vocab_size, activation='softmax')
])

rnn_model.compile(loss='categorical_crossentropy', optimizer='adam')

def load_image(img_data):
    img = Image.open(io.BytesIO(img_data))
    img = img.resize((299, 299))
    img = np.expand_dims(np.array(img), axis=0)
    return preprocess_input(img)

def extract_features(img_data):
    img = load_image(img_data)
    return model.predict(img)

def generate_desc(photo):
    in_text = 'startseq'
    for _ in range(max_length):
        sequence = [tokenizer['word_index'][w] for w in in_text.split() if w in tokenizer['word_index']]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = rnn_model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = {v: k for k, v in tokenizer['word_index'].items()}.get(yhat, None)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    return in_text

def load_api_keys():
    try:
        with open(API_KEYS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_api_keys(api_keys):
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(api_keys, f)

def generate_api_key(secret):
    return hashlib.sha256(secret.encode() + SECRET_KEY.encode()).hexdigest()

def is_valid_api_key(api_key):
    api_keys = load_api_keys()
    return api_key in api_keys

def add_api_key(secret):
    api_key = generate_api_key(secret)
    api_keys = load_api_keys()
    if api_key not in api_keys:
        api_keys.append(api_key)
        save_api_keys(api_keys)
    return api_key

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        api_key = query_params.get('api_key', [None])[0]
        image_url = query_params.get('image_url', [None])[0]
        secret = query_params.get('secret', [None])[0]

        if secret:
            api_key = add_api_key(secret)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'api_key': api_key}
            self.wfile.write(json.dumps(response).encode())
            return

        if not api_key or not is_valid_api_key(api_key):
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Invalid API Key'}
            self.wfile.write(json.dumps(response).encode())
            return

        if not image_url:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Missing image_url parameter'}
            self.wfile.write(json.dumps(response).encode())
            return

        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image_data = response.content
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': str(e)}
            self.wfile.write(json.dumps(response).encode())
            return

        try:
            photo = extract_features(image_data)
            description = generate_desc(photo)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'description': description}
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': str(e)}
            self.wfile.write(json.dumps(response).encode())

def main():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
