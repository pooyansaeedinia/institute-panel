from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='users',
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

    def __str__(self):
        return self.user.username


class Avatars(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class WeekDays(models.Model):
    WEEK_DAYS_CHOICES = (
        'SAT','SUN','MON','TUE',
        'WED','THU','FRI',
    )
    name = models.CharField(
        max_length=4,
        choices=WEEK_DAYS_CHOICES,
    )

    def __str__(self):
        return self.name


class Courses(models.Model):
    course_name = models.CharField(
        max_length=100,
    )
    teacher = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='teacher_courses',
        limit_choices_to={'educational_group': 'teacher'},
    )
    students = models.ManyToManyField(
        Profile,
        related_name='students_courses',
        blank=True,
        limit_choices_to={'educational_group': 'student'}
    )
    course_code = models.CharField(
        max_length=6,
        unique=True,
        db_index=True,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    week_days = models.ManyToManyField(
        WeekDays,
    )
    avatar = models.ForeignKey(
        Avatars,
        on_delete=models.CASCADE,
        related_name='avatar_courses',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f'{self.course_name} - {self.course_code}'
