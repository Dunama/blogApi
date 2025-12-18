from rest_framework import permissions, viewsets

from blog_api.permissions import IsAuthorOrReadOnly

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

	def get_queryset(self):
		queryset = Comment.objects.select_related('author', 'post')
		post_id = self.request.query_params.get('post')
		if post_id:
			queryset = queryset.filter(post_id=post_id)
		return queryset

	def perform_create(self, serializer):
		# Persist the current user as the author of the comment.
		serializer.save(author=self.request.user)
