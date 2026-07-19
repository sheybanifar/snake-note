from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    # login & logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # password change
    path(
        'password_change/',
        views.CustomPasswordChangeView.as_view(),
        name='password_change'),

    path('dashboard/', views.dashboard, name='dashboard')
]