from rest_framework import serializers
from django.contrib.auth import get_user_model
from employee.models import Employee
from employee.serializers import EmployeeSerializer

User = get_user_model()

# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    employee_details = EmployeeSerializer(required=False)  

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'employee_details']

    def create(self, validated_data):
        employee_data = validated_data.pop('employee_details', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Create employee details if user is an employee
        if user.role == 'employee' and employee_data:
            Employee.objects.create(user=user, **employee_data)

        return user



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role  # Inject 'role' into the token payload
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role  # Add 'role' to the response body
        return data
