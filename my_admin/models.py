from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from accounts.models import CustomUser


# Create your models here.

class Departments(models.Model):
    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


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
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
        ('MON','monday'),
        ('TUE','Tuesday'),
        ('WED','Wednesday'),
        ('THU','Thursday'),
        ('FRI','Friday'),
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
    department = models.ForeignKey(
        Departments,
        on_delete=models.CASCADE,
        related_name='departments',
        blank=True,
        null=True,
        default=1
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.SET("no teacher"),
        related_name='teacher_courses',
        limit_choices_to={'educational_group': 'teacher'},
    )
    students = models.ManyToManyField(
        CustomUser,
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
    total_time = models.IntegerField(default=0)
    week_days = models.ManyToManyField(
        WeekDays,
    )
    avatar = models.ForeignKey(
        Avatars,
        on_delete=models.SET(4),
        related_name='avatar_courses',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f'{self.course_name} - {self.course_code}'


class Sessions(models.Model):
    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        related_name='course_sessions',
    )

    note = models.TextField()

    date = models.DateField()

    absent_list = models.ManyToManyField(
        CustomUser,
        related_name='absent_sessions',
        blank=True,
        limit_choices_to={'educational_group': 'student'},
    )

    is_done = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.course} - {self.date}'


def not_in_the_past(value):
    today = timezone.localdate()
    if value < today:
        raise ValidationError("deadline must be in the past")


class Homeworks(models.Model):
    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
    )

    date = models.DateField(
        auto_now_add=True
    )

    content = models.TextField()

    deadline = models.DateField(validators=[not_in_the_past])

    end = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            for student in self.course.students.all():
                StudentHomework.objects.get_or_create(
                    homework=self,
                    student=student
                )

    def __str__(self):
        return f'{self.course} - {self.date}'


class StudentHomework(models.Model):
    homework = models.ForeignKey(
        Homeworks,
        on_delete=models.CASCADE,
        related_name="student_homeworks"
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="student_homeworks"
    )
    is_done = models.BooleanField(default=False)
    file = models.FileField(upload_to="student_homeworks/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("homework", "student")

    def mark_as_done(self, file=None):
        self.is_done = True
        if file:
            self.file = file
        self.submitted_at = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.homework} - {self.student}'