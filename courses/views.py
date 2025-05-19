from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Course, Lecture, Enroll
from django.contrib import messages
from django.contrib.auth.decorators import login_required # for Access Control
from django.contrib.auth.decorators import user_passes_test
from .forms import CourseForm, LectureForm, StudentSignUpForm, LecturerSignUpForm, LoginForm
from django.utils.text import slugify
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Student')
            user.groups.add(group)
            messages.success(request, 'Student account created successfully!')
            return redirect('account_login')
    else:
        form = StudentSignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def lecturer_signup(request):
    if request.method == 'POST':
        form = LecturerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Lecturer')
            user.groups.add(group)
            messages.success(request, 'Lecturer account created successfully!')
            return redirect('account_login')
    else:
        form = LecturerSignUpForm()
    return render(request, 'account/lecturer_signup.html', {'form': form})


def user_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                
                # ✅ Check user group and redirect accordingly
                if user.groups.filter(name="Lecturer").exists():
                    return redirect('lecturer-dashboard')  # URL name for lecturer dashboard
                elif user.groups.filter(name="Student").exists():
                    return redirect('home')  # URL name for student dashboard
                else:
                    messages.warning(request, 'Your account is not assigned to a user group.')
                    return redirect('home')  # fallback

            else:
                messages.error(request, 'Invalid credentials')
    
    return render(request, 'account/login.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('account_login')


# def student_signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             try:
#                 group = Group.objects.get(name='Student')
#                 user.groups.add(group)
#                 messages.success(request, "Signed up successfully as student.")
#             except Group.DoesNotExist:
#                 messages.error(request, "Student group does not exist!")
#             login(request, user)
#             return redirect('home') 
#     else:
#         form = UserCreationForm()
#     return render(request, 'account/signup.html', {'form': form, 'user_type': 'Student'})

# def lecturer_signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             try:
#                 group = Group.objects.get(name='Lecturer')
#                 user.groups.add(group)
#                 messages.success(request, "Signed up successfully as lecturer.")
#             except Group.DoesNotExist:
#                 messages.error(request, "Lecturer group does not exist!")
#             login(request, user)
#             return redirect('lecturer-dashboard')
#     else:
#         form = UserCreationForm()
#     return render(request, 'account/signup.html', {'form': form, 'user_type': 'Lecturer'})



def index(request):
    courses = Course.objects.filter(course_is_active='Yes', course_is_featured="Yes")
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


def topic_courses(request, topic_slug):
    topic = Topic.objects.get(topic_slug=topic_slug)
    courses = Course.objects.filter(course_is_active='Yes', course_topic=topic)
    context = {
        'courses': courses,
        'topic': topic,
    }
    return render(request, 'courses/topic_courses.html', context)


def search_courses(request):
    if request.method == "GET":
        keyword = request.GET.get('q')
        courses = Course.objects.filter(course_is_active='Yes')
        searched_courses = courses.filter(course_title__icontains=keyword) | courses.filter(course_description__icontains=keyword)
        
        context = {
            'courses': searched_courses,
            'keyword': keyword,
        }
        return render(request, 'courses/search_courses.html', context)


def course_detail(request, course_slug):
    try:
        course = Course.objects.get(course_slug=course_slug)
        lectures = Lecture.objects.filter(course=course.id)

        # Check
        if request.user.is_authenticated:
            enrolled = Enroll.objects.filter(course=course, user=request.user)
        else:
            enrolled = None
        

        context = {
            'course': course,
            'lectures': lectures,
            'enrolled': enrolled,
        }
        return render(request, 'courses/course_detail.html', context)

    except:
        messages.error(request, "Course Does not Exist.")
        return redirect(index)


@login_required(login_url='account_login')
def lecture(request, course_slug):
    try:
        course = Course.objects.get(course_slug=course_slug)
        lectures = Lecture.objects.filter(course=course.id)
        first_lecture = Lecture.objects.filter(course=course.id)[:1]
        #Check User Enrolled
        enrolled = Enroll.objects.filter(course=course, user=request.user)

        context = {
            'course': course,
            'lectures': lectures,
            'first_lecture': first_lecture,
            'enrolled': enrolled,
        }
        # return render(request, 'courses/lecture.html', context)
        #Check User Enrolled
        if enrolled:
            return render(request, 'courses/lecture.html', context)
        else:
            #User Logged In but Not Enrolled
            messages.error(request, "Enroll Now to access this course.")
            return render(request, 'courses/course_detail.html', context)

    except:
        messages.error(request, "Course Does not Exist.")
        return redirect(index)


@login_required(login_url='account_login')
def lecture_selected(request, course_slug, lecture_slug):
    try:
        course = Course.objects.get(course_slug=course_slug)
        lectures = Lecture.objects.filter(course=course.id)
        lecture_selected = Lecture.objects.get(lecture_slug=lecture_slug)
        #Check User Enrolled
        enrolled = Enroll.objects.filter(course=course, user=request.user)

        context = {
            'course': course,
            'lectures': lectures,
            'lecture_selected': lecture_selected,
            'enrolled': enrolled,
        }
        # return render(request, 'courses/lecture_selected.html', context)
        #Check User Enrolled
        if enrolled:
            return render(request, 'courses/lecture_selected.html', context)
        else:
            #User Logged In but Not Enrolled
            messages.error(request, "Enroll Now to access this course.")
            return render(request, 'courses/course_detail.html', context)

    except:
        messages.error(request, "Course Does not Exist.")
        return redirect(index)


@login_required(login_url='account_login')
def enroll(request, course_id):
    user = request.user
    course = Course.objects.get(id=course_id)

    try:
        Enroll.objects.create(user=user, course=course)
        messages.success(request, "Successfully enrolled to the Course.")
        return redirect(index)

    except:
        messages.error(request, "Couldn't Enroll to the course. Please try again later.")
        return redirect(index)


@login_required(login_url='account_login')
def enrolled_courses(request):

    try:
        courses = Enroll.objects.filter(user=request.user)
        context = {
            'courses': courses,
        }
        return render(request, 'courses/enrolled_courses.html', context)

    except:
        messages.error(request, "Couldn't Enroll to the course. Please try again later.")
        return redirect(index)
    

def is_lecturer(user):
    return user.is_authenticated and user.groups.filter(name='Lecturer').exists()

@login_required(login_url='account_login')
@user_passes_test(is_lecturer)
def lecturer_dashboard(request):
    courses = Course.objects.filter(lecturer=request.user)
    return render(request, 'courses/lecturer/dashboard.html', {'courses': courses})

@login_required
@user_passes_test(is_lecturer)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.lecturer = request.user
            course.course_slug = slugify(course.course_title)
            course.save()
            form.save_m2m()
            messages.success(request, 'Course created.')
            return redirect('lecturer-dashboard')
    else:
        form = CourseForm()
    return render(request, 'courses/lecturer/add_course.html', {'form': form})

@login_required
@user_passes_test(is_lecturer)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, lecturer=request.user)
    form = CourseForm(request.POST or None, request.FILES or None, instance=course)
    if request.method == 'POST' and form.is_valid():
        c = form.save(commit=False)
        c.course_slug = slugify(c.course_title)
        c.save()
        form.save_m2m()
        messages.success(request, 'Course updated.')
        return redirect('lecturer-dashboard')
    return render(request, 'courses/lecturer/edit_course.html', {'form': form})

@login_required
@user_passes_test(is_lecturer)
def add_lecture(request, course_id):
    course = get_object_or_404(Course, id=course_id, lecturer=request.user)
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES)
        if form.is_valid():
            lec = form.save(commit=False)
            lec.course = course
            lec.lecture_slug = slugify(lec.lecture_title)
            lec.save()
            messages.success(request, 'Lecture added.')
            return redirect('lecturer-dashboard')
    else:
        form = LectureForm()
    return render(request, 'courses/lecturer/add_lecture.html', {'form': form, 'course': course})

@login_required
@user_passes_test(is_lecturer)
def edit_lecture(request, lecture_id):
    lec = get_object_or_404(Lecture, id=lecture_id, course__lecturer=request.user)
    form = LectureForm(request.POST or None, request.FILES or None, instance=lec)
    if request.method == 'POST' and form.is_valid():
        l = form.save(commit=False)
        l.lecture_slug = slugify(l.lecture_title)
        l.save()
        messages.success(request, 'Lecture updated.')
        return redirect('lecturer-dashboard')
    return render(request, 'courses/lecturer/edit_lecture.html', {'form': form})