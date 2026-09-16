from django.urls import path
from .views import exercise_list_view, exercise_create_view, exercise_update_view, exercise_delete_view

urlpatterns = [
    path('exercises/', exercise_list_view, name='api_exercise_list'),
    path('exercises/create/', exercise_create_view, name='api_exercise_create'),
    path('exercises/<int:pk>/', exercise_update_view, name='api_exercise_update'),
    path('exercises/<int:pk>/delete/', exercise_delete_view, name='api_exercise_delete'),
]