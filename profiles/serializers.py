# profiles/serializers.py

from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'photo', 'address']
        read_only_fields = ['user']
