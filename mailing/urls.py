from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import NewsletterListView

app_name = MailingConfig.name

urlpatterns = [
    path('', NewsletterListView.as_view(), name='home'),
]
