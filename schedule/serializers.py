from rest_framework import serializers
from .models import WorkoutSchedule
from exercises.serializers import ExerciseSerializer
from exercises.models import Exercise


class WorkoutScheduleSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)
    exercise_ids = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(), many=True, write_only=True, source='exercises'
    )
    muscle_groups = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutSchedule
        fields = [
            'id', 'day_of_week', 'exercises', 'exercise_ids',
            'muscle_groups', 'notes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_muscle_groups(self, obj):
        return list(obj.exercises.values_list('muscle_group', flat=True).distinct())