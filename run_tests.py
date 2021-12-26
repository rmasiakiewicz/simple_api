import unittest

from api import app


class ApiTest(unittest.TestCase):

    def test_status(self):
        api = app.test_client(self)
        response = api.get("/app/user_task")
        self.assertEqual(response.status_code, 200)

    def test_response_content_type(self):
        api = app.test_client(self)
        response = api.get("/app/user_task")
        self.assertEqual(response.content_type, "text/csv")

    def test_content_is_not_empty(self):
        api = app.test_client(self)
        response = api.get("/app/user_task")
        self.assertGreater(response.content_length, 0)


if __name__ == "__main__":
    unittest.main()
