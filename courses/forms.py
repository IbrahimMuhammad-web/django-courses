from django import forms
from django.contrib.auth.models import User
from .models import Course, Lecture

from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }),
        label='Username'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        label='Password'
    )

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LecturerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        # exclude slug & timestamps; lecturer is set in view
        exclude = ['course_slug', 'lecturer', 'course_created_at', 'course_updated_at']

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        # course & slug & timestamps set in view
        exclude = ['course', 'lecture_slug', 'lecture_created_at', 'lecture_updated_at']
