import main
import pytest

print("tests!!!")

@pytest.fixture
def client(request):
    client = main.app.test_client()
    return client

def test_index(client):
    rv = client.get("/")
    assert 'forms' in rv.data
