from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from blog_api.permissions import IsAuthorOrReadOnly

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.select_related('author').prefetch_related('likes')
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
	parser_classes = [MultiPartParser, FormParser, JSONParser]

	def perform_create(self, serializer):
		# Persist the current user as the author of the post.
		serializer.save(author=self.request.user)

	@action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
	def like(self, request, pk=None):
		post = self.get_object()
		user = request.user
		if post.likes.filter(id=user.id).exists():
			post.likes.remove(user)
			liked = False
		else:
			post.likes.add(user)
			liked = True

		return Response({'liked': liked, 'likes_count': post.likes.count()}, status=status.HTTP_200_OK)
