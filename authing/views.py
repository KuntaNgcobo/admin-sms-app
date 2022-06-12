from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import views
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)
            return HttpResponseRedirect(reverse('sms_app:index'))
        else:
            context = {
                "error": "There Was An Error Logging In, Try Again...",
                "html": views.LoginView.form_class(),
            }
            return render(request, 'login.html', context)

    else:
        logout_user(request)
        context = {
                "html": views.LoginView.form_class(),
            }
        return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('authing:login_user'))