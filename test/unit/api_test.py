import unittest
import pytest

from app.api import api_application


@pytest.mark.unit
class TestApi(unittest.TestCase):
    def setUp(self):
        self.client = api_application.test_client()
        api_application.config['TESTING'] = True

    def test_hello_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello from The Calculator!', response.data)

    def test_add_endpoint_correct_result(self):
        response = self.client.get('/calc/add/2/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'5', response.data)

    def test_add_endpoint_with_negative_numbers(self):
        response = self.client.get('/calc/add/-5/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'-2', response.data)

    def test_add_endpoint_with_floats(self):
        response = self.client.get('/calc/add/2.5/3.5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'6.0', response.data)

    def test_add_endpoint_with_invalid_params(self):
        response = self.client.get('/calc/add/abc/3')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'cannot be converted to number', response.data)

    def test_substract_endpoint_correct_result(self):
        response = self.client.get('/calc/substract/10/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'7', response.data)

    def test_substract_endpoint_with_negative_result(self):
        response = self.client.get('/calc/substract/3/10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'-7', response.data)

    def test_substract_endpoint_with_floats(self):
        response = self.client.get('/calc/substract/5.5/2.5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'3.0', response.data)

    def test_substract_endpoint_with_invalid_params(self):
        response = self.client.get('/calc/substract/xyz/3')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'cannot be converted to number', response.data)


if __name__ == "__main__":
    unittest.main()
