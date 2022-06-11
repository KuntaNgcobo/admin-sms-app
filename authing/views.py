from cgitb import html
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

def login_user(request):
    print("IAM:",request.user,request.user.is_authenticated, request.user.is_anonymous)
    if request.method == "POST" and request.user != "AnonymousUser":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if request.user.is_authenticated:
            login(request, user)
            return HttpResponseRedirect(reverse('sms_app:index'))
        else:
            context = {
                "error": "There Was An Error Logging In, Try Again...",
                "html": views.LoginView.form_class(),
            }
            return render(request, 'login.html', context)

    else:
        context = {
                "html": views.LoginView.form_class(),
            }
        return render(request, 'login.html', context)

def logout_user(request):
    print("IAMOUT:",request.user,request.user.is_authenticated)
    logout(request)
    return HttpResponseRedirect(reverse('authing:login_user'))