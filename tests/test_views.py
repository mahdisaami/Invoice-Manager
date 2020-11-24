from unittest import TestCase

from app import app, db
from models import User


class TestAuthenticatedView(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.user = User.create('info@gmail.com', '123')
        db.session.add(self.user)
        db.session.commit()

    def test_authenticated_users(self):
        user_data = {
            'email': 'info@gmail.com',
            'password': '123'
        }
        result1 = self.app.post('/login/', user_data, format='json' )
        self.assertEqual(result1.status_code, 200)

        result2 = self.app.get('/invoice_template/')
        self.assertEqual(result2.status_code, 200)
