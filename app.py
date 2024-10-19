import os
from flask import Flask, request, redirect, jsonify
import pyshorteners
from flask_wtf.csrf import CSRFProtect
import pyshorteners

app = Flask(__name__)
app.config['SECRET_KEY'] =  os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)  # Enable CSRF protection

s = pyshorteners.Shortener()

# In-memory storage for the shortened URLs
url_mapping = {}

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({'error': 'Empty URL provided'}), 400
    if original_url == '':
        return jsonify({'error': 'Empty URL provided'}), 400
    
    if not original_url.startswith('http://') and not original_url.startswith('https://'):
        return jsonify({'error': 'Invalid URL format'}), 400

    # Shorten the URL
    shortened_url = s.tinyurl.short(original_url)
    url_mapping[shortened_url] = original_url
    return jsonify({'shortened_url': shortened_url})

@app.route('/<path:shortened>', methods=['GET'])
def redirect_url(shortened):
    original_url = url_mapping.get(f'https://tinyurl.com/{shortened}')
    if original_url:
        #this is an addition 
        return redirect(original_url)
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)