import pytest
from app import app

print("starting tests...")

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'  # Add a test secret key for CSRF protection
    with app.test_client() as client:
        yield client

def test_shorten_url(client):
    response = client.post('/shorten', json={'url': 'https://www.example.com'})
    assert response.status_code == 200
    assert 'shortened_url' in response.get_json()

def test_redirect_url(client):
    # First shorten the URL
    response = client.post('/shorten', json={'url': 'https://www.example.com'})
    shortened_url = response.get_json()['shortened_url'].split('/')[-1]

    # Now redirect to the original URL
    response = client.get(f'/{shortened_url}')
    assert response.status_code == 302  # Redirect status code
    assert response.headers['Location'] == 'https://www.example.com'

def test_invalid_redirect(client):
    response = client.get('/nonexistent-url')
    assert response.status_code == 404

def test_missing_url(client):
    response = client.post('/shorten', json={})
    assert response.status_code == 400  # Bad Request
    assert response.get_json()['error'] == 'Missing URL'

def test_invalid_url_format(client):
    response = client.post('/shorten', json={'url': 'invalid-url'})
    assert response.status_code == 400  # Bad Request
    assert response.get_json()['error'] == 'Invalid URL format'

def test_empty_url(client):
    response = client.post('/shorten', json={'url': ''})
    assert response.status_code == 400  # Bad Request
    assert response.get_json()['error'] == 'Empty URL provided'

def test_shorten_url_multiple_times(client):
    url = 'https://www.example.com'
    response1 = client.post('/shorten', json={'url': url})
    response2 = client.post('/shorten', json={'url': url})
    assert response1.get_json()['shortened_url'] == response2.get_json()['shortened_url']

def test_csrf_protection(client):
    # Attempt to POST without CSRF token
    response = client.post('/shorten', json={'url': 'https://www.example.com'}, headers={'X-CSRF-Token': ''})
    assert response.status_code == 403  # Forbiddenpip install pytest pytest-cov


print("tests done!")
