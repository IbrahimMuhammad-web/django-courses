from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'account/profile.html')
    else:
        messages.error(request, "Please login to access your profile.")
        return redirect('account_login')