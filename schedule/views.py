from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import WorkoutSchedule
from .serializers import WorkoutScheduleSerializer


@extend_schema(
    responses={200: WorkoutScheduleSerializer(many=True)},
    description="Get the logged-in user's full week schedule.",
    tags=['schedule'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def schedule_list_view(request):
    schedules = WorkoutSchedule.objects.filter(user=request.user).order_by('day_of_week')
    serializer = WorkoutScheduleSerializer(schedules, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=WorkoutScheduleSerializer,
    responses={201: WorkoutScheduleSerializer},
    description="Create a schedule entry for a day.",
    tags=['schedule'],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_create_view(request):
    serializer = WorkoutScheduleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=WorkoutScheduleSerializer,
    responses={200: WorkoutScheduleSerializer},
    description="Update an existing schedule entry.",
    tags=['schedule'],
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def schedule_update_view(request, pk):
    try:
        schedule = WorkoutSchedule.objects.get(pk=pk, user=request.user)
    except WorkoutSchedule.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = WorkoutScheduleSerializer(schedule, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: None},
    description="Delete a schedule entry.",
    tags=['schedule'],
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def schedule_delete_view(request, pk):
    try:
        schedule = WorkoutSchedule.objects.get(pk=pk, user=request.user)
    except WorkoutSchedule.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    schedule.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)