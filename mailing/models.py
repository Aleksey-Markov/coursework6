from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Адрес электронной почты')
    name = models.CharField(max_length=100, verbose_name='Имя клиента')
    comment = models.TextField(verbose_name='Комментарий клиента', **NULLABLE)

    def __str__(self):
        return f' Клиент: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mail(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Содержание письма')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение рассылки'
        verbose_name_plural = 'Сообщения рассылки'


class Newsletter(models.Model):

    title = models.CharField(max_length=100, verbose_name='Название рассылки', **NULLABLE, default='Без названия')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='начало рассылки')
    periodicity = (
        ('per_day', 'раз в день'),
        ('per_week', 'раз в неделю'),
        ('per_month', 'раз в месяц')
    )
    mail_status = (
        ('active', 'Создана'),
        ('send', 'Запущена'),
        ('ended', 'Завершена')
    )
    interval = models.CharField(max_length=25, choices=periodicity, default='per_week', verbose_name='Периодичность')
    status = models.CharField(max_length=25, choices=mail_status, default='active', verbose_name='Статус рассылки')
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, verbose_name='Сообщение рассылки')
    client = models.ManyToManyField(Client, verbose_name='Клиент')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Attempt(models.Model):
    last_attempt_date = models.DateTimeField(auto_now=True, verbose_name='Дата последней попытки', **NULLABLE)
    attempt_status = models.BooleanField(default=False, verbose_name='статус')
    attempt_response = models.CharField(max_length=250, verbose_name='ответ почтового сервиса', **NULLABLE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f'''Попытка отправки рассылки {self.newsletter.title} от {self.last_attempt_date}
    Статус: {self.attempt_status}
    Ответ сервера: {self.attempt_response}
    Состояние рассылки: {self.newsletter.status}'''

    class Meta:
        verbose_name = 'Попытка отправки рассылки'
        verbose_name_plural = 'Попытки отправки рассылки'

