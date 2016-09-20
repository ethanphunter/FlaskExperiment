from tests.testDatabase import TestDatabase

if (__name__ == "__main__"):
    db = TestDatabase()
    gamesResult = db.getQuery("select * from games")
    usersResult = db.getQuery("select * from users")
    if (gamesResult == ["Error"]):
        print("Games Table not created!")
        raise ValueError("Database creation failed")
    elif (usersResult == ["Error"]):
        print("Users table creation failed")
        raise ValueError("Database creation failed")
