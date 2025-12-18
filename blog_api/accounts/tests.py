from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
	def test_signup_returns_tokens_and_user(self):

		# Critical: signup works and returns JWT tokens.
		payload = {
			"username": "alice",
			"email": "alice@example.com",
			"password": "password123",
		}
		res = self.client.post('/api/auth/signup/', payload, format='json')
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		self.assertIn('access', res.data)
		self.assertIn('refresh', res.data)
		self.assertIn('user', res.data)
		self.assertEqual(res.data['user']['username'], 'alice')

	def test_login_returns_tokens(self):
		# Critical: login endpoint returns JWT tokens for valid credentials.
		user_model = get_user_model()
		user_model.objects.create_user(username='bob', password='password123')

		res = self.client.post('/api/auth/login/', {'username': 'bob', 'password': 'password123'}, format='json')
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertIn('access', res.data)
		self.assertIn('refresh', res.data)
