from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.UserRegistration,name='register'),
    path('', views.LoginPage, name='login'),
    path('adminv/', views.adminView, name='admin_view'),
    path('userv/', views.userView, name='user_view'), # Example route
    path('', views.Logout, name='logout'), # Example route
]