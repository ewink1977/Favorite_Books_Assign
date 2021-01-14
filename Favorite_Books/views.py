from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Users, Books
import bcrypt

def home(request):
    return render(request, 'html/login.html')

def handle_registration(request):
    if request.method == 'POST':
        errors = Users.objects.basic_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items:
                messages.error(request, value, extra_tags='danger')
            return redirect('home')
        prehash = request.POST['password']
        hash_n_salt = bcrypt.hashpw(prehash.encode(), bcrypt.gensalt()).decode()
        newuser = Users.objects.create(
            first_name = request.POST['firstname'],
            last_name = request.POST['lastname'],
            email = request.POST['email'],
            password = hash_n_salt
        )
        print(f"{newuser.id}, {newuser.first_name}, {newuser.password}")
        request.session['userid'] = newuser.id
        messages.success(request, f"User { request.POST['email'] } has been created successfully!")
        # CHANGE THIS TO BOOK PAGE ONCE THAT IS MADE.
        return redirect('home')
    else:
        return redirect('home')

def handle_login(request):
    if request.method == 'POST':
        user = Users.objects.filter(email = request.POST['email_login'])
        if user:
            loggedin_user = user[0]
            print("USER LOCATED")
            if bcrypt.checkpw(request.POST['password_login'].encode(), loggedin_user.password.encode()):
                print("PASSWORD VALIDATED")
                request.session['userid'] = loggedin_user.id
                request.session['loggedin'] = True
                print(request.session['userid'])
                messages.success(request, f"User {loggedin_user.first_name} has logged in!")
                context = {
                    'loggedin_user': loggedin_user
                }
            # CHANGE THIS TO BOOK PAGE ONCE THAT IS MADE.
            return redirect('home')
    else:
        return redirect('home')