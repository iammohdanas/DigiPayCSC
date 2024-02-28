import datetime
import random
import string
import time
import xmltodict
from datetime import datetime

def process_withdrawform():
    aadhar_number = str(input("Enter 12 digits aadhar number : "))
    txn_amount = str(input("Enter transaction amount : "))
    bank_shortcode = "BARB"
    transaction_type = "22"
    bank_name = "Bank of Baroda"
    bank_iin = "606985"
    txn_id = bank_shortcode[:3]+ str(random.randint(10**31, 10**32 - 1))
    alphanumeric_chars = string.ascii_letters + string.digits
    msg_id = bank_shortcode[:3] + ''.join(random.choices(alphanumeric_chars, k=29))
    customer_ref_number = str(random.randint(100000000000, 999999999999))

    current_local_time = datetime.now()
    offset_seconds = -time.timezone if (time.localtime().tm_isdst == 0) else -time.altzone
    offset_hours = offset_seconds // 3600
    offset_minutes = (offset_seconds % 3600) // 60
    offset_str = "{:02d}:{:02d}".format(abs(offset_hours), abs(offset_minutes))
    offset_str = ("+" if offset_hours >= 0 else "-") + offset_str
    ts = current_local_time.strftime('%Y-%m-%dT%H:%M:%S') + offset_str

    current_local_time = datetime.now()
    offset_seconds = -time.timezone if (time.localtime().tm_isdst == 0) else -time.altzone
    offset_hours = offset_seconds // 3600
    offset_minutes = (offset_seconds % 3600) // 60
    offset_str = "{:02d}:{:02d}".format(abs(offset_hours), abs(offset_minutes))
    offset_str = ("+" if offset_hours >= 0 else "-") + offset_str
    crnTns = current_local_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + offset_str

    context = {

        "ns2ReqPay": {
            "@xmlnsns2": "http://npci.org/upi/schema/",
            "@xmlnsns3": "http://npci.org/cm/schema/",
            "Head": {
                "@callbackEndpointIP": "192.168.48.237",
                "@msgId": msg_id,
                "@orgId": "232323",
                "@prodType": "AEPS",
                "@ts": ts,
                "@ver": "2.0"
            },
            "Txn": {
                "@crtnTs": crnTns,
                "@custRef": customer_ref_number,
                "@id": txn_id,
                # "@initiationMode": "00",
                "@note": "AEPS Transaction",
                "@purpose": transaction_type,
                "@refId": "008142",
                "@refUrl": "https://www.npci.org.in/",
                "@subType": "PAY",
                "@ts": ts,
                "@type": "PAY"
            },
            "Payer": {
                "@addr": "232323@ore",
                "@code": "6012",
                "@name": "",
                "@seqNum": "0",
                "@type": "ENTITY",
                "Info": {
                    "Identity": {
                        "@type": "BANK",
                        "@verifiedName": bank_name
                    },
                    "Rating": {
                        "@verifiedAddress": "TRUE"
                    }
                },
                "Device": {
                    "Tag": [
                        {"@name": "TYPE", "@value": "INET"},
                        {"@name": "posEntryCode", "@value": "019"},
                        {"@name": "posServCdnCode", "@value": "05"},
                        {"@name": "cardAccpTrId", "@value": "register"},
                        {"@name": "cardAccIdCode", "@value": ""},
                        {"@name": "LOCATION", "@value": ""},
                        {"@name": "PinCode", "@value": "123456"},
                        {"@name": "AgentId", "@value": "XXXXXXXXXXXXXXXXXXXXXXXXX"}
                    ]
                },
                "Ac": {
                    "@addrType": "AADHAAR",
                    "Detail": [
                        {"@name": "IIN", "@value": bank_iin},
                        {"@name": "UIDNUM", "@value": aadhar_number}
                    ]
                },
                "Creds": {
                    "Cred": {
                        "@subType": "AADHAAR-BIO-FP",
                        "@type": "AADHAAR",
                        "Auth": {
                            "@ac": "STGNPCI001",
                            "@lk": "MLIfwcvTfWA0o8qdLa_SWgMMRgvWzaynhOg9YmLdQsgusioghfshOE-38",
                            "@rc": "Y",
                            "@sa": "STGNPCI001",
                            "@tid": "registered",
                            "@txn": "008142",
                            "@uid": "",
                            "@ver": "2.5",
                            "Uses": {
                                "@pi": "n",
                                "@pa": "n",
                                "@pfa": "n",
                                "@bio": "y",
                                "@bt": "FMR,FIR",
                                "@pin": "n",
                                "@otp": "n"
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
                            "Skey": {
                                "@ci": "20250929",
                            },
                            "Hmac": {},
                            "Data": {"@type":"X"}
                        }
                    }
                },
                "Amount": {
                    "@curr": "INR",
                    "@value": txn_amount
                }
            },
            "Payees": {
                "Payee": {
                    "@addr": "@663366.iin.npci",
                    "@code": "0000",
                    "@seqNum": "0",
                    "@type": "PERSON",
                    "Amount": {
                        "@curr": "INR",
                        "@value": txn_amount
                    },
                    "Creds": {
                        "Cred": {
                            "@subType": "NA",
                            "@type": "PostCredit"
                        }
                    }
                }
            },
            "Signature": {
                "@xmlns": "http://www.w3.org/2000/09/xmldsig#",
                "SignedInfo": {
                    "CanonicalizationMethod": {
                        "@Algorithm": "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
                    },
                    "SignatureMethod": {
                        "@Algorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
                    },
                    "Reference": {
                        "@URI": "",
                        "Transforms": {
                            "Transform": {
                                "@Algorithm": "http://www.w3.org/2000/09/xmldsig#enveloped-signature"
                            }
                        },
                        "DigestMethod": {
                            "@Algorithm": "http://www.w3.org/2001/04/xmlenc#sha256"
                        },
                        "DigestValue": "qMX89cH6TbRh15pHG4P+3phZkMtqCs7YWRKAJq/7c/s=",
                    }
                },
                "SignatureValue": "fpZW7CKcQ4fZZGfiveUBuidJtapmhIM46unQGPeMyNl",
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

    xml_data = xmltodict.unparse(context, full_document=False)
    xml_data = xml_data.replace('<ns2ReqPay', '<ns2:ReqPay').replace('</ns2ReqPay>', '</ns2:ReqPay>')
    xml_data = xml_data.replace('xmlnsns2="http://npci.org/upi/schema/"', 'xmlns:ns2="http://npci.org/upi/schema/"')
    xml_data = xml_data.replace('xmlnsns3="http://npci.org/cm/schema/"','xmlns:ns3="http://npci.org/cm/schema/"')
    xml_response = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_data
    
    # Return the XML response
    return xml_response

print(process_withdrawform())