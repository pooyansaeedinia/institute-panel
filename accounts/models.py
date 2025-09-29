from django.contrib.auth.models import AbstractUser
from django.db import models

from teacher.models import Profile


# Create your models here.


class CustomUser(AbstractUser):
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        Profile.objects.get_or_create(user=self)

    def __str__(self):
        return self.username