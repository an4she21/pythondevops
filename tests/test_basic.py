import unittest
import sys
import os
import json

# Add src directory to path so we can import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import create_app


class TestFlaskApp(unittest.TestCase):
    """Test suite for Flask application endpoints"""
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_home_page(self):
        """Test that home page returns 200 and contains expected content"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Python', response.data)
    
    def test_info_page(self):
        """Test that info page returns 200 and contains expected content"""
        response = self.client.get('/info')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hostname', response.data)
    
    def test_monitor_page(self):
        """Test that monitor page returns 200"""
        response = self.client.get('/monitor')
        self.assertEqual(response.status_code, 200)
    
    def test_api_process(self):
        """Test that /api/process endpoint returns valid JSON"""
        response = self.client.get('/api/process')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        
        data = json.loads(response.data)
        self.assertIn('processes', data)
        self.assertIsInstance(data['processes'], list)
        if len(data['processes']) > 0:
            self.assertIn('pid', data['processes'][0])
            self.assertIn('name', data['processes'][0])
    
    def test_api_monitor(self):
        """Test that /api/monitor endpoint returns valid JSON with expected keys"""
        response = self.client.get('/api/monitor')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        
        data = json.loads(response.data)
        self.assertIn('cpu', data)
        self.assertIn('mem', data)
        self.assertIn('disk', data)
        self.assertIn('net_sent', data)
        self.assertIn('net_recv', data)
        self.assertIn('disk_read', data)
        self.assertIn('disk_write', data)
        
        # Verify values are numeric
        self.assertIsInstance(data['cpu'], (int, float))
        self.assertIsInstance(data['mem'], (int, float))
        self.assertIsInstance(data['disk'], (int, float))
    
    def test_404_error(self):
        """Test that non-existent routes return 404"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
