from django.shortcuts import render

from my_admin.models import Courses


# Create your views here.

def dashboard(request):
    courses = Courses.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'my_admin/index.html', context)