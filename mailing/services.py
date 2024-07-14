import smtplib

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from blog.models import Blog
from config.settings import CACHE_ENABLED
from mailing.models import Newsletter, Attempt, Client


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=60)
    scheduler.start()


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    print('начало проверки дат окончания активных рассылок')
    for mailing in Newsletter.objects.all():
        if mailing.start_time > current_datetime and mailing.status == 'send':
            mailing.status = ['ended']
            mailing.save()

    mailings = (
        Newsletter.objects.filter(start_time__lte=current_datetime).filter(status__in=['send']).filter(
            next_date__lte=current_datetime))

    for mailing in mailings:

        rl = [client_.email for client_ in mailing.Client.all()]
        server_response = ''
        status = False
        try:
            server_response = send_mail(
                subject=mailing.mail.theme,
                message=mailing.mail.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=rl,
                fail_silently=False
            )
            server_response = str(server_response)
            status = True
        except smtplib.SMTPException as e:
            server_response = str(e)
            status = False
        finally:
            log = Attempt(status=status, response=server_response, last_time_sending=current_datetime,
                       mailing_parameters=mailing)
            print(log)
            log.save()

            next_date_calculated = None

            if mailing.interval == 'per_day':
                next_date_calculated = mailing.next_date + timezone.timedelta(days=1)
            elif mailing.interval == 'per_week':
                next_date_calculated = mailing.next_date + timezone.timedelta(days=7)
            elif mailing.interval == 'per_month':
                next_date_calculated = mailing.next_date + timezone.timedelta(days=30)

            if next_date_calculated > mailing.end_time:
                if status:
                    mailing.status = 'finished'
                else:
                    mailing.status = 'finished_error'
            else:
                mailing.next_date = next_date_calculated

            mailing.save()


def get_blog_from_cache():
    if not CACHE_ENABLED:
        return Blog.objects.order_by('?')[:3]

    key = 'blog_list'
    blog_list = cache.get(key)
    if blog_list is None:

        blog_list = Blog.objects.order_by('?')[:3]
        cache.set(key, blog_list)
    return blog_list
