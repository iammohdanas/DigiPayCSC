import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from flask import json
from .forms import SignUpForm, EditProfileForm, ChangePasswordForm
from django.contrib.auth.models import User
from .components import generate_txn_id, dict_to_xml, bank_list
import pandas as pd
from authenticate.txncomponents.withdrawformreq import withdraw_apireq
import xml.etree.ElementTree as ET


def home(request):
    return render(request, 'authenticate/home.html')

def withdrawform(request):
    bank_list_context = bank_list()
    context = {
        **bank_list_context,
    }
    return render(request, 'transaction/withdrawform.html',context)

def depositform(request):
    bank_list_context = bank_list()
    context = {
        **bank_list_context,
    }
    return render(request, 'transaction/depositform.html',context)

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


# def process_withdrawform(request):
#     if request.method == 'GET':
#         customer_mobile_number = request.GET.get('customermobilenumber')
#         aadhar_number = request.GET.get('aadharNumber')
#         amount = request.GET.get('amount')
#         bank_option = request.GET.get('bankOption')
#         order_id = generate_order_id()
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         form_data = {
#             'order_id': order_id,
#             'mid':'mid',
#             'timeStamp': timestamp,
#             'customer_mobile_number': customer_mobile_number,
#             'aadhar_number': aadhar_number,
#             'amount': amount,
#             'bank_option': bank_option,
#         }
#         # json_data = json.dumps(form_data)
#         # return JsonResponse(form_data)
#         xml_data = dict_to_xml(form_data)
#         # print("Form Data (XML):", xml_data.decode('utf-8'))
#         return HttpResponse(xml_data, content_type="application/xml")
#     else:
#         return HttpResponse("Invalid request method.")

# def process_withdraw_elements(request):
#     if request.method == 'GET':
#         customer_mobile_number = request.GET.get('customermobilenumber')
#         aadhar_number = request.GET.get('aadharNumber')
#         amount = request.GET.get('amount')
#         bank_option = request.GET.get('bankOption')
#         order_id = generate_order_id()
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         form_data = {
#             'order_id': order_id,
#             'mid':'mid',
#             'timeStamp': timestamp,
#             'customer_mobile_number': customer_mobile_number,
#             'aadhar_number': aadhar_number,
#             'amount': amount,
#             'bank_option': bank_option,
#         }
#     return HttpResponse("Invalid request method.")

def process_withdrawform(request):
    api_req_data_context = withdraw_apireq(request)
    context = {
        **api_req_data_context,
    }
    def dict_to_xml_recursive(tag, d):
        elem = ET.Element(tag)
        for key, val in d.items():
            if isinstance(val, dict):
                elem.append(dict_to_xml_recursive(key, val))
            elif isinstance(val, list):
                for item in val:
                    elem.append(dict_to_xml_recursive(key, item))
            else:
                child = ET.Element(key)
                child.text = str(val)
                elem.append(child)
        return elem

    root = dict_to_xml_recursive("Root", context)
    xml_string = ET.tostring(root, encoding='utf8', method='xml')
    return HttpResponse(xml_string, content_type='application/xml')
