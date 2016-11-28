from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import User, validationManager
import bcrypt
import datetime
from django.core.urlresolvers import reverse
# from datetime import datetime


# password = b"super secret password"
#CONTROLLER
#Create your views here.
def index(request):
    return render(request, 'loginreg/index.html')

def register(request):
    error = False
    if not validationManager().validateEmail(request, request.POST['email']):
        error = True

    if not validationManager().validateName(request, request.POST['first_name'], request.POST['last_name']):
        error = True

    if not validationManager().validatePassword(request, request.POST['password'], request.POST['password_confirmation']):
        error = True

    if not error:
        hashed = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed)
        messages.success(request, 'You have successfully been registered!')
        request.session['user']=user.id
        return redirect(reverse('landing'))
    else:
        return redirect('/')

def login(request):
    user = validationManager().validateLogin(request, request.POST['email'], request.POST['password'])
    if user:
        request.session['user']=user[1].id
        return redirect(reverse('landing'))
    else:
        return redirect('/')
def logout(request):
    request.session.clear()
    return redirect('/')