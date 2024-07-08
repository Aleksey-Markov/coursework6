from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from mailing.models import Newsletter


class NewsletterListView(ListView):
    model = Newsletter

