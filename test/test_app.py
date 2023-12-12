import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.tester = app.test_client()

    def test_hello_route(self):
        # Test the "/" route
        response = self.tester.get("/")
        status_code = response.status_code
        data = response.get_data(as_text=True)

        self.assertEqual(status_code, 200)
        self.assertEqual(data, "hello welcome in Movies")

    def test_about_route(self):
        # Test the "/about" route
        response = self.tester.get("/about")
        status_code = response.status_code
        data = response.get_data(as_text=True)

        self.assertEqual(status_code, 200)
        self.assertEqual(data, "This is the about page")

    def test_movies_route(self):
        # Test the "/movies" route and check the returned data
        response = self.tester.get("/movies")
        status_code = response.status_code
        data = response.get_data(as_text=True)

        expected_data = "List of movies: Movie 1, Movie 2, Movie 3"

        self.assertEqual(status_code, 200)
        self.assertEqual(data, expected_data)

    def test_invalid_route(self):
        # Test an invalid route
        response = self.tester.get("/nonexistent")
        status_code = response.status_code

        self.assertEqual(status_code, 404)

if __name__ == "__main__":
    unittest.main()
