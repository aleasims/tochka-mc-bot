from asgiref.sync import sync_to_async

from panel.models import (Course, Recording, User, TGAdmin)

from typing import List, Optional


class DatabaseManager:
    """Link to Django ORM."""

    @sync_to_async
    def get_all_admins(self) -> List[TGAdmin]:
        return list(TGAdmin.objects.all())

    @sync_to_async
    def get_all_users(self) -> List[User]:
        return list(User.objects.all())

    @sync_to_async
    def get_user(self, tg_id: int) -> Optional[User]:
        try:
            user = User.objects.get(tg_id=tg_id)
            return user
        except User.DoesNotExist:
            # can't catch MultipleObjectsReturned because tg_id is a primary key
            return None

    @sync_to_async
    def add_user(self, tg_id: int, name: str):
        user = User(tg_id=tg_id, name=name)
        user.save()

    @sync_to_async
    def delete_user(self, tg_id: int):
        User.objects.filter(tg_id=tg_id).delete()

    @sync_to_async
    def get_all_cousres(self) -> List[Course]:
        # exhausting this query set for small tables works fine
        return list(Course.objects.all())

    @sync_to_async
    def add_recording(self, user: User, course: Course):
        recording = Recording(user=user, course=course)
        recording.save()

    @sync_to_async
    def delete_recording(self, user: User, course: Course):
        Recording.objects.filter(user=user, course=course).delete()
