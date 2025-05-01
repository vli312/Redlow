from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def profile(request,username):
    user = get_object_or_404(User,username=username)
    user_id = int(user.id)
    return render(request,
                  'users/user/profile.html',
                  {'user':user}
                            )

def editprofile(request,username):
    user = get_object_or_404(User,username=username)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')
        user.detail.fname = request.POST.get('fname')
        user.detail.lname = request.POST.get('lname')
        user.detail.role = request.POST.get('role')
        user.save()
        userFK = User.objects.get(username=request.session.get('username'))
        messages.add_message(request, messages.SUCCESS, 'User created successfully with the username: %s' % username)
        return redirect('users:profile',username=user.username)
    return render(request,
                  'users/user/editprofile.html',
                  {'user':user})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        favproteinsource = request.POST.get('proteinSource')
        user = User.objects.create_user(username, email, password)
        user.detail.fname = fname
        user.detail.lname = lname
        user.detail.favproteinsource = favproteinsource
        user.save()
        request.session['username'] = user.username
        request.session['role'] = user.detail.role
        userFK = User.objects.get(username=request.session.get('username'))
        messages.add_message(request, messages.SUCCESS, 'User created successfully with the username: %s' % username)
        return redirect('users:profile',username=user.username)
    return render(request,'users/user/register.html')

def login_user(request):
    username = request.POST.get("username")
    pw = request.POST.get("pw")

    user = authenticate(username=username, password=pw)
    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.detail.role
        userFK = User.objects.get(username=request.session.get('username'))
        messages.add_message(request, messages.SUCCESS, 'You have logged in successfully!')
    else:
        messages.add_message(request, messages.ERROR, 'Invalid username or password')
    return redirect('page:homeview')

def logout_user(request):
    userFK = User.objects.get(username=request.session.get('username'))
    del request.session['username']
    del request.session['role']
    return redirect('page:homeview')