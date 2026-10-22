from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

from .forms import UserRegisterForm, ProfileForm
from .models import Profile

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
        self.object = form.save(False)
        user = self.object
        user.is_active = False
        user.set_password(form.cleaned_data['password'])
        user.save()

        # create profile
        Profile.objects.create(user=user)

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
        try:
            User = get_user_model()
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
        except Exception:
            messages.error(
                request,
                'Account activation failed. Invalid data'
            )
            return redirect('home')

        if not default_token_generator.check_token(user, token):
            messages.error(
                request,
                'Account activation failed. Invalid token or has expired.'
            )
            return redirect('home')
        
        user.is_active = True
        user.save()
        messages.success(
            request,
            'Account is activated. You can now log in.'
        )
        return redirect('accounts:login')
            
@login_required
def dashboard(request):
    return render(
        request,
        'accounts/dashboard.html',
    )

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/edit.html'
    success_url = reverse_lazy('accounts:edit')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        old_photo_name = self.object.photo.name
        storage = self.object.photo.storage

        response = super().form_valid(form)

        new_photo_name = self.object.photo.name
        
        if old_photo_name and old_photo_name != new_photo_name:
            storage.delete(old_photo_name)

        return response
        
        