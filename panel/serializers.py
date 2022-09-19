from .models import TGAdmin, User, Course, Application, Message, ScheduledMessage
from rest_framework import serializers

class TGAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TGAdmin
        fields = ['tg_id', 'name']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['tg_id', 'name']

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'description', 'order']

class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ['user', 'course']

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['text']


class ScheduledMessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScheduledMessage
        fields = ['message', 'recipient']


