from django.conf import settings
from django.db import models


class Post(models.Model):
	title = models.CharField(max_length=255)
	body = models.TextField()
	cover_photo = models.ImageField(upload_to='covers/', blank=True, null=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# Compatibility aliases for the existing Social Book templates.
	@property
	def image(self):
		return self.cover_photo

	@property
	def user(self):
		return self.author

	@property
	def caption(self):
		return self.body

	@property
	def no_of_likes(self) -> int:
		return self.likes.count()

	class Meta:
		ordering = ['-created_at']

	def __str__(self) -> str:
		return self.title
