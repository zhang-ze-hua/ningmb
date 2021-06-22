import pytest


@pytest.mark.usefixtures('class_fixture')
class TestCase:
    @pytest.mark.parametrize('case', [3, 4, 5])
    def test01(self, case, case_fixture):
        print("==============test01============")
        assert case > 3

    def test02(self, case_fixture):
        print("==============test02============")
        assert True
