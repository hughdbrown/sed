import unittest

#from mock import Mock, patch
from nose.tools import (
    raises,
    assert_true, assert_false, assert_equals
)


class TestSed(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        assert_true(True)
