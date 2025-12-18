from __future__ import annotations

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import Profile


class Command(BaseCommand):
    help = "Create a small set of dummy users + profiles for follow/unfollow testing."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=6)
        parser.add_argument("--password", type=str, default="password123")

    def handle(self, *args, **options):
        count: int = options["count"]
        password: str = options["password"]

        created = 0
        for i in range(1, count + 1):
            username = f"demo{i}"
            email = f"{username}@example.com"

            user, was_created = User.objects.get_or_create(username=username, defaults={"email": email})
            if was_created:
                user.set_password(password)
                user.save()
                created += 1

            profile, _ = Profile.objects.get_or_create(user=user)
            if not profile.bio:
                profile.bio = f"Hi, I'm {username}."
            if not profile.location:
                profile.location = "Internet"
            profile.save()

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} new users. Password for all demo users: {password}"))
