from django.contrib import admin

from mailing.models import Mail, Newsletter, Attempt, Client


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'content')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'mail', 'user', 'status', 'interval')
    search_fields = ('client', 'status')
    list_filter = ('client', 'status')


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_attempt_date', 'attempt_status', 'attempt_response', 'newsletter')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    