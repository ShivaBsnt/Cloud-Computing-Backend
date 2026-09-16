from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Exercise
from .serializers import ExerciseSerializer


@extend_schema(
    responses={200: ExerciseSerializer(many=True)},
    description='List all exercises in the exercise library.',
    tags=['exercises'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exercise_list_view(request):
    exercises = Exercise.objects.all().order_by('name')
    serializer = ExerciseSerializer(exercises, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=ExerciseSerializer,
    responses={201: ExerciseSerializer},
    description='Add a new custom exercise to the library.',
    tags=['exercises'],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def exercise_create_view(request):
    serializer = ExerciseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=ExerciseSerializer,
    responses={200: ExerciseSerializer},
    description='Update an existing exercise.',
    tags=['exercises'],
)
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def exercise_update_view(request, pk):
#     try:
#         exercise = Exercise.objects.get(pk=pk)
#     except Exercise.DoesNotExist:
#         return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
#
#     serializer = ExerciseSerializer(exercise, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=ExerciseSerializer,
    responses={200: ExerciseSerializer},
    description='Partially update an existing exercise.',
    tags=['exercises'],
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def exercise_update_view(request, pk):
    try:
        exercise = Exercise.objects.get(pk=pk)
    except Exercise.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ExerciseSerializer(exercise, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses={204: None},
    description='Delete an exercise.',
    tags=['exercises'],
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def exercise_delete_view(request, pk):
    try:
        exercise = Exercise.objects.get(pk=pk)
    except Exercise.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    exercise.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)