from rest_framework import generics, permissions, status
from .serializers import UserProfileSerializer, UserSerializer, UserUpdateSerializer
from .models import User
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.utils.email_utils import send_otp, send_welcome_email
from .serializers import CustomTokenObtainPairSerializer

from django.shortcuts import render
from django.conf import settings
from drf_spectacular.utils import extend_schema

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from apps.users.models import EmailOTP, User
from apps.users.serializers import SignupSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def home(request):
    return render(request, 'users/home.html')


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request=SignupSerializer,
        responses={201: UserSerializer},
        description="Register a new user (worker, customer, or both)."
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(UserSerializer(user).data, status=201)


@api_view(['POST'])
def google_auth(request):
    token = request.data.get("token")
    if not token:
        return Response({"error": "Token not provided", "status": False}, status=status.HTTP_400_BAD_REQUEST)

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID
        )
        print(id_info)
        email = id_info['email']
        first_name = id_info.get('given_name', '')
        last_name = id_info.get('family_name', '')
        profile_pic_url = id_info.get('picture', '')

        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_unusable_password()
            user.full_name = f"{first_name} {last_name}"
            user.registration_method = 'google'
            user.save()
        else:
            if user.registration_method != 'google':
                return Response({
                    "error": "User needs to sign in through email",
                    "status": False
                }, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                "status": True
            },
            status=status.HTTP_200_OK
        )

    except ValueError:
        return Response({"error": "Invalid token", "status": False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    authentication_classes = []

    email = request.data.get("email")
    otp = request.data.get("otp")

    if not email or not otp:
        return Response({"detail": "Email and OTP required"}, status=400)

    try:
        record = EmailOTP.objects.get(email=email)
    except EmailOTP.DoesNotExist:
        return Response({"detail": "OTP not found. Please request a new one."}, status=400)

    if record.is_expired():
        record.delete()
        return Response({"detail": "OTP expired. Please request a new one."}, status=400)

    if record.otp != str(otp):
        return Response({"detail": "Invalid OTP"}, status=400)

    # ✅ OTP is correct → verify user
    user = User.objects.filter(email=email).first()
    if user:
        user.is_verified = True
        user.save()

    # Cleanup OTP
    record.delete()
    send_welcome_email(email, user.full_name)

    return Response({"detail": "Email verified successfully!"}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def resend_otp(request):
    """
    Resend OTP to user's email if previous OTP expired or user requests new one
    """
    email = request.data.get("email")

    if not email:
        return Response({"detail": "Email is required"}, status=400)

    # Check if user exists
    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"detail": "No account found with this email"}, status=400)

    # Delete any existing OTP for this email (optional but cleaner)
    EmailOTP.objects.filter(email=email).delete()

    # Send new OTP
    send_otp(email, user.full_name)

    return Response({"detail": "A new OTP has been sent to your email."}, status=200)


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET: Return the full profile of the authenticated user (with nested details)
    PUT/PATCH: Update basic profile fields (full_name, phone, bio, profile_image)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        # GET → full nested profile
        if self.request.method == "GET":
            return UserProfileSerializer
        # PUT/PATCH → update limited fields
        return UserUpdateSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserProfileSerializer(self.get_object()).data)

    patch = put  # optional shortcut for PATCH requests


class UploadProfilePhotoView(generics.GenericAPIView):
    """
    POST: Upload or update profile picture
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user = request.user
        profile_image = request.FILES.get("profile_image")

        if not profile_image:
            return Response({"error": "No profile_image file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Save file to user's profile_image field
        user.profile_image = profile_image
        user.save()

        return Response({
            "message": "Profile picture uploaded successfully",
            "profile_image_url": request.build_absolute_uri(user.profile_image.url)
        }, status=status.HTTP_200_OK)


class PublicUserView(generics.RetrieveAPIView):
    """
    GET: View another user's public profile
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"
