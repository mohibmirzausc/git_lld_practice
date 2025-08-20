import unittest
from user import User
from group import Group

class TestSuite(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_user_creation(self):
        user1 = User("James")
        user2 = User("Bryn")

        group1 = Group("G1", user1, user2)
        print(group1)
        self.assertEqual(len(group1.users), 2)

unittest.main(verbosity=2)