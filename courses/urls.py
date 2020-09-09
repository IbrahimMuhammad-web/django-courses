from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('courses/', views.courses, name="courses"),
    path('<slug:course_slug>/', views.course_detail, name="course-detail"),
]
