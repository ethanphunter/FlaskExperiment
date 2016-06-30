import main
import pytest

testData = {
    "testUser1" : {
        "username" : "test1",
        "password" :  "1234"
    },
    "testUser2" : {
        "username" : "test2",
        "password" : "4321"
    }
}

addFriendPostData = {
    "friend_username" : testData["testUser2"]["username"]
}

acceptFriendRequest = {
    "friend_username" : testData["testData1"]["username"]
}

@pytest.fixture
def client(request):
    client = main.app.test_client()
    return client

def test_index(client):
    rv = client.get("/")
    assert '<h2>Welcome' in rv.data

def test_login(client):
    rv = client.get("/login")
    assert "Please Log In" in rv.data

def test_main(client):
    rv = client.get("/login")
    assert "Please Log In" in rv.data
    rv = client.post("/login", data=testData["testUser1"], follow_redirects=True)
    assert '<h2>Welcome' in rv.data
    rv = client.get("/gameList")
    assert '<h2>Welcome test1' in rv.data
    rv = client.post("/addFriend", data=addFriendPostData, follow_redirects=True)
    assert '<td>' + testData["testUser2"]["username"] in rv.data
    rv = client.get("/logout")
    assert '<h2>Logged Out</h2>' in rv.data
    rv = client.post("/login", data=testData["testUser2"], follow_redirects=True)
    assert '<h2>Welcome' in rv.data
    rv = client.post("/acceptFriendRequest", data=acceptFriendRequest, follow_redirects=True)
    assert '<td>' + testData["testUser1"]["username"] in rv.data
