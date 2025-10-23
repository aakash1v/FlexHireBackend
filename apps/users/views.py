from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from django.shortcuts import render
from django.conf import settings
from drf_spectacular.utils import extend_schema

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from apps.users.models import User
from apps.users.serializers import SignupSerializer, UserSerializer


def home(request):
    return render(request, 'users/home.html')


class SignupView(APIView):
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
