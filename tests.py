import pytest
from app import app

print("starting tests...")

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
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

print("tests done!")