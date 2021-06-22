import pytest


@pytest.mark.ze
def test01():
    assert 1 == 1


@pytest.mark.parametrize('case', [1,2,3])
def test02(case):
    assert case == 1

