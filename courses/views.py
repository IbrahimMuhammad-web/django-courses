from django.shortcuts import render, redirect
from .models import Course, Lecture
from django.contrib import messages

# Create your views here.

def index(request):
    courses = Course.objects.filter(course_is_active='Yes')
    context = {
        'courses': courses,
    }
    return render(request, 'courses/index.html', context)


def courses(request):
    courses = Course.objects.filter(course_is_active='Yes')
    context = {
        'courses': courses,
    }
    return render(request, 'courses/courses.html', context)


def course_detail(request, course_slug):
    try:
        course = Course.objects.get(course_slug=course_slug)
        lectures = Lecture.objects.filter(course=course.id)
        context = {
            'course': course,
            'lectures': lectures,
        }
        return render(request, 'courses/course_detail.html', context)

    except Course.DoesNotExist:
        messages.error(request, "Course Does not Exist.")
        return redirect(index)


def lecture(request):
    return render(request, 'courses/lecture.html')
        

