import json
import random
import string
import datetime
from django.http import JsonResponse
import xml.etree.ElementTree as ET

def generate_order_id():
    current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    order_id = f"ORDERID_{current_datetime}_{random_chars}"
    return order_id


def dict_to_xml(dict_data):
    root = ET.Element("FormData")
    for key, value in dict_data.items():
        element = ET.SubElement(root, key)
        element.text = str(value)
    return ET.tostring(root, encoding='utf-8')
