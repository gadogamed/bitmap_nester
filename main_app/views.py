from django.shortcuts import render, redirect
from .models import nesters
from django.contrib import messages
from django.http import JsonResponse
from .models import new_in
from .models import history_m

import os

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        
        # Check if the email already exists
        if nesters.objects.filter(mail=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('/')

        # Create a new user object
        new_user = nesters(name=name, mail=email,password=password)
        new_user.save()
        messages.success(request, 'User registered successfully.')
        return redirect('/')

    return render(request, "register.html", {})

def sign(request):
    if request.method == 'POST':
        email = request.POST.get('mail')
        password = request.POST.get('pass')
        user = nesters.objects.get(mail=email)
        if user.password == password:
            messages.success(request, f'Login successful. Email: {email}, Password: {password}')
            return redirect('home.html/')
        else:
            messages.error(request, f'Login failed. Email: {email}, Password: {password}')

    return render(request, 'sign.html')

def home(request):
    data=new_in.objects.all()
    context={"items":data}
    return render(request, 'home.html',context)

def result(request):
    return render(request, 'result.html')

def history(request):
    data=history_m.objects.all()
    context={"items":data}
    return render(request, 'history.html',context)

def delete_item(request,item_id):
    item=new_in.objects.get(pk=item_id)
    if os.path.exists(item.input_image.path):os.remove(item.input_image.path)
    item.delete()
    return redirect('/home.html')

from .img_proc import *
import cv2
from django.conf import settings

def upload_image_view(request):
    if request.method == 'POST' and request.FILES.get('file-upload'):
        uploaded_file = request.FILES['file-upload']
        # Process the image with OpenCV
        processed_images = split_by_cont(uploaded_file)
        
        # Get the ID of the last object created in the model
        last_input_instance_id = new_in.objects.latest('id').id if new_in.objects.exists() else 0

        # Save each processed image
        for image in processed_images:
            last_input_instance_id += 1
            processed_image_name = f'out_img_{last_input_instance_id}.jpg'
            processed_image_path = os.path.join(settings.MEDIA_ROOT, processed_image_name)
            cv2.imwrite(processed_image_path, image)
            input_instance = new_in.objects.create(input_image=processed_image_name)

        return redirect('/home.html')
    else:
        return JsonResponse({'error': 'No image file provided'})
    