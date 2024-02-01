from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, AbstractUser
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Author
from account.serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    queryset = Author.objects.all()
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK, )
            else:
                return Response({'detail': 'User account is not active'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
