from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

from .forms import UserRegisterForm

class CustomLogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        message = messages.success(
            request,
            'You\'re logged out'
        )
        return super().dispatch(request, *args, **kwargs)

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    
    success_url = reverse_lazy('accounts:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your password has been changed successfully')
        
        return response

class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy('accounts:password_reset_done')

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Your Password has been reset successfully'
        )
        return response

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:user_register_done')

    def form_valid(self, form):
        user = form.save(False)
        user.is_active = False
        user.set_password(form.cleaned_data['password'])
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        activation_path = reverse(
            'accounts:user_activate',
            kwargs={
                'uid':uid,
                'token': token
            }
        )

        activation_url = self.request.build_absolute_uri(activation_path)

        email_body = f'''Hi {user.username},
        To activate your account click on the link below:

        {activation_url}

        powered by Snake note
        '''

        email = EmailMessage(
            subject='Account activation',
            body=email_body,
            to=[user.email]
        )
        email.send()

        return HttpResponseRedirect(self.get_success_url())

class UserRegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'

class UserActivateView(View):
    def get(self, request, uid, token):
        user_id = urlsafe_base64_decode(uid).decode()
        try:
            user = get_user_model().objects.get(user_id)
        except get_user_model().DoesNotExist:
            pass

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                self.request,
                'Your account is activated. Now log in using your credentials.'
            )
            return HttpResponseRedirect('accounts:login')
        else:
            pass
@login_required
def dashboard(request):
    return render(
        request,
        'accounts/dashboard.html',
    )