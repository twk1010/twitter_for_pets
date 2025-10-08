import unittest

from twitter_for_pets import app

class TestTwitterForPets(unittest.TestCase):    
    def test_home_route(self):
        client = app.test_client()
        
        client.post('/tweet')
        client.post('/tweet')
        client.post('/tweet')
        
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("3 tweets", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
