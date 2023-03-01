from rest_framework import serializers
from .models import UserProfile, DompetDigital


class UserProfileSerialize(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'age', 'status']


class DompetDigitalSerialize(serializers.ModelSerializer):
    class Meta:
        model = DompetDigital
        fields = ['saldo']
