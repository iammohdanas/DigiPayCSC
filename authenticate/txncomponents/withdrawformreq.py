import datetime
from decimal import Decimal
import json
import random
from django.http import HttpResponse
from authenticate.components import generate_txn_id, generate_msg_id
from withdrawreqDB.models import Transaction
import pandas

def bankdata():
    file_path = 'authenticate\data\Bank_List.json'
    with open(file_path, 'r') as file:
        bank_data = json.load(file)
    bank_id = [bank['BankID'] for bank in bank_data]
    bank_names = [bank['BANK_NAME'] for bank in bank_data]
    bank_shortcode_data = [bank['ShortCode'] for bank in bank_data]
    bank_imps_status = [bank['IMPS_Status'] for bank in bank_data]
    bank_neft_status = [bank['NEFT_Status'] for bank in bank_data]
    bank_isverficationavailable = [bank['IsVerficationAvailable'] for bank in bank_data]
    context = {
        'bank_data':bank_data,
        'bank_id': bank_id,
        'bank_names': bank_names,
        'bank_shortcode': bank_shortcode_data,
        'bank_imps_status': bank_imps_status,
        'bank_neft_status': bank_neft_status,
        'bank_isverficationavailable' : bank_isverficationavailable,
    }
    return context


def withdraw_apireq(request):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + datetime.datetime.now().strftime("%z")
    if request.method == 'GET':
        customer_mobile_number = request.GET.get('customermobilenumber')
        aadhar_number = request.GET.get('aadharNumber')
        txn_amount = request.GET.get('amount')
        bank_shortcode = request.GET.get('bankOption')
        transaction_type = request.GET.get('transactionType', None)
    txn_amount = str(Decimal(txn_amount).quantize(Decimal('0.01')))
    aadhar_number = str(aadhar_number)
    file_path_bank_list = 'authenticate\data\Bank_List.json'
    with open(file_path_bank_list, 'r') as file:
        bank_data = json.load(file)
    for bank in bank_data:
        if bank['ShortCode'] == bank_shortcode:
            bank_name = bank['BANK_NAME']
    
    file_path_bank_IIN = 'authenticate\data\Bank_IIN_list.json'
    with open(file_path_bank_IIN, 'r') as file:
        bank_IIN_data = json.load(file)
    for bank in bank_IIN_data:
        if bank['Bank_Code'] == bank_shortcode:
            bank_iin = str(bank['IIN'])
        else:
            bank_iin = "Not Available"

    txn_id = generate_txn_id(request)
    while Transaction.objects.filter(txn_id=txn_id).exists():
        txn_id = generate_txn_id(request)
    
    msg_id = generate_msg_id(request)

    customer_ref_number = str(random.randint(100000000000, 999999999999))
    while Transaction.objects.filter(customer_reference_number=customer_ref_number).exists():
        customer_ref_number = str(random.randint(100000000000, 999999999999))

    transaction = Transaction.objects.create(
            txn_id=txn_id,
            timestamp=timestamp,
            aadhaar_number=aadhar_number,
            transaction_amount_value=txn_amount,
            bank_id=bank_shortcode,
            customer_reference_number = customer_ref_number           
        )
    context ={
    "ns2ReqPay": {
        "xmlnsns2": "http://npci.org/upi/schema/",
        "xmlnsns3": "http://npci.org/cm/schema/",
        "Head": {
            "callbackEndpointIP": "192.168.48.237",
            "msgId": "msg_id",
            "orgId": "232323",
            "prodType": "AEPS",
            "ts": "timestamp",
            "ver": "2.0"
        },
        "Txn": {
            "crtnTs": "timestamp",
            "custRef": "customer_ref_number",
            "id": "txn_id",
            "initiationMode": "00",
            "note": "AEPS Transaction",
            "purpose": "transaction_type",
            "refId": "008142",
            "refUrl": "https://www.npci.org.in/",
            "subType": "PAY",
            "ts": "timestamp",
            "type": "PAY"
        },
        "Payer": {
            "addr": "232323@ore",
            "code": "6012",
            "name": "",
            "seqNum": "0",
            "type": "ENTITY",
            "Info": {
                "Identity": {
                    "type": "BANK",
                    "verifiedName": "bank_name"
                },
                "Rating": {
                    "verifiedAddress": "TRUE"
                }
            },
            "Device": {
                "Tag": [
                    {
                        "name": "TYPE",
                        "value": "INET"
                    },
                    {
                        "name": "posEntryCode",
                        "value": "019"
                    },
                    {
                        "name": "posServCdnCode",
                        "value": "05"
                    },
                    {
                        "name": "cardAccpTrId",
                        "value": "register"
                    },
                    {
                        "name": "cardAccIdCode",
                        "value": ""
                    },
                    {
                        "name": "LOCATION",
                        "value": ""
                    },
                    {
                        "name": "PinCode",
                        "value": "123456"
                    },
                    {
                        "name": "AgentId",
                        "value": "XXXXXXXXXXXXXXXXXXXXXXXXX"
                    }
                ]
            },
            "Ac": {
                "addrType": "AADHAAR",
                "Detail": [
                    {
                        "name": "IIN",
                        "value": "bank_iin"
                    },
                    {
                        "name": "UIDNUM",
                        "value": "aadhar_number"
                    }
                ]
            },
            "Creds": {
                "Cred": {
                    "subType": "AADHAAR-BIO-FP",
                    "type": "AADHAAR",
                    "Auth": {
                        "ac": "STGNPCI001",
                        "lk": "MLIfwcvTfWA0o8qdLa_SWgMMRgvWzaynhOg9YmLdQsgusioghfshOE-38",
                        "rc": "Y",
                        "sa": "STGNPCI001",
                        "tid": "registered",
                        "txn": "008142",
                        "uid": "",
                        "ver": "2.5",
                        "Uses": {
                            "pi": "n",
                            "pa": "n",
                            "pfa": "n",
                            "bio": "y",
                            "bt": "FMR,FIR",
                            "pin": "n",
                            "otp": "n"
                        },
                        "Meta": {
                            "udc": "NPC000010700183",
                            "rdsId": "SCPL.WIN.001",
                            "rdsVer": "1.0.3",
                            "dpId": "Morpho.SmartChip",
                            "dc": "9a374a3f-9670-493f-86aa-8756ddcea24b",
                            "mi": "MSO1300E2L0SW",
                            "mc": ""
                        },
                        "Skey": {},
                        "Hmac": {},
                        "Data": {}
                    }
                }
            },
            "Amount": {
                "curr": "INR",
                "value": "txn_amount"
            }
        },
        "Payees": {
            "Payee": {
                "addr": "@663366.iin.npci",
                "code": "0000",
                "seqNum": "0",
                "type": "PERSON",
                "Amount": {
                    "curr": "INR",
                    "value": "txn_amount"
                },
                "Creds": {
                    "Cred": {
                        "subType": "NA",
                        "type": "PostCredit"
                    }
                }
            }
        },
        "Signature": {
            "xmlns": "http://www.w3.org/2000/09/xmldsig#",
            "SignedInfo": {
                "CanonicalizationMethod": {
                    "Algorithm": "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
                },
                "SignatureMethod": {
                    "Algorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
                },
                "Reference": {
                    "URI": "",
                    "Transforms": {
                        "Transform": {
                            "Algorithm": "http://www.w3.org/2000/09/xmldsig#enveloped-signature"
                        }
                    },
                    "DigestMethod": {
                        "Algorithm": "http://www.w3.org/2001/04/xmlenc#sha256"
                    },
                    "DigestValue": "qMX89cH6TbRh15pHG4P+3phZkMtqCs7YWRKAJq/7c/s="
                }
            },
            "SignatureValue": "",
            "KeyInfo": {
                "KeyValue": {
                    "RSAKeyValue": {
                        "Modulus": "",
                        "Exponent": "AQAB"
                    }
                }
            }
        }
    }
}
    return context



