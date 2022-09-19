# export PYTHONPATH="/Users/chukrello/proga/tochka-mc-bot/"
from django.http import HttpResponse, HttpRequest

from rest_framework import viewsets
from rest_framework import permissions

from .models import TGAdmin, User, Course, Application, Message, ScheduledMessage
from .serializers import TGAdminSerializer, UserSerializer, CourseSerializer, ApplicationSerializer, MessageSerializer, ScheduledMessageSerializer

class TGAdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TGAdmin.objects.all().order_by('-name')
    serializer_class = TGAdminSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-name')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Course.objects.all().order_by('-name')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class ScheduledMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ScheduledMessage.objects.all()
    serializer_class = ScheduledMessageSerializer
    permission_classes = [permissions.IsAuthenticated]




def index(request: HttpRequest):
    return HttpResponse("Panel page will be here")
