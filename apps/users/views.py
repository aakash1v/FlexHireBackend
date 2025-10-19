from django.contrib.auth.models import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.users.models import CustomerProfile, Location, User, WorkerProfile

from django.shortcuts import render


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
