from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post
from .models import Comment


class CommentApiTests(APITestCase):
	def setUp(self):
		user_model = get_user_model()
		self.author = user_model.objects.create_user(username='author2', password='password123')
		self.post = Post.objects.create(title='t', body='b', author=self.author)

	def test_create_comment_requires_auth(self):
		# Critical: unauthenticated users cannot comment.
		res = self.client.post('/api/comments/', {'post': self.post.id, 'body': 'hi'}, format='json')
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

		self.client.force_authenticate(user=self.author)
		res2 = self.client.post('/api/comments/', {'post': self.post.id, 'body': 'hi'}, format='json')
		self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
		self.assertEqual(res2.data['body'], 'hi')

		comment = Comment.objects.get(id=res2.data['id'])
		self.assertEqual(comment.author_id, self.author.id)
		self.assertEqual(comment.post_id, self.post.id)

	def test_filter_comments_by_post(self):
		# Critical: filter works via ?post=<id>
		self.client.force_authenticate(user=self.author)
		Comment.objects.create(post=self.post, author=self.author, body='c1')
		other_post = Post.objects.create(title='t2', body='b2', author=self.author)
		Comment.objects.create(post=other_post, author=self.author, body='c2')

		res = self.client.get(f'/api/comments/?post={self.post.id}')
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		# comments endpoint is also paginated by default; support both shapes.
		data = res.data.get('results', res.data)
		self.assertEqual(len(data), 1)
		self.assertEqual(data[0]['body'], 'c1')
