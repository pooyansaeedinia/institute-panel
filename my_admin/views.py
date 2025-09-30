from django.shortcuts import render

from my_admin.models import Courses, Departments, Sessions, Homeworks


# Create your views here.

def course_list(request):
    courses = Courses.objects.all()
    departments = Departments.objects.all()
    context = {
        'courses': courses,
        'departments': departments,
    }
    return render(request, 'my_admin/course-list.html', context)


def course_detail(request, code):
    course = Courses.objects.get(course_code=code)
    number_of_students = 0
    for student in course.students.all():
        number_of_students += 1
    def session_number_calculate(start_time, end_time, total_hours_of_class):
        first_time = str(start_time)
        last_time = str(end_time)
        total_hours = int(last_time[:2]) - int(first_time[:2])
        total_minute = int(last_time[3:5]) - int(first_time[3:5])
        if total_minute < 0:
            hour = total_hours - 1
            minute = 60 + total_minute
            total_time = f'{hour}:{minute}'
        elif total_minute > 0:
            hour = total_hours
            minute = total_minute
            total_time = f'{hour}:{minute}'
        else:
            total_time = f'{total_hours}:{total_minute}'

        number = float(total_time[:1]) + (int(total_time[2:4])/60)
        number_of_sessions = total_hours_of_class // number
        return int(number_of_sessions)
    session_number = session_number_calculate(course.start_time,course.end_time,course.total_time)
    completed_session = len(Sessions.objects.filter(course=course))
    remaining_sessions = session_number - completed_session
    sessions = Sessions.objects.filter(course=course)
    in_progress_homeworks = Homeworks.objects.filter(course=course, end=False)
    finished_homeworks = Homeworks.objects.filter(course=course, end=True)
    context = {
        'course': course,
        'number_of_students': number_of_students,
        'sessions': sessions,
        'session_number': session_number,
        'completed_session': completed_session,
        'remaining_sessions': remaining_sessions,
        'in_progress_homeworks': in_progress_homeworks ,
        'finished_homeworks': finished_homeworks,
    }
    return render(request, 'my_admin/course-detail.html', context)

