from asgiref.sync import sync_to_async

from panel.models import (Course, Recording, User)

from typing import List

class DatabaseManager:
    """Connect to Django ORM."""

    @sync_to_async
    def get_user(self, user_id: int) -> User:
        return User.objects.get(user_id=user_id)

    @sync_to_async
    def add_user(self, user_id: int, name: str):
        user = User(user_id=user_id, name=name)
        user.save()

    @sync_to_async
    def delete_user(self, user_id: int):
        User.objects.filter(user_id=user_id).delete()

    @sync_to_async
    def get_all_cousres(self) -> List[Course]:
        # exhausting this query set for small tables works fine
        return sorted(list(Course.objects.all()), key=lambda c: c.order)

    @sync_to_async
    def add_recording(self, user: User, course: Course):
        recording = Recording(user=user, course=course)
        recording.save()

    @sync_to_async
    def delete_recording(self, user: User, course: Course):
        Recording.objects.filter(user=user, course=course).delete()
