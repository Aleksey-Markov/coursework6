import secrets

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView

from users.forms import UserRegisterForm, UserForm, ModeratorUserForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.activation_token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}/'
        send_mail(
            'Confirm your email',
            f'To activate your account, click the following link: {url}',
            'EMAIL_HOST_USER',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


def email_verification(self, request, token):
    user = get_object_or_404(User, activation_token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('change_user_status'):
            return ModeratorUserForm
        if user.is_active:
            return UserForm
        raise PermissionDenied
