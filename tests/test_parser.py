from get_papers.parser import is_academic

def test_is_academic_true():
    assert is_academic("Harvard University")

def test_is_academic_false():
    assert not is_academic("Pfizer Inc.")

