# accounts/views.py

from rest_framework import generics
from accounts.serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
