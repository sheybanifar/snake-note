from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages

class CustomLogoutView(auth_views.LoginView):
    def dispatch(self, request, *args, **kwargs):
        message = messages.success(
            request,
            'You\'re logged out'
        )
        return super().dispatch(request, *args, **kwargs)

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    success_url = 'accounts:dashboard'
    
    def dispatch(self, request, *args, **kwargs):
        message = messages.success(
            request,
            'Your password was changed successfully')
        
        return super().dispatch(request)

@login_required
def dashboard(request):
    return render(
        request,
        'accounts/dashboard.html',
    )