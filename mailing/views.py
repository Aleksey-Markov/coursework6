from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from blog.models import Blog
from mailing.forms import NewsletterForm, NewsletterManagerForm
from mailing.models import Newsletter, Attempt, Mail, Client


class NewsletterListView(ListView):
    model = Newsletter


class ManagerNewsletterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'mailing.view_mailingparameters'
    model = Newsletter
    template_name = 'mailing_parameters_list.html'


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    fields = ['title', 'mail', 'start_time', 'interval', 'status', 'client']
    success_url = reverse_lazy('mailing:home')

    def form_valid(self, form):
        m_ps = form.save()
        m_ps.creator = self.request.user
        m_ps.save()
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    fields = ['name', 'mail', 'start_time', 'interval', 'status', 'client']
    success_url = reverse_lazy('mailing:list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.creator:
            return NewsletterForm
        if user.has_perm('mailing.change_status'):
            return NewsletterManagerForm
        raise PermissionDenied


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('mailing:list')


class MailListView(LoginRequiredMixin, ListView):
    model = Mail

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(creator=self.request.user)
        return qs


class MailCreateView(LoginRequiredMixin, CreateView):
    model = Mail
    fields = ['subject', 'content', ]
    success_url = reverse_lazy('mailing:create')

    def form_valid(self, form):
        message = form.save()
        message.creator = self.request.user
        message.save()
        return super().form_valid(form)


class MailUpdateView(LoginRequiredMixin, UpdateView):
    model = Mail
    fields = ['subject', 'content', ]
    success_url = reverse_lazy('mailing:message_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.creator:
            return NewsletterForm
        raise PermissionDenied


class MailDeleteView(LoginRequiredMixin, DeleteView):
    model = Mail
    success_url = reverse_lazy('mailing:message_list')


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt


def index_data(request):
    count_mailing_items = Newsletter.objects.count()
    count_active_mailing_items = Newsletter.objects.filter(status='is_active').count()
    count_unic_clients = Client.objects.values_list('email', flat=True).count()
    random_blogs = Blog.objects.order_by('?')[:3]
    context = {'count_mailing_items': count_mailing_items,
               'count_active_mailing_items': count_active_mailing_items,
               'count_unic_clients': count_unic_clients,
               'random_blogs': random_blogs,
               }

    return render(request, 'mailing/newsletter_list.html', context)
