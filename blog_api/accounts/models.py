from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	profileimg = models.ImageField(upload_to='profiles/', blank=True, null=True)
	bio = models.TextField(blank=True, default='')
	location = models.CharField(max_length=255, blank=True, default='')
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f"Profile({self.user.username})"


class Follow(models.Model):
	follower = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='following_relations',
	)
	following = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='follower_relations',
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow_pair')
		]

	def __str__(self) -> str:
		return f"{self.follower.username} -> {self.following.username}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_user(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

