from django.forms import ModelForm

from mailing.models import Newsletter


class NewsletterForm(ModelForm):
    class Meta:
        model = Newsletter
        exclude = ('user',)


class NewsletterManagerForm(ModelForm):
    class Meta:
        model = Newsletter
        fields = ('status',)
