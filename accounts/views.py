from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Profile
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
)
from .supabase_storage import upload_profile_picture
from authbackend.storage import upload_file


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
    description='Login using username and password and receive an authentication token.',
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


@extend_schema_view(
    get=extend_schema(
        description="Retrieve the logged-in user's profile",
        responses={200: ProfileSerializer},
    ),
    patch=extend_schema(
        description="Update bio, phone, name, or email",
        request=ProfileSerializer,
        responses={200: ProfileSerializer},
    ),
)
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_detail_view(request):
    """
    GET   /api/profile/ -> view full profile
    PATCH /api/profile/ -> update bio, phone, name, email
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'image': {
                    'type': 'string',
                    'format': 'binary',
                }
            },
            'required': ['image'],
        }
    },
    description='Upload or replace the profile picture. Send as multipart/form-data with field "image".',
)
@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def upload_profile_picture_view(request):
    if 'image' not in request.FILES:
        return Response({'detail': 'No image file provided.'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['image']
    profile, _ = Profile.objects.get_or_create(user=request.user)

    try:
        public_url = upload_profile_picture(file, request.user.id)
    except Exception as e:
        return Response({'detail': f'Upload failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    profile.profile_picture_url = public_url
    profile.save()

    return Response({'profile_picture_url': public_url}, status=status.HTTP_200_OK)


@extend_schema(
    request=ChangePasswordSerializer,
    responses={200: dict},
    description='Change the current password. Invalidates the existing token.',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        # Invalidate old token, force re-login with new password
        Token.objects.filter(user=user).delete()
        return Response(
            {'detail': 'Password changed successfully. Please log in again.'},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: dict},
    description='Permanently delete the currently authenticated user\'s account.',
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account_view(request):
    user = request.user
    user.delete()
    return Response({'detail': 'Account deleted successfully.'}, status=status.HTTP_200_OK)


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
    description='Upload a general file (not a profile picture) to cloud storage.',
)
@api_view(["POST"])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
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