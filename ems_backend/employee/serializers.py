
from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'department', 'position', 'phone']
        read_only_fields = ['user']
