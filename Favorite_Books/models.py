from django.db import models
import re

from django.db.models.deletion import CASCADE

class ValidationTest(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        if len(postData['firstname']) < 2:
            errors['firstname'] = "First name must be more than two characters."
        if len(postData['lastname']) < 2:
            errors['lastname'] = "Last name must be more than two characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        emaildupcheck = Users.objects.filter(email=postData['email'])
        if emaildupcheck == postData['email']:
            errors['email'] = "That email address already exists. Did you forget your password?"
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters."
        if not postData['confirm-pw'] == postData['password']:
            errors['confirm-pw'] = "Password mismatch. Maybe a typo? Please try again!"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField()
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # fav_books = Books the user has favorited.
    # books_added = Books the user has uploaded/added.

    objects = ValidationTest()

class Books(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    uploaded_by = models.ForeignKey(
        Users,
        related_name = "books_added",
        on_delete = CASCADE
    )
    users_who_fav = models.ManyToManyField(
        Users,
        related_name = "fav_books",
    )