from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from book.permissions import IsTokenProvided
from .serializers import CustomUserSerializer, CustomAuthTokenSerializer
from accounts.models import CustomUser


class CustomUserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_201_CREATED, headers=headers)
    
    
class CustomUserLoginView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id})


class CustomUserLogoutView(APIView):
    permission_classes = (IsTokenProvided,)

    def post(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Token '):
            return Response({'error': 'Invalid Authorization header'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]

        try:
            token = Token.objects.get(key=token)
            token.delete()
            return Response({'books': 'deleted'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
