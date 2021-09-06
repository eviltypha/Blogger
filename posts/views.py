from .forms import ImageForm
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Post

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('content')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/')

    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        captcha = request.POST['captcha']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username taken')
                return redirect('register')
            elif any(i.isdigit() for i in password1) == False:
                messages.error(request, 'Password must contain numbers')
                return redirect('register')
            elif all(i.isdigit() for i in password1) == True:
                messages.error(request, 'Password must contain alphabets')
                return redirect('register')
            elif len(password1) < 8:
                messages.error(
                    request, 'Password must be atleast 8 characters long')
                return redirect('register')
            elif captcha != '5':
                messages.error(request, 'Invalid captcha')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, password=password1)
                user.save()

        else:
            messages.error(request, 'Passwords not matching')
            return redirect('register')

        return redirect('/')

    else:
        return render(request, 'register.html')


def content(request):
    userid = request.user.id
    posts = Post.objects.filter(author_id=userid)
    return render(request, 'content.html', {'posts': posts})


def create(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author_id = request.user.id
            obj.save()

    return redirect('content')


def search(request):
    username = request.GET['searchbox']
    userid = User.objects.filter(username=username)[0]
    posts = Post.objects.filter(author_id=userid, public=1)
    return render(request, 'search.html', {'posts': posts, 'userid': username})


def logout(request):
    auth.logout(request)
    return redirect('/')
