from Database_Module.models import Success, Failure

def testSuccess():
    s = Success("A value")
    """A Success should:"""

    """Return True for isSuccess"""
    assert s.isSuccess() == True

    """Return False for isFailure"""
    assert s.isFailure() == False

    """Return the value for get"""
    assert s.get() == "A value"

    """Return the value for getOrElse"""
    assert s.getOrElse("Not a value") == "A value"

def testFailure():
    f = Failure("A failure message")
    """A Failure should:"""

    """Return False for isSuccess"""
    assert f.isSuccess() == False

    """Return True for isFailure"""
    assert f.isFailure() == True

    """Return None for get"""
    assert f.get() == None

    """Return the given value for getOrElse"""
    assert f.getOrElse("Not a value") == "Not a value"

    """Return the error message"""
    assert f.getErrorMessage() == "A failure message"
