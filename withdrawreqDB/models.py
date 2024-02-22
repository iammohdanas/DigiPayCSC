from django.db import models

# Create your models here.
class Transaction(models.Model):
    txn_id = models.CharField(max_length=100, verbose_name="Transaction ID", primary_key=True)
    timestamp = models.DateTimeField(verbose_name="Timestamp")
    customer_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Customer ID")
    aadhaar_number = models.CharField(max_length=100, verbose_name="Aadhaar Number")
    transaction_type = models.CharField(max_length=100, verbose_name="Transaction Type")
    transaction_amount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Transaction Amount Value")
    transaction_amount_currency = models.CharField(max_length=3, verbose_name="Transaction Amount Currency")
    transaction_status = models.CharField(max_length=100, blank=True, null=True, verbose_name="Transaction Status")
    error_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Error Code")
    merchant_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Merchant ID")
    terminal_id = models.CharField(max_length=100, verbose_name="Terminal ID")
    bank_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bank ID")
    location = models.CharField(max_length=100, verbose_name="Location")
    transaction_ref_number = models.CharField(max_length=100, verbose_name="Transaction Reference Number", unique=True)
    response_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Response Code")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    user_agent = models.TextField(blank=True, null=True, verbose_name="User Agent")
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Transaction Fee")
    customer_reference_number = models.CharField(max_length=100, verbose_name="Customer Reference Number",null=True, unique=True)