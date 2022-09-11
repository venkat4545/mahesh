from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from form import settings
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return render(request,"index.html")
def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        password=request.POST['password']
        conformpass=request.POST['conformpass']
          
        """""
        if User.objects.filter(username=username):
            messages.error(request,"username already exists")
            return redirect(home)
        if User.objects.filter(email=email):
            messages.error(request,"email already exists")
            return redirect(home)
        if password!=conformpass:
            messages.error(request,"password should be same")
        """

        myuser=User.objects.create_user(username,email,password)
        myuser.firstname=firstname
        myuser.lastname=lastname
        myuser.save()
        messages.success(request,"signup success")
        subject="welcome to colortokens"
        message="hello"+myuser.firstname+"this is a conformation email for conforming your email address"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        return redirect(signin)
    return render(request,'signup.html')
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            firstname=user.get_username
            #subject="welcome to colortokens"
            #message="hello"+user.get_username+"this is a conformation email for conforming your email address"
            #from_email=settings.EMAIL_HOST_USER
            #to_list=[user.get_email_field_name]
            #send_mail(subject,message,from_email,to_list,fail_silently=True)
            return render(request,'index.html',{'firstname':firstname})
        else:
            messages.error(request,"wrong")

    return render(request,'signin.html')
def signout(request):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect(home)