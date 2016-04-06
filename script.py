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

def test_login(client):
    rv = client.get("/login")
    assert "Please Log In" in rv.data

def test_inventory(client):
    rv = client.get("/inventory")
    assert "<tr><td>100</td><td>soda</td>" in rv.data
