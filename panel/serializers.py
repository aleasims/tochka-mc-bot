from rest_framework import serializers

from .models import (Application, Course, Message, ScheduledMessage, TGAdmin,
                     User)


class TGAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TGAdmin
        fields = ['tg_id', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['tg_id', 'name', 'surname', 'group_id']


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'who',
                  'where', 'day', 'time', 'img_path', 'order']


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'user', 'course']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text']


class ScheduledMessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScheduledMessage
        fields = ['id', 'message', 'recipient']
