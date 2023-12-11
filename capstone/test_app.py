import unittest
try:
    from app import app
except ImportError as e:
    print("Some modules are missing: {}".format(e))

class FlaskTestCase(unittest.TestCase):
    
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

if __name__ == "__main__":
    unittest.main()
