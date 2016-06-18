import os
import unittest


class HelloTest(unittest.TestCase):
    
    def setUp(self):
        super(HelloTest, self).setUp()

    def test_hello(self):
        print "HELLO"
        self.assertEqual('hello', 'poop')

