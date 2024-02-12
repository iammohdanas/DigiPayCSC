import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from flask import json
from .forms import SignUpForm, EditProfileForm, ChangePasswordForm
from django.contrib.auth.models import User
from .components import generate_order_id, dict_to_xml

def home(request):
    return render(request, 'authenticate/home.html')

def withdrawform(request):
    return render(request, 'transaction/withdrawform.html')

def depositform(request):
    return render(request, 'transaction/depositform.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully')
            return redirect('home')
        else:
            messages.warning(request, "Username or Password is incorrect !!")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            form = SignUpForm(request.POST)
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'authenticate/register.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'authenticate/edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Changed Successfully")
            return redirect('home')
    else:
        form = ChangePasswordForm(user=request.user)
        print(form)
    context = {
        'form': form,
    }
    return render(request, 'authenticate/change_password.html', context)


def process_withdrawform(request):
    if request.method == 'GET':
        customer_mobile_number = request.GET.get('customermobilenumber')
        aadhar_number = request.GET.get('aadharNumber')
        amount = request.GET.get('amount')
        bank_option = request.GET.get('bankOption')
        checkbox_checked = request.GET.get('checkboxChecked')
        order_id = generate_order_id()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print("Customer Mobile Number:", customer_mobile_number)
        # print("Aadhar Number:", aadhar_number)
        # print("Amount:", amount)
        # print("Bank Option:", bank_option)
        
        form_data = {
            'order_id': order_id,
            'mid':'mid',
            'timeStamp': timestamp,
            'customer_mobile_number': customer_mobile_number,
            'aadhar_number': aadhar_number,
            'amount': amount,
            'bank_option': bank_option,
        }
        # json_data = json.dumps(form_data)
        # print("Form Data:", json_data)
        # return JsonResponse(form_data)

        xml_data = dict_to_xml(form_data)
        # print("Form Data (XML):", xml_data.decode('utf-8'))
        return HttpResponse(xml_data, content_type="application/xml")
    else:
        return HttpResponse("Invalid request method.")