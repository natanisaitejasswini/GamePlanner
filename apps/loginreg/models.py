from __future__ import unicode_literals
from django.db import models
import re
from django.contrib import messages
import bcrypt
from datetime import datetime, date, timedelta, time
from time import strftime
# Create your models here.
class validationManager(models.Manager):
    def validateEmail(self, request, email):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')
        if not EMAIL_REGEX.match(email):
            messages.error(request, "Email is not valid")
            return False
        else:
            # check if email is already in database
            try:
                User.objects.get(email=email)
                messages.error(request, "Email is already in use")
                return False
            except User.DoesNotExist:
                pass
        return True

    def validateName(self, request, first_name, last_name):
        no_error = True
        if len(first_name) < 2 or any(char.isdigit() for char in first_name):
            messages.error(request, 'Frist name must be 2 characters and only letters')
            no_error = False
        if len(last_name) < 2 or any(char.isdigit() for char in last_name):
            messages.error(request, 'Last name must be 2 characters and only letters')
            no_error = False
        return no_error

    def validatePassword(self, request, password, confirm_password):
        no_error = True
        if len(password) < 8:
            messages.error(request, 'Password must be greater than 8 characters')
            no_error = False
        if not password == confirm_password:
            messages.error(request, 'Password confirmation must match password')
            no_error = False
        return no_error

    def validateLogin(self, request, email, password):
        try:
            user = User.objects.get(email=email)
            if bcrypt.hashpw(password.encode('utf-8'), user.password.encode('utf-8')) == user.password:
                messages.success(request, "Welcome!")
                return (True, user)
        except User.DoesNotExist:
            messages.error(request, "Invalid email")
            return False


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    emailManager = validationManager()
    objects = models.Manager()

#models.TextField()
#user_id = models.ForeignKey(User)
