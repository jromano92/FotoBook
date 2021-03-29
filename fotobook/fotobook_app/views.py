from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import *
import bcrypt 

# Create your views here.

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    user = None if 'user_id' not in request.session else User.objects.get(id=request.session['user_id'])
    if not user: 
        return redirect('/')
    else:
        context= {
            'user': User.objects.get(id=request.session['user_id']),
            'all_images': Image.objects.all(),
            'images': Image.objects.order_by('-created_at')
        }
    return render(request, 'dashboard.html', context)

def delete(request, image_id):
    delete = Image.objects.get(id=image_id)
    delete.delete()

    return redirect('dashboard')

def upload(request): 
    pic = request.FILES['picture']
    Image.objects.create(name=pic.name, image=pic)

    return redirect('dashboard')


def login(request):
    errors = User.objects.login_validate(request.POST)

    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        return redirect('dashboard')

def register(request):
    errors = User.objects.register(request.POST)

    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')

    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            about_me = request.POST['about_me'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['wecome'] = user.first_name
        return redirect('dashboard')

def create(request):
    return render(request, 'register.html')

def edit(request, user_id):
    user1 = User.objects.get(id=user_id)
    context = {
        'user': user1
    }
    return render(request, 'edit.html', context)

def update(request, user_id):
    errors = User.objects.update_validate(request.POST)

    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect(f'/myaccount/{user_id}/edit')
    
    else:
        user1 = User.objects.get(id=user_id)
        user1.first_name = request.POST['first_name']
        user1.last_name = request.POST['last_name']
        user1.email = request.POST['email']
        user1.save()

    return redirect('dashboard')

def spotlight(request, image_id):
    my_image = Image.objects.get(id=image_id)
    context = {
        'image': my_image,
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'spotlight.html', context)