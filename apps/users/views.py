from django.contrib.auth.models import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


from django.shortcuts import render
from django.conf import settings

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from apps.users.models import CustomerProfile, Location, User, WorkerProfile


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


def home(request):
    return render(request, 'users/home.html')


@api_view(['POST'])
def signup(request):
    data = request.data
    email = data.get('email')
    full_name = data.get('full_name')
    phone = data.get('phone')
    password = data.get('password')
    role = data.get('role')
    location_data = data.get('location')  # dictionary

    if not all([email, full_name, phone, password, role]):
        return Response({"error": "Missing required fields"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)

    user = User.objects.create(
        email=email,
        full_name=full_name,
        phone=phone,
        role=role,
        password=make_password(password),
    )

    # Create location dynamically if provided
    location = None
    if location_data:
        location = Location.objects.create(
            city=location_data.get('city', ''),
            district=location_data.get('district', ''),
            state=location_data.get('state', ''),
            pincode=location_data.get('pincode', ''),
            lat=location_data.get('lat'),
            long=location_data.get('long'),
        )

    # Create profiles
    if role in ['worker', 'both']:
        WorkerProfile.objects.create(
            user=user,
            skills=data.get('skills', []),
            location=location
        )

    if role in ['customer', 'both']:
        CustomerProfile.objects.create(
            user=user,
            location=location
        )

    return Response({"success": True, "user_id": user.id}, status=201)
