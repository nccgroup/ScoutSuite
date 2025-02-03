import unittest
from unittest.mock import patch
from ScoutSuite.providers.base.provider import BaseProvider

class MockBaseProvider(BaseProvider):
    """Mock class to test BaseProvider without requiring metadata"""
    def __init__(self):
        self.metadata = {}
        self.last_run = None
        self.services = {}

    def _load_metadata(self):
        """Override to prevent metadata loading"""
        pass

class TestBaseProvider(unittest.TestCase):
    def setUp(self):
        """Set up a BaseProvider instance for testing"""
        self.provider = MockBaseProvider()

    def test_manage_object_dict(self):
        """Test manage_object with dictionary input"""
        # Test adding new key to dictionary
        test_dict = {}
        result = self.provider.manage_object(test_dict, 'new_key', 'test_value')
        self.assertEqual(result['new_key'], 'test_value')
        
        # Test existing key in dictionary
        test_dict = {'existing_key': 'old_value'}
        result = self.provider.manage_object(test_dict, 'existing_key', 'new_value')
        self.assertEqual(result['existing_key'], 'old_value')  # Should not change existing value

    def test_manage_object_class(self):
        """Test manage_object with class object input"""
        class TestClass:
            pass
        
        # Test adding new attribute
        test_obj = TestClass()
        result = self.provider.manage_object(test_obj, 'new_attr', 'test_value')
        self.assertEqual(result.new_attr, 'test_value')
        
        # Test existing attribute
        test_obj = TestClass()
        setattr(test_obj, 'existing_attr', 'old_value')
        result = self.provider.manage_object(test_obj, 'existing_attr', 'new_value')
        self.assertEqual(result.existing_attr, 'old_value')  # Should not change existing value

    def test_manage_object_callback(self):
        """Test manage_object with callback function"""
        callback_called = {'value': None}
        
        def test_callback(value):
            callback_called['value'] = value

        # Test callback with dictionary
        test_dict = {}
        self.provider.manage_object(test_dict, 'callback_key', 'callback_value', callback=test_callback)
        self.assertEqual(callback_called['value'], 'callback_value')

        # Test callback with object
        class TestClass:
            pass
        test_obj = TestClass()
        callback_called['value'] = None  # Reset callback value
        self.provider.manage_object(test_obj, 'callback_attr', 'callback_value', callback=test_callback)
        self.assertEqual(callback_called['value'], 'callback_value')

    def test_manage_object_no_infinite_loop(self):
        """Test that manage_object doesn't cause infinite recursion"""
        # This test would have failed with the original implementation
        test_dict = {}
        try:
            self.provider.manage_object(test_dict, 'test_key', 'test_value')
        except RecursionError:
            self.fail("manage_object caused infinite recursion")

if __name__ == '__main__':
    unittest.main()
