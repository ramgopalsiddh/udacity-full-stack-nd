import pytest
import time
import source.my_functions as my_functions

# Function based test
def test_add():
    result = my_functions.add(1,4)
    assert result == 5

def test_add_strings():
    result = my_functions.add("Ram Gopal", " Siddh")
    assert result == "Ram Gopal Siddh"

def test_divid():
    result = my_functions.divide(10,2)
    assert result == 5

def test_divid_by_zero():
    with pytest.raises(ZeroDivisionError):
        my_functions.divide(10,0)

# stop test for a given time
@pytest.mark.slow
def test_very_slow():
    time.sleep(5)
    result = my_functions.divide(10,2)
    assert result == 5

# skip the test 
@pytest.mark.skip(reason="This test is not worning currently")
def test_add_skip():
    assert my_functions.add(1,2) == 3

# mark fail and skip test
@pytest.mark.xfail(reason="we know we cannot divide by zero")
def test_divide_zero_broken():
    my_functions.divide(4,0)