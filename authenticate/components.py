import json
import random
import string
import datetime
from django.http import JsonResponse
import xml.etree.ElementTree as ET

def generate_txn_id(request):
    if request.method == 'GET':
        bank_shortcode = request.GET.get('bankOption')
    txn_id = bank_shortcode[:3]+ str(random.randint(10**31, 10**32 - 1))
    return txn_id


def dict_to_xml(dict_data):
    root = ET.Element("FormData")
    for key, value in dict_data.items():
        element = ET.SubElement(root, key)
        element.text = str(value)
    return ET.tostring(root, encoding='utf-8')

def bank_list():
    file_path = 'authenticate\data\Bank_List.json'
    with open(file_path, 'r') as file:
        bank_data = json.load(file)
    bank_id = [bank['BankID'] for bank in bank_data]
    bank_names = [bank['BANK_NAME'] for bank in bank_data]
    bank_shortcode = [bank['ShortCode'] for bank in bank_data]
    bank_imps_status = [bank['IMPS_Status'] for bank in bank_data]
    bank_neft_status = [bank['NEFT_Status'] for bank in bank_data]
    bank_isverficationavailable = [bank['IsVerficationAvailable'] for bank in bank_data]
    context = {
        'bank_data':bank_data,
        'bank_id': bank_id,
        'bank_names': bank_names,
        'bank_shortcode': bank_shortcode,
        'bank_imps_status': bank_imps_status,
        'bank_neft_status': bank_neft_status,
        'bank_isverficationavailable' : bank_isverficationavailable,
    }
    return context

