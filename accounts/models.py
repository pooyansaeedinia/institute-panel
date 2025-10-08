from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.

class CustomUser(AbstractUser):
    user_code = models.CharField(
        editable=False,
        unique=True,
        default='',
    )

    national_code = models.CharField(
        max_length=10,
        unique=True,
        default='',
    )

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

    Tel = models.CharField(
        max_length=12,
        unique=True,
        default='',
    )

    birth_date = models.DateField(default=timezone.now)

    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]

    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default='',
    )

    address = models.TextField(
        default=''
    )

    def __str__(self):
        return self.username

    def code_generator(self):
        username_numbers = str(ord(self.username[0])) + str(ord(self.username[-1]))
        national_code_number = str(self.national_code)[:3]
        phone_number_number = str(self.Tel)[8:]
        birth_date_number = str(self.birth_date)[6] + str(self.birth_date)[8:]
        full_code = username_numbers + national_code_number + phone_number_number + birth_date_number
        return full_code

    def save(self, *args, **kwargs):
        if not self.user_code:
            self.user_code = self.code_generator()
        super().save(*args, **kwargs)