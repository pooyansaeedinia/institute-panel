from django.contrib import admin
from my_admin.models import Courses, Avatars, WeekDays

# Register your models here.

admin.site.register(Courses)
admin.site.register(Avatars)
admin.site.register(WeekDays)

