from django.contrib import admin

from .models import Sessions, Departments, Homeworks, WeekDays, Courses, Avatars, StudentHomework


# Register your models here.
class SessionAdminInline(admin.TabularInline):
    model = Sessions
    fields = ['course', 'note', 'date', 'absent_list', 'is_done']
    extra = 0

class HomeworkAdmin(admin.TabularInline):
    model = Homeworks
    fields = ['course','content','deadline','end']
    extra = 0

class CoursesAdmin(admin.ModelAdmin):
    inlines = (SessionAdminInline,HomeworkAdmin)


admin.site.register(Departments)
admin.site.register(Courses, CoursesAdmin)
admin.site.register(Avatars)
admin.site.register(WeekDays)
admin.site.register(Homeworks)
admin.site.register(Sessions)
admin.site.register(StudentHomework)

