from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserRegistrationSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from rest_framework.permissions import AllowAny


from django.contrib.auth import get_user_model

User = get_user_model()


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterUserView(APIView):
    permission_classes = []  # No authentication required

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'If the email exists, a reset link has been sent.'})  # Do not leak info

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"

        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({'detail': 'If the email exists, a reset link has been sent.'})




class PasswordResetConfirmView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not (uidb64 and token and new_password):
            return Response({'error': 'Missing data'}, status=400)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'error': 'Invalid UID'}, status=400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password has been reset successfully.'})


