from django.contrib.auth.models import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import CustomerProfile, Location, User, WorkerProfile
from apps.utils.email_utils import send_otp


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["city", "district", "state", "pincode", "lat", "long"]


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=["worker", "customer", "both"])
    skills = serializers.ListField(child=serializers.CharField(), required=False)
    location = LocationSerializer(required=False)

    def create(self, validated_data):
        location_data = validated_data.pop("location", None)
        skills = validated_data.pop("skills", [])

        user = User.objects.create(**{**validated_data, "password": make_password(validated_data["password"])})

        location = None
        if location_data:
            location = Location.objects.create(**location_data)

        if user.role in ["worker", "both"]:
            WorkerProfile.objects.create(user=user, skills=skills, location=location)

        if user.role in ["customer", "both"]:
            CustomerProfile.objects.create(user=user, location=location)

        send_otp(validated_data.get("email"), validated_data.get("full_name"))
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role", "is_verified"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extend default token serializer to include user info in response.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Optional: Add custom claims in JWT payload if needed
        token["email"] = user.email
        token["role"] = user.role
        token["full_name"] = user.full_name

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user info to response
        data["user"] = {
            "id": str(self.user.id),
            "full_name": self.user.full_name,
            "email": self.user.email,
            "phone": self.user.phone,
            "role": self.user.role,
            "is_verified": self.user.is_verified,
            "profile_image": (self.user.profile_image if self.user.profile_image else None),
        }

        return data


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["city", "district", "state", "pincode", "lat", "long"]


class WorkerProfileSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = WorkerProfile
        fields = [
            "skills",
            "experience_years",
            "hourly_rate",
            "work_radius_km",
            "is_available",
            "location",
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = CustomerProfile
        fields = ["address", "verified_badge", "location"]


class UserProfileSerializer(serializers.ModelSerializer):
    worker_profile = WorkerProfileSerializer(read_only=True)
    customer_profile = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "role",
            "bio",
            "profile_image",
            "is_verified",
            "avg_rating",
            "registration_method",
            "worker_profile",
            "customer_profile",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["email", "registration_method", "created_at", "updated_at"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "phone", "bio", "profile_image"]
