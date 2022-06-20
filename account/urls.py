from django.urls import path, include
from django.contrib.auth import views as auth_views


from .views import user_login, user_logout, register

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'),
         name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),
         name='password_change_done'),
    path('register/', register, name='register'),


]
