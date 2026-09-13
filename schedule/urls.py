from django.urls import path
from .views import schedule_list_view, schedule_create_view, schedule_update_view, schedule_delete_view

urlpatterns = [
    path('schedule/', schedule_list_view, name='api_schedule_list'),
    path('schedule/create/', schedule_create_view, name='api_schedule_create'),
    path('schedule/<int:pk>/', schedule_update_view, name='api_schedule_update'),
    path('schedule/<int:pk>/delete/', schedule_delete_view, name='api_schedule_delete'),
]