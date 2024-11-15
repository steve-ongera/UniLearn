from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .import views
from django.contrib.auth import authenticate, login, logout
from app.EmailBackEnd import EmailBackEnd

# Register new user
def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # checking email
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists!')
            return redirect('register')

        # Checking username
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists!')
            return redirect('register')

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request, 'registration/register.html')


# Login existing user
def LOGIN_PAGE(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Use custom backend for authentication
        user = EmailBackEnd.authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Email/Password!')
            return redirect('login')

    return render(request, 'registration/login.html')


# User profile page
def PROFILE(request):
    return render(request, 'registration/profile.html')


# Update user profile
def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        # Update password if provided
        if password is not None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile successfully updated.')
        return redirect('profile')

    return render(request, 'registration/profile_update.html')


# Logout user
def LOGOUT(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')
