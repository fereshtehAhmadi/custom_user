from rest_framework.response import Response
from rest_framework import status, views, permissions, pagination
from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from accounts.paginations import CustomPagination
from accounts.renders import UserRender
from accounts.models import User
from accounts.serializer import UserRegisterationSerializer, UserLoginSerializer, UserSerializer


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
                return Response({'token':token, 'msg':'login success...'}, status=status.HTTP_200_OK)
        
        return Response({'errors': {'non_field_errors':['username or password is not valid!!']}},
                        status=status.HTTP_404_NOT_FOUND)


class UserView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        serializer = UserSerializer(instance=page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(instance=user, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        user.is_active = False
        user.save()
        return Response({'msg': 'user deactivated...'})

