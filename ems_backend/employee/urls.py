from django.urls import path
from .views import EmployeeListCreateView, EmployeeDetailView, EmployeeMeView, ExcelPieChartView

urlpatterns = [
    path('', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('me/', EmployeeMeView.as_view(), name='employee-me'),
    path('upload-excel/', ExcelPieChartView.as_view(), name='upload-excel'),


]
