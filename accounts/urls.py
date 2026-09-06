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

    # password reset
    path(
        'password_reset/',
        views.PasswordResetView.as_view(),
        name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Register account
    path(
        'register/',
        views.UserRegisterView.as_view(),
        name='register'
    ),
    path(
        'register/done/',
        views.UserRegisterDoneView.as_view(),
        name='user_register_done'
    ),
    path(
        'activate/<uid>/<token>/',
        views.UserActivateView.as_view(),
        name='user_activate'
    ),
]