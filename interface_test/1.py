import unittest


class TestMathFunc(unittest.TestCase):

    def setUp(self):
        print("do something befor test.prepare environment")

    def tearDown(self):
        print("do something after test.Clean up")

    def test_add(self):
        self.assertEqual(3, 3)
        self.assertNotEqual(3, 4)

    @unittest.skip("i don't want to run this case")
    def test_minus(self):
        self.assertEqual(1, 1)

    @unittest.skipIf(1 == 1, "true skip")
    def test_multi(self):
        self.assertEqual(6, 6)

    @unittest.skipUnless(1 == 2, "false skip")
    def test_divide(self):
        self.assertEqual(2, 2)
        self.assertEqual(2.5, 2)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # 使用这种方法可以对测试用例排序
    tests = [TestMathFunc("test_add"), TestMathFunc("test_minus"), TestMathFunc("test_divide")]
    # suite.addTests(tests)
    suite.addTest(TestMathFunc("test_add"))
    # 使用TestLoader的方法传入TestCase
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMathFunc))

    # 在同目录下生成txt格式的测试报告
    # with open('UnittestTextReport.txt', 'a') as f:
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
