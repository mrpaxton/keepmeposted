from django.shortcuts import render
from django.core.urlresolvers import reverse

# Create your views here.


from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserSignupForm


def login_view(request):

    next = request.GET.get("next")
    title = "Login"
    credential = "Try username: Foo, password: Burrito, or sign up a new user"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)

        if next:
            return redirect(next)

        #todo: try to use reverse()
        return redirect(reverse("news:tech-article-list"))


    return render(request, "form.html", {"form": form, "title": title, "credential": credential})


def logout_view(request):
    logout(request)
    return redirect(reverse("news:general-article-list"))


def signup_view(request):
    next = request.GET.get("next")
    title = "Sign Up"
    form = UserSignupForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        print("user: ", user.username)
        print("password: ", password)
        print("new_user: ", new_user)
        if new_user is not None:
            login(request, new_user)
            if next:
                return redirect(next)
            return redirect(reverse("news:tech-article-list"))

    context = {
        "form": form,
        "title": title
    }

    return render(request, "form.html", context)
