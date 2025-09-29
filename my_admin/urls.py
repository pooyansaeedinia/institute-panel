from django.urls import path
from .views import course_list, course_detail

app_name = 'my_admin'

urlpatterns = [
    path('', course_list, name='home'),
]
