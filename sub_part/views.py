from django.shortcuts import render
from . models import *
from django.contrib import messages
from django.conf import settings
import random
from django.core.mail import send_mail
import datetime


  #django rest framework headers

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . serializers import PBI_registerd_datas



Account_number=str(86004200)+str(random.randint(1000,9999))

# Get request page
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')
def dashboard(request):
     return render(request,'dashboard.html')



def register_form_submission(request):
    if request.method =='POST':
        if register_table.objects.filter(email_id=request.POST.get('email_id')):
            messages.error(request,'This email  has already registered',extra_tags='already_registered')
            return render(request,'register.html')
        elif register_table.objects.filter(email_id=request.POST.get('email_id'),phone_number=request.POST.get('phone_number')):
            messages.error(request,'This email and phone number has already registered',extra_tags='already_registered')
            return render(request,'register.html')
        elif register_table.objects.filter(phone_number=request.POST.get('phone_number')):
            messages.error(request,'This phone number has already registered',extra_tags='already_registered')
            return render(request,'register.html')
        else:
            ex1=register_table(first_name=request.POST.get('first_name'),
                            last_name=request.POST.get('last_name'),
                            email_id=request.POST.get('email_id'),
                            password=request.POST.get('password'),
                            phone_number=request.POST.get('phone_number'),
                            account_number=Account_number,
                            deposit_amount=500,
                            )
                            
            ex1.save()
            try:
                first_name=request.POST.get('first_name')
                last_name=request.POST.get('last_name')
                email_id=request.POST.get('email_id')
                password=request.POST.get('password')
                phone_number=request.POST.get('phone_number'),
                account_number=Account_number,
                subject = ('Account Opening')
                message = f'Hi {first_name}, thank you for Opening Account  in Our bank \n Your Account number:{account_number}\n Password:{password}.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email_id, ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'login.html') 
            except:
                print("mail not sent")



def login_form_submission(request):
    if request.method=='POST':
        if register_table.objects.filter(account_number=request.POST.get('account_number'),password=request.POST.get('password')):
            print("**login successfully****")
            logger_data=register_table.objects.get(account_number=request.POST.get('account_number'),password=request.POST.get('password'))
            account_number=logger_data.account_number
            view_statments=bank_statment_table.objects.filter(account_number=account_number)
            return render(request,'dashboard.html',{'logger_data':logger_data,'view_statments':view_statments})            
        else:
            print("**invalid account number or password***")
            messages.error(request,'Invalid account number or password',extra_tags='failed')
            return render(request,'login.')
                         


def deposit_amount_stored(request,account_number):
    current_date_and_time=datetime.datetime.now()
    print(f"current date and time ->{current_date_and_time}")

    logger_data=register_table.objects.get(account_number=account_number)
    already_deposit_amount=logger_data.deposit_amount
    print(f"your balance amount:{already_deposit_amount}")
    current_deposit_amount=request.POST.get('deposit_amount')
    current_deposit_amount=int(already_deposit_amount)+int(current_deposit_amount)
    print(f"updated current deposit amount is {current_deposit_amount}")
    messages.error(request,'Amount deposited successfully!...',extra_tags='deposit')
    logger_data=register_table.objects.filter(account_number=account_number).update(deposit_amount=current_deposit_amount)
    print("amount updated successfully")
    logger_data=register_table.objects.get(account_number=account_number)
    firstname=logger_data.first_name
    lastname=logger_data.last_name
    account_holder_name=firstname+" "+lastname
    account_number=logger_data.account_number
    deposit_amount=request.POST.get('deposit_amount')
    balance_amount=logger_data.deposit_amount
    date_of_transaction=current_date_and_time
    bank_statment=bank_statment_table(account_holder_name=account_holder_name,
                                     account_number=account_number,
                                     deposit_amount=deposit_amount,
                                     balance_amount=balance_amount,
                                     withdraw_amount="-",
                                     date_of_transaction=date_of_transaction
                                     )
    bank_statment.save()
    print("**bank statment updated successfully****")
    view_statments=bank_statment_table.objects.filter(account_number=account_number)
    return render(request,'dashboard.html',{'logger_data':logger_data,'view_statments':view_statments})

def withdraw_amount_stored(request,account_number):
    logger_data=register_table.objects.get(account_number=account_number)
    already_deposit_amount=logger_data.deposit_amount
    print(f"your balance amount:{already_deposit_amount}")
    current_withdraw_amount=request.POST.get('withdraw_amount')
    print(f"current withdraw amount:{current_withdraw_amount}")
    
    if int(current_withdraw_amount)<=int(already_deposit_amount)-int(500):
        current_withdraw_amount=int(already_deposit_amount)-int(current_withdraw_amount)
        print(f"updated current deposit amount is {current_withdraw_amount}")
        messages.error(request,'Amount withdraw successfully!...',extra_tags='deposit')
        logger_data=register_table.objects.filter(account_number=account_number).update(deposit_amount=current_withdraw_amount)
        print("amount updated successfully")

        #*****bank statment update********
        logger_data=register_table.objects.get(account_number=account_number)
        current_date_and_time=datetime.datetime.now()
        print(f"current date and time ->{current_date_and_time}")
        firstname=logger_data.first_name
        lastname=logger_data.last_name
        account_holder_name=firstname+" "+lastname
        account_number=logger_data.account_number
        
        withdraw_amount=request.POST.get('withdraw_amount')
        balance_amount=logger_data.deposit_amount
        date_of_transaction=current_date_and_time

        bank_statment=bank_statment_table(account_holder_name=account_holder_name,
                                     account_number=account_number,
                                     balance_amount=balance_amount,
                                     deposit_amount="-",
                                     withdraw_amount=withdraw_amount,
                                     date_of_transaction=date_of_transaction
                                     )
        bank_statment.save()
        print("**bank statment updated successfully****")
    else:
        print("sorry please type proper amount")
        messages.error(request,'Please type proper amount',extra_tags='withdraw')
    logger_data=register_table.objects.get(account_number=account_number)
    view_statments=bank_statment_table.objects.filter(account_number=account_number)
    return render(request,'dashboard.html',{'logger_data':logger_data,'view_statments':view_statments})

    #django restframework------API convertion code
class PBI_register_List(APIView):
    def get(self,request):
        all_register_data=register_table.objects.all()
        serializer=PBI_registerd_datas(all_register_data,many=True)
        
        return Response(serializer.data)
    