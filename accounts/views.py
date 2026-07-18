from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        message = messages.success(
            request,
            'You\'re logged out'
        )
        return super().dispatch(request)

@login_required
def dashboard(request):
    return render(
        request,
        'accounts/dashboard.html',
    )