from rest_framework.response import Response
from rest_framework import status, views, permissions
from rest_framework.views import APIView
from rest_framework import viewsets

from accounts.models import User
from accounts.serializer import UserRegisterationSerializer


class UserRegisterView(APIView):
    def post(self, request, format=None):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
