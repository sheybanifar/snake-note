from django.shortcuts import render
from django.shortcuts import redirect

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('accounts:dashboard')