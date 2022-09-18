from django.db import models


class TGAdmin(models.Model):
    """Admin user."""
    user_id = models.IntegerField(verbose_name='Telegram ID',
                                  name='user_id',
                                  unique=True)
    name = models.CharField(verbose_name='Name',
                            name='name',
                            max_length=100,)


class User(models.Model):
    """Normal user."""
    user_id = models.IntegerField(verbose_name='Telegram ID',
                                  name='user_id',
                                  unique=True)


class Course(models.Model):
    """Course."""
    name = models.CharField(verbose_name='Name',
                            name='name',
                            max_length=200)
    description = models.TextField(verbose_name='Course description',
                                   name='description',
                                   blank=False)
    order = models.IntegerField(verbose_name='Order',
                                name='order',
                                default=0)


class Recording(models.Model):
    """Recording of some user to some course."""
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             verbose_name='Recording',
                             name='recording')
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT,
                               verbose_name='Course',
                               name='course')
