from django import http
from django.db.models.query import RawQuerySet
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from django.shortcuts import render,redirect
from accounts.forms import SignupForm
from .models import User
from sesame.utils import get_token,get_user
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def SignupView(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        try:
            user = User.objects.create_user(email=email,username=username)
            user.save()
            return redirect('login')
        except Exception as e:
            return HttpResponse(f"The error is {e}")
    form = SignupForm()
    return render(request,'accounts/signup.html',{'form':form})

            
def LoginView(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            token_query_string = get_token(User.objects.get(email=email))
            link = settings.HARDCODED_LINK + token_query_string + "/"
            send_mail("Passwordless Login",f"Click this link: {link}",settings.EMAIL_HOST_USER,[email])
            return HttpResponse("Email sent successfully")
        except Exception as e:
            return HttpResponse(f"The user is not created yet")
    return render(request,'accounts/login.html')

def HomeView(request,token):
    token = token
    print(token)
    print(get_user(request_or_sesame=token))
    try:
        if get_user(request_or_sesame=token) is not None:
            email = get_user(request_or_sesame=token)
            user = User.objects.get(email=email)
            return render(request,'accounts/home.html',{'user':user})
        else:
            return HttpResponse("Invalid token or token is expired")
    except Exception as e:
        return HttpResponse(f"error is {e}")
