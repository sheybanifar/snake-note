from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.urls import reverse_lazy

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

@login_required
def dashboard(request):
    return render(
        request,
        'accounts/dashboard.html',
    )