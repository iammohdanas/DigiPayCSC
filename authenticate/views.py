import datetime
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
import json
from .forms import SignUpForm, EditProfileForm, ChangePasswordForm
from .components import generate_msg_id, generate_txn_id, bank_list
from authenticate.txncomponents.withdrawformreq import withdraw_apireq
import xmltodict
from django.urls import reverse

def home(request):
    return render(request, 'authenticate/home.html')

def withdrawform(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    
    context = {'bank_data':bank_list()}
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

def process_withdrawform(request):
    configinput = {}
    configinput2 ={}
    if request.method == 'POST':
        configinput["customer_mobile_number"] = request.POST.get('customermobilenumber')
        configinput["aadhar_number"] = request.POST.get('aadharNumber')
        configinput["txn_amount"] = request.POST.get('amount')
        configinput["bank_shortcode"] = request.POST.get('bankOption')
        configinput["transaction_type"] = request.POST.get('transactionType', None)
        txn_id = generate_txn_id(request)
    
    txn_id = generate_txn_id(request)   
    msg_id = generate_msg_id(request)
    configinput2["txnId"] = txn_id
    configinput2["msgId"] = msg_id
    configinput2["callbackEndpointIP"] = "127.0.0.1"

    api_req_data_context = withdraw_apireq(configinput, configinput2)
    context = {
        **api_req_data_context,
    }
    xml_data = xmltodict.unparse({"xml": context}, full_document=False)
    xml_data = xml_data.replace('<ns2ReqPay', '<ns2:ReqPay').replace('</ns2ReqPay>', '</ns2:ReqPay>')
    xml_data = xml_data.replace('xmlnsns2="http://npci.org/upi/schema/"', 'xmlns:ns2="http://npci.org/upi/schema/"')
    xml_data = xml_data.replace('xmlnsns3="http://npci.org/cm/schema/"','xmlns:ns3="http://npci.org/cm/schema/"')
    xml_response = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_data
    return HttpResponse(xml_response, content_type="application/xml")
