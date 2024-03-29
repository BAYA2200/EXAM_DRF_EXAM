from rest_framework.generics import CreateAPIView
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth.password_validation import validate_password

from account.models import Author

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password, ])
    password_2 = serializers.CharField(write_only=True)

    class Meta:
        model = Author
        fields = ('username', 'email', 'password', 'password_2')  # Добавил 'email' в поля

    def validate(self, data):
        if data['password'] != data['password_2']:
            raise ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = Author.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user