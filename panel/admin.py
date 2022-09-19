from django.contrib import admin

from .models import Course, Recording, TGAdmin, User

admin.site.register(Course)
admin.site.register(Recording)
admin.site.register(TGAdmin)
admin.site.register(User)
