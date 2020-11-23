from unittest import TestCase

from app import app


class TestAuthenticatedView(TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_authenticated_users(self):
        result1 = self.app.get('/render_sample/')
        self.assertEqual(result1.status_code, 404)

        result2 = self.app.get('/invoice_template/')
        self.assertEqual(result2.status_code, 302)
