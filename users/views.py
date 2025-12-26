from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from users.models import CustomUser
from users.permissions import IsOwner
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsOwner]


class UserDestroyAPIView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsOwner]
