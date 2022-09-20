from asgiref.sync import sync_to_async

from panel.models import (Course, Application, User,
                          TGAdmin, Message, ScheduledMessage)

from typing import List, Optional


class DatabaseManager:
    """Link to Django ORM."""

    # exhausting query sets for small tables works fine

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
    def update_user(self, tg_id: int, **kwargs):
        """This function can update User info.
        Accepts possible keyword args: `name`, `surname`, `group_id`
        """

        try:
            user = User.objects.get(tg_id=tg_id)
        except User.DoesNotExist:
            return

        name = kwargs.get('name')
        surname = kwargs.get('surname')
        group_id = kwargs.get('group_id')
        if name is not None:
            user.name = name
        if surname is not None:
            user.surname = surname
        if group_id is not None:
            user.group_id = group_id
        user.save()

    @sync_to_async
    def delete_user(self, tg_id: int):
        User.objects.filter(tg_id=tg_id).delete()

    @sync_to_async
    def get_all_cousres(self) -> List[Course]:
        return list(Course.objects.all())

    @sync_to_async
    def get_course(self, course_id: int) -> Optional[Course]:
        try:
            course = Course.objects.get(id=course_id)
            return course
        except Course.DoesNotExist:
            return None

    @sync_to_async
    def add_application(self, user: User, course: Course):
        application = Application(user=user, course=course)
        application.save()

    @sync_to_async
    def get_applications(self, user_id: int) -> List[Application]:
        applications = list(Application.objects.filter(user=user_id))
        return applications

    @sync_to_async
    def delete_application(self, user_id: int, course_id: int):
        Application.objects.filter(user=user_id, course=course_id).delete()

    @sync_to_async
    def get_all_messages(self) -> List[Message]:
        return list(Message.objects.all())

    @sync_to_async
    def get_message(self, id_: int) -> Optional[Message]:
        try:
            message = Message.objects.get(id=id_)
            return message
        except Message.DoesNotExist:
            return None

    @sync_to_async
    def get_all_scheduled_messages(self) -> List[ScheduledMessage]:
        return list(ScheduledMessage.objects.all())

    @sync_to_async
    def get_recipients(self, message: Message) -> List[ScheduledMessage]:
        return list(sc.recipient for sc in ScheduledMessage.objects.filter(message=message))

    @sync_to_async
    def delete_scheduled_message(self, id_: int):
        ScheduledMessage.objects.filter(id=id_).delete()
