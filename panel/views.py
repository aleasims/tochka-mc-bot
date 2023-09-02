from rest_framework import viewsets

from .models import (Application, Course, Message, ScheduledMessage, TGAdmin,
                     User)
from .serializers import (ApplicationSerializer, CourseSerializer,
                          MessageSerializer, ScheduledMessageSerializer,
                          TGAdminSerializer, UserSerializer,
                          GroupedScheduledMessageSerializer)


class TGAdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TGAdmins to be viewed or edited.
    """
    queryset = TGAdmin.objects.all().order_by('-name')
    serializer_class = TGAdminSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-name')
    serializer_class = UserSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Courses to be viewed or edited.
    """
    queryset = Course.objects.all().order_by('-order')
    serializer_class = CourseSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Applications to be viewed or edited.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ScheduledMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScheduledMessages to be viewed or edited.
    """
    queryset = ScheduledMessage.objects.all()
    serializer_class = ScheduledMessageSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'create' and isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return serializer_class(*args, **kwargs)

class GroupedScheduledMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScheduledMessages to be viewed or edited.
    """
    queryset = ScheduledMessage.objects.all()
    serializer_class = GroupedScheduledMessageSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'create' and isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return serializer_class(*args, **kwargs)
