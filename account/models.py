from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.




class Author(AbstractUser):
    registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}"


