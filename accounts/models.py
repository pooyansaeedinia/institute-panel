from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CustomUser(AbstractUser):
    EDUCATIONAL_GROUP_CHOICES = [
        ('teacher', 'teacher'),
        ('student', 'student'),
        ('admin', 'admin'),
    ]

    educational_group = models.CharField(
        max_length=7,
        choices=EDUCATIONAL_GROUP_CHOICES,
        default='',
        blank=True,
        null=True,
    )

    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]

    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default='',
    )

    def __str__(self):
        return self.username