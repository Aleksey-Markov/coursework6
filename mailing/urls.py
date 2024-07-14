from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import NewsletterListView, NewsletterCreateView, NewsletterDetailView, NewsletterUpdateView, \
    NewsletterDeleteView, ManagerNewsletterListView, MailListView, MailCreateView, MailUpdateView, MailDeleteView, \
    AttemptListView, index_data

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(15)(index_data)),
    path('list/', NewsletterListView.as_view(), name='list'),
    path('create/', NewsletterCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', NewsletterDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', NewsletterUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', NewsletterDeleteView.as_view(), name='delete'),
    path('manager_list/', ManagerNewsletterListView.as_view(), name='manager_list'),

    path('message_list/', MailListView.as_view(), name='message_list'),
    path('message_create/', MailCreateView.as_view(), name='message_create'),
    path('message_edit/<int:pk>/', MailUpdateView.as_view(), name='message_edit'),
    path('message_delete/<int:pk>/', MailDeleteView.as_view(), name='message_delete'),

    path('logs_list/', AttemptListView.as_view(), name='logs_list'),
]
