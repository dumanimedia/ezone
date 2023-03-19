from django.contrib.auth.models import User
from django.db import models


class Userprofile(models.Model):
    user = models.OneToOneField(
        User, related_name="userprofile", on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def user_fullname(self):
        return f"{self.first_name} {self.last_name}"
