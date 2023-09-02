from django.contrib import admin

from .models import (Application, Course, Message, ScheduledMessage, TGAdmin,
                     User, GroupedScheduledMessage)

admin.site.register(Application)
admin.site.register(Course)
admin.site.register(Message)
admin.site.register(ScheduledMessage)
admin.site.register(GroupedScheduledMessage)
admin.site.register(TGAdmin)
admin.site.register(User)
