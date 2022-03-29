from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'avatar', 'date_of_birth', 'last_time_visit', )
