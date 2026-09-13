from django.urls import path
from .views import exercise_list_view, exercise_create_view

urlpatterns = [
    path('exercises/', exercise_list_view, name='api_exercise_list'),
    path('exercises/create/', exercise_create_view, name='api_exercise_create'),
]