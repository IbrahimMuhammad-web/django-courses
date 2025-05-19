from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    
    # Authentication URLs
    path('login/', views.user_login, name='account_login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/student/', views.student_signup, name='student-signup'),
    path('signup/lecturer/', views.lecturer_signup, name='lecturer-signup'),
    
    
    path('courses/', views.courses, name="courses"),
    path('courses/search/', views.search_courses, name="search-courses"),
    path('courses/enrolled-courses/', views.enrolled_courses, name="enrolled-courses"),

    path('courses/<slug:topic_slug>/', views.topic_courses, name="topic-courses"),
    path('course/<slug:course_slug>/', views.course_detail, name="course-detail"),
    path('course/<slug:course_slug>/lecture/', views.lecture, name="lecture"),
    path('course/<slug:course_slug>/lecture/<slug:lecture_slug>/', views.lecture_selected, name="lecture-selected"),

    path('course/enroll/<int:course_id>/', views.enroll, name="enroll"),
    
    
    # Lecturer URLs
    path('lecturer/dashboard/',  views.lecturer_dashboard, name='lecturer-dashboard'),
    path('lecturer/course/add/', views.add_course,         name='add-course'),
    path('lecturer/course/<int:course_id>/edit/', views.edit_course, name='edit-course'),
    path('lecturer/course/<int:course_id>/add-lecture/', views.add_lecture, name='add-lecture'),
    path('lecturer/lecture/<int:lecture_id>/edit/', views.edit_lecture, name='edit-lecture'),

]
