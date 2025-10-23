from django.contrib.auth.models import make_password
from rest_framework import serializers

from apps.users.models import CustomerProfile, Location, User, WorkerProfile


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['city', 'district', 'state', 'pincode', 'lat', 'long']


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['worker', 'customer', 'both'])
    skills = serializers.ListField(
        child=serializers.CharField(), required=False)
    location = LocationSerializer(required=False)

    def create(self, validated_data):
        location_data = validated_data.pop('location', None)
        skills = validated_data.pop('skills', [])

        user = User.objects.create(
            **{**validated_data, "password": make_password(validated_data["password"])}
        )

        location = None
        if location_data:
            location = Location.objects.create(**location_data)

        if user.role in ['worker', 'both']:
            WorkerProfile.objects.create(
                user=user, skills=skills, location=location)

        if user.role in ['customer', 'both']:
            CustomerProfile.objects.create(user=user, location=location)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "phone", "role", "is_verified"]
