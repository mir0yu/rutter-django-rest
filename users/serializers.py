from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'avatar',
                  'date_of_birth', 'last_time_visit', 'email', 'password',)
        read_only_fields = ('id', 'last_time_visit', )
        extra_kwargs = {
            'email': {'write_only': True},
            'password': {'write_only': True},
        }
