#   THIS IS FOR LOGIN AND REGISTRATION PAGES ONLY

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, get_user_model
from .forms import LoginForm, RegisterForm



@login_required(login_url='/login/')
def home_page(request):
    context = {
        "title":"How are you"
    }
    return render(request,"home_page.html",context)

def about_page(request):
    return render(request,"about_page.html")

def contacts_page(request):
    return render(request,"contacts_page.html")


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    print(request.user.is_authenticated())
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(request.user.is_authenticated())
            login(request, user)
            return redirect("/admin")
        else:
            print('Error')
    return render(request, "auth/login.html", context)


User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username,email,password)
        print(new_user)

    return render(request, "auth/register.html", context)