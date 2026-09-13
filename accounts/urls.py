from django.urls import path
from . import views
from .views import upload_file_view

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_detail_view, name='profile-detail'),
    path('profile/upload-picture/', views.upload_profile_picture_view, name='profile-upload-picture'),
    path('profile/change-password/', views.change_password_view, name='profile-change-password'),
    path('profile/delete/', views.delete_account_view, name='profile-delete'),
]