from django.urls import path
from .import views 

urlpatterns = [
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
    path('logout/', views.logout_view, name='logout'),
]
