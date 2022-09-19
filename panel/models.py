from django.db import models


class TGAdmin(models.Model):
    """Telegram admin."""
    tg_id = models.BigIntegerField(primary_key=True,
                                   verbose_name='Telegram ID',
                                   name='tg_id',
                                   unique=True)
    name = models.CharField(verbose_name='Имя',
                            name='name',
                            max_length=100)

    class Meta:
        verbose_name = 'TGAdmin'
        verbose_name_plural = 'TGAdmins'

    def __str__(self):
        return "{} ({})".format(self.name, self.tg_id)


class User(models.Model):
    """Normal user."""
    tg_id = models.BigIntegerField(primary_key=True,
                                   verbose_name='Telegram ID',
                                   name='tg_id',
                                   unique=True)
    name = models.CharField(verbose_name='Имя',
                            name='name',
                            max_length=100)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return "{} ({})".format(self.name, self.tg_id)


class Course(models.Model):
    """Course."""
    name = models.CharField(verbose_name='Название',
                            name='name',
                            max_length=200)
    description = models.TextField(verbose_name='Описание',
                                   name='description',
                                   blank=False)
    order = models.IntegerField(verbose_name='Порядковый номер',
                                name='order',
                                default=1)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return "{}".format(self.name)


class Application(models.Model):
    """Application of some user for some course."""
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь',
                             name='user')
    course = models.ForeignKey(Course,
                               on_delete=models.PROTECT,
                               verbose_name='Курс',
                               name='course')

    class Meta:
        verbose_name = 'Заяка на курс'
        verbose_name_plural = 'Заявки на курсы'

    def __str__(self):
        return "{} -> {}".format(self.user, self.course)


class Message(models.Model):
    """Message to be sent."""

    text = models.TextField(verbose_name='Текст сообщения',
                            name='text',
                            blank=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        if len(self.text) <= 20:
            return "(ID={}) {}".format(self.id, self.text)
        return "(ID={}) {}...".format(self.id, self.text[:20])


class ScheduledMessage(models.Model):
    """Message is scheduled to send to some user."""

    message = models.ForeignKey(Message,
                                on_delete=models.PROTECT,
                                verbose_name='Сообщение',
                                name='message')

    recipient = models.ForeignKey(User,
                                  on_delete=models.PROTECT,
                                  verbose_name='Получатель',
                                  name='recipient')

    class Meta:
        verbose_name = 'Запланированная отправка'
        verbose_name_plural = 'Запланированные отправки'

    def __str__(self):
        return "{} -> {}".format(self.message, self.recipient)
