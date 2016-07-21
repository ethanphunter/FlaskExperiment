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

testUser1 = testData["testUser1"]["username"]
testUser2 = testData["testUser2"]["username"]

addFriendPostData = {
    "friend_username" : testUser2
}

acceptFriendRequest = {
    "friend_username" : testUser1
}

startGameData = {
    "user" : testUser1
}

moves = {
    "whiteMove1" : {
        "from-row" : "7",
        "from-col" : "d",
        "to-row"   : "5",
        "to-col"   : "d"
    },
    "whiteMove2" : {
        "from-row" : "",
        "from-col" : "",
        "to-row"   : "",
        "to-col"   : ""
    },
    "blackMove1" : {
        "from-row" : "2",
        "from-col" : "c",
        "to-row"   : "4",
        "to-col"   : "c"
    },
    "blackMove2" : {
        "from-row" : "",
        "from-col" : "",
        "to-row"   : "",
        "to-col"   : ""
    }
}

@pytest.fixture
def client(request):
    client = main.app.test_client()
    return client

def doLogin(client,username,password):
    rv = client.get("/login")
    assert "Please Log In" in rv.data
    rv = client.post("/login", data={"username": username, "password": password}, follow_redirects=True)
    assert '<h2>Welcome' in rv.data

def doLogout(client):
    rv = client.get("/logout")
    assert '<h2>Logged Out</h2>' in rv.data

def test_index(client):
    rv = client.get("/")
    assert '<h2>Welcome' in rv.data

def test_login(client):
    rv = client.get("/login")
    assert "Please Log In" in rv.data

def test_main(client):
    doLogin(client,testUser1,testData["testUser1"]["password"])
    rv = client.get("/gameList")
    assert '<h2>Welcome test1' in rv.data
    rv = client.post("/addFriend", data=addFriendPostData, follow_redirects=True)
    assert 'Request sent' in rv.data
    rv = client.get("/logout")
    assert '<h2>Logged Out</h2>' in rv.data
    rv = client.post("/login", data=testData["testUser2"], follow_redirects=True)
    assert '<h2>Welcome' in rv.data
    rv = client.get("/gameList")
    assert testData["testUser1"]["username"] in rv.data
    rv = client.post("/acceptFriendRequest", data=acceptFriendRequest, follow_redirects=True)
    assert testData["testUser1"]["username"] in rv.data
    rv = client.get("/userSettings")
    assert '<title>Settings</title>' in rv.data
    doLogout(client)

def test_chessGame(client):
    doLogin(client,testUser2,testData["testUser2"]["password"])
    rv = client.post("/startGame", data=startGameData, follow_redirects=True)
    assert 'Space to Move From' in rv.data
    rv = client.post("/makeMove", data=moves["whiteMove1"], follow_redirects=True)
    assert 'Their Turn' in rv.data
    doLogout(client)
    doLogin(client,testUser1,testData["testUser1"]["password"])
    # rv = client.post()
