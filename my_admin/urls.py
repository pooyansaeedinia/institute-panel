from django.urls import path
from .views import course_list, course_detail, teachers_list

app_name = 'my_admin'

urlpatterns = [
    path('', course_list, name='course_list'),
    path('course/<int:code>/', course_detail, name='course_detail'),
    path('teachers/', teachers_list, name='teachers'),
]
