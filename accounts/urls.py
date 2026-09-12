from django.urls import path
from . import views
from .views import upload_file_view

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path("upload/", upload_file_view, name="upload-file")
]
