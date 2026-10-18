import pytest
from calc import evaluate


@pytest.mark.parametrize("expr,res", [
    ("2+3", 5), ("2+3*4", 14), ("10÷4", 2.5), ("6×7", 42),
    ("-5+2", -3), ("0.1+0.2", 0.3), ("8/2", 4),
])
def test_ok(expr, res):
    assert evaluate(expr) == res


@pytest.mark.parametrize("expr", ["1/0", "2+", "__import__('os')", "abc"])
def test_bad(expr):
    with pytest.raises(Exception):
        evaluate(expr)
