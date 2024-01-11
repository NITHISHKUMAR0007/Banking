from django.db import models

# Create your models here.

class register_table(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email_id=models.EmailField()
    password=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=50)
    account_number=models.CharField(max_length=100)
    deposit_amount=models.CharField(max_length=100)

class bank_statment_table(models.Model):
    account_holder_name=models.CharField(max_length=100)
    account_number=models.CharField(max_length=100)
    deposit_amount=models.CharField(max_length=100)
    withdraw_amount=models.CharField(max_length=100)
    balance_amount=models.CharField(max_length=100)
    date_of_transaction=models.CharField(max_length=100)