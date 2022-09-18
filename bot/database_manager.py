from asgiref.sync import sync_to_async

from panel.models import User

class DatabaseManager:
    """Connect to Django ORM."""

    @sync_to_async
    def get_all_users(self):
        return list(User.objects.all())
