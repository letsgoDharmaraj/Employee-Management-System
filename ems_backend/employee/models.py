from django.db import models
from accounts.models import User  


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.position}"
