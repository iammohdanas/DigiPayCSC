import json
import random
import string
import datetime
from django.http import JsonResponse
import xml.etree.ElementTree as ET

def generate_txn_id(request):
    if request.method == 'POST':
        bank_shortcode = request.POST.get('bankOption')
    txn_id = bank_shortcode[:3]+ str(random.randint(10**31, 10**32 - 1))
    return txn_id

def generate_msg_id(request):
    if request.method == "POST":
        bank_shortcode = request.POST.get('bankOption')
    alphanumeric_chars = string.ascii_letters + string.digits
    msg_id = bank_shortcode[:3] + ''.join(random.choices(alphanumeric_chars, k=29))
    return msg_id

def dict_to_xml(dict_data):
    root = ET.Element("FormData")
    for key, value in dict_data.items():
        element = ET.SubElement(root, key)
        element.text = str(value)
    return ET.tostring(root, encoding='utf-8')

def bank_iin_list():
    file_path = "authenticate/data/Bank_IIN_list.json"
    bank_data = None
    with open(file_path, 'r') as file:
        bank_data = json.load(file)
    return bank_data

def bank_list():
    file_path = "authenticate/data/Bank_List.json"
    bank_data = None
    with open(file_path, 'r') as file:
        bank_data = json.load(file)
    # bank_id = [bank['BankID'] for bank in bank_data]
    # bank_names = [bank['BANK_NAME'] for bank in bank_data]
    # bank_shortcode = [bank['ShortCode'] for bank in bank_data]
    # bank_imps_status = [bank['IMPS_Status'] for bank in bank_data]
    # bank_neft_status = [bank['NEFT_Status'] for bank in bank_data]
    # bank_isverficationavailable = [bank['IsVerficationAvailable'] for bank in bank_data]
    # context = {
    #     'bank_data':bank_data,
    #     'bank_id': bank_id,
    #     'bank_names': bank_names,
    #     'bank_shortcode': bank_shortcode,
    #     'bank_imps_status': bank_imps_status,
    #     'bank_neft_status': bank_neft_status,
    #     'bank_isverficationavailable' : bank_isverficationavailable,
    # }
    # return context
    return bank_data

def generate_timestamp():
    custom_datetime = datetime.datetime(2023, 2, 13, 15, 11, 38, 43000)
    timezone_offset = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime('%z')
    formatted_timestamp = custom_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + timezone_offset
    return formatted_timestamp