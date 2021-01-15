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
        return redirect('all_books')
    else:
        return redirect('home')

def handle_login(request):
    if request.method == 'POST':
        user = Users.objects.filter(email = request.POST['email_login'])
        if user:
            loggedin_user = user[0]
            if bcrypt.checkpw(request.POST['password_login'].encode(), loggedin_user.password.encode()):
                request.session['userid'] = loggedin_user.id
                request.session['loggedin'] = True
                messages.success(request, f"User {loggedin_user.first_name} has logged in!")
                context = {
                    'loggedin_user': loggedin_user
                }
            return redirect('all_books')
    else:
        return redirect('home')

def logout(request):
    request.session.flush()
    request.session['loggedin'] = False
    return redirect('home')

def all_books(request):
    if request.session['loggedin'] == True:
        context = {
            'loggedinuser': Users.objects.get(id = request.session['userid']),
            'books': Books.objects.all(),
        }
        return render(request, 'html/all_books.html', context)
    else:
        messages.error(request, "Please log in before continuing!", extra_tags = 'danger')
        return redirect('home')

def add_book(request):
    if request.method == 'POST':
        adding_user = Users.objects.get(id = request.session['userid'])
        new_book = Books.objects.create(
            title = request.POST['newbooktitle'],
            description = request.POST['newbookdesc'],
            uploaded_by = adding_user,
        )
        adding_user.fav_books.add(new_book)
        return redirect('all_books')
    else:
        return redirect('all_books')

def edit_book(request):
    pass

def view_book(request):
    pass

def fav_book(request):
    pass