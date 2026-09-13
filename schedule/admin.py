from django.contrib import admin
from .models import WorkoutSchedule


@admin.register(WorkoutSchedule)
class WorkoutScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'created_at', 'updated_at')
    list_filter = ('day_of_week',)
    filter_horizontal = ('exercises',)