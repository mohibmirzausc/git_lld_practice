import unittest

class TestSuite(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def test_case(self):
        print("test_case")

    def tearDown(self):
        print("tearDown")

if __name__ == "__main__":
    unittest.main(verbosity=2)