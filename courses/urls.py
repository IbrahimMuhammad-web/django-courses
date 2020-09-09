from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('courses/', views.courses, name="courses"),
    path('course/<slug:course_slug>/', views.course_detail, name="course-detail"),
    path('course/<slug:course_slug>/lecture/', views.lecture, name="lecture"),
    path('course/<slug:course_slug>/lecture/<slug:lecture_slug>/', views.lecture_selected, name="lecture-selected"),
]
