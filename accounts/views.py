from rest_framework.response import Response
from rest_framework import status, views, permissions
from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from accounts.renders import UserRender
from accounts.models import User
from accounts.serializer import UserRegisterationSerializer, UserLoginSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                login(request, user)
                return Response({'token':token, 'msg':'login success...'}, status=status.HTTP_200_OK)
        
        return Response({'errors': {'non_field_errors':['username or password is not valid!!']}},
                        status=status.HTTP_404_NOT_FOUND)

