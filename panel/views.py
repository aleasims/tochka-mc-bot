from rest_framework import permissions, viewsets

from .models import (Application, Course, Message, ScheduledMessage, TGAdmin,
                     User)
from .serializers import (ApplicationSerializer, CourseSerializer,
                          MessageSerializer, ScheduledMessageSerializer,
                          TGAdminSerializer, UserSerializer)


class TGAdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TGAdmins to be viewed or edited.
    """
    queryset = TGAdmin.objects.all().order_by('-name')
    serializer_class = TGAdminSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-name')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Courses to be viewed or edited.
    """
    queryset = Course.objects.all().order_by('-order')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Applications to be viewed or edited.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class ScheduledMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ScheduledMessages to be viewed or edited.
    """
    queryset = ScheduledMessage.objects.all()
    serializer_class = ScheduledMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
