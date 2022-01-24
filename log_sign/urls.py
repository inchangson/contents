from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import Main

app_name = 'log_sign'

urlpatterns = [
    # Main
    path('', Main.as_view()), 

    # LogIn
    path('login/',
        auth_views.LoginView.as_view(template_name='log_sign/login.html'),
        name='login'
    ),

    # LogOut
    path('logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # SignUp
    path('signup/', views.signup, name='signup'),
]

