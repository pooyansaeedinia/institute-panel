from django.shortcuts import render

from my_admin.models import Courses, Departments


# Create your views here.

def course_list(request):
    courses = Courses.objects.all()
    departments = Departments.objects.all()
    context = {
        'courses': courses,
        'departments': departments,
    }
    return render(request, 'my_admin/index.html', context)


def course_detail(request, course_id):
    pass