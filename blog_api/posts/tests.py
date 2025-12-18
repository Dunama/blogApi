from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post


class PostApiTests(APITestCase):
	def setUp(self):
		# Create two users for like/unlike tests.
		user_model = get_user_model()
		self.author = user_model.objects.create_user(username='author', password='password123')
		self.other = user_model.objects.create_user(username='other', password='password123')

	def test_posts_list_is_paginated(self):
		# Critical: listing is paginated.
		Post.objects.bulk_create(
			[Post(title=f't{i}', body='body', author=self.author) for i in range(11)]
		)

		res = self.client.get('/api/posts/')
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertIn('results', res.data)
		self.assertIn('count', res.data)
		self.assertEqual(res.data['count'], 11)
		self.assertEqual(len(res.data['results']), 10)

	def test_create_post_requires_auth(self):
		# Critical: unauthenticated users cannot create posts.
		res = self.client.post('/api/posts/', {'title': 'x', 'body': 'y'}, format='json')
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

		self.client.force_authenticate(user=self.author)
		res2 = self.client.post('/api/posts/', {'title': 'x', 'body': 'y'}, format='json')
		self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
		self.assertEqual(res2.data['title'], 'x')
		self.assertEqual(res2.data['body'], 'y')

	def test_like_unlike_toggle(self):
		# Critical: like endpoint toggles like/unlike for authenticated user.
		post = Post.objects.create(title='t', body='b', author=self.author)

		self.client.force_authenticate(user=self.other)
		like1 = self.client.post(f'/api/posts/{post.id}/like/')
		self.assertEqual(like1.status_code, status.HTTP_200_OK)
		self.assertTrue(like1.data['liked'])
		self.assertEqual(like1.data['likes_count'], 1)

		like2 = self.client.post(f'/api/posts/{post.id}/like/')
		self.assertEqual(like2.status_code, status.HTTP_200_OK)
		self.assertFalse(like2.data['liked'])
		self.assertEqual(like2.data['likes_count'], 0)
