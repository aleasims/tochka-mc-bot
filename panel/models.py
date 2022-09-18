from django.db import models


class User(models.Model):
    user_id = models.IntegerField('user_id')

class Courses(models.Model):
    name = models.CharField('name', max_length=100)
