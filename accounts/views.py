from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


@extend_schema(
    request=RegisterSerializer,
    responses={201: UserSerializer},
    description='Register a new user and receive an authentication token.',
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'user': UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,
    responses={200: UserSerializer},
    description='Login using email and password and receive an authentication token.',
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'user': UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses={200: dict},
    description='Logout the currently authenticated user.',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)

@extend_schema(
    responses={200: UserSerializer},
    description='Get the profile of the currently authenticated user.',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    return Response(
        UserSerializer(request.user).data,
        status=status.HTTP_200_OK,
    )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authbackend.storage import upload_file

@extend_schema(
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "format": "binary",
                }
            },
            "required": ["file"],
        }
    },
    responses={201: dict},
)
@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_file_view(request):

    file = request.FILES.get("file")

    if not file:
        return Response(
            {"error": "No file provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    path = upload_file(file)

    return Response(
        {
            "message": "File uploaded successfully",
            "path": path,
        },
        status=status.HTTP_201_CREATED,
    )