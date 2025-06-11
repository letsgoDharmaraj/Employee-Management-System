from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializer
from accounts.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSelfOrAdmin


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsSelfOrAdmin]
