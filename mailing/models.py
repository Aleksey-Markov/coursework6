from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


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
    start_time = models.DateTimeField(default=timezone.now)
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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

