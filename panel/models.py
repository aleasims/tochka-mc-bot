from django.db import models


class TGAdmin(models.Model):
    """Admin user."""
    tg_id = models.IntegerField(verbose_name='Telegram ID',
                                name='tg_id',
                                unique=True)
    name = models.CharField(verbose_name='Name',
                            name='name',
                            max_length=100)


class User(models.Model):
    """Normal user."""
    tg_id = models.IntegerField(verbose_name='Telegram ID',
                                name='tg_id',
                                unique=True)
    name = models.CharField(verbose_name='Name',
                            name='name',
                            max_length=100)


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
                                default=1)


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
