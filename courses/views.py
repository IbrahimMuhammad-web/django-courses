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

    except:
        messages.error(request, "Course Does not Exist.")
        return redirect(index)


def lecture(request, course_slug):
    try:
        course = Course.objects.get(course_slug=course_slug)
        lectures = Lecture.objects.filter(course=course.id)
        first_lecture = Lecture.objects.filter(course=course.id)[:1]
        context = {
            'course': course,
            'lectures': lectures,
            'first_lecture': first_lecture,
        }
        return render(request, 'courses/lecture.html', context)

    except:
        messages.error(request, "Course Does not Exist.")
        return redirect(index)


def lecture_selected(request, course_slug, lecture_slug):
    try:
        course = Course.objects.get(course_slug=course_slug)
        lectures = Lecture.objects.filter(course=course.id)
        lecture_selected = Lecture.objects.get(lecture_slug=lecture_slug)
        context = {
            'course': course,
            'lectures': lectures,
            'lecture_selected': lecture_selected,
        }
        return render(request, 'courses/lecture_selected.html', context)

    except:
        messages.error(request, "Course Does not Exist.")
        return redirect(index)

        

