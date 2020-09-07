from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Student, FreeTrialSub, ConquereSub, Course, ExplorerSub
from django.core.mail import send_mail
import random
import razorpay
from django.contrib import messages

client = razorpay.Client(auth=("rzp_test_JvDA7T1fvpIDXj", "4MIuwamLHLmUjrILyXFyiq3U"))
# Create your views here.
global OTP
def Home(request):
    return render(request, 'PayApp/arscience.html')


def Trial(request):                                           # view for free trial
    if request.method == "POST":
        mail = request.POST.get('email', '')
        phnum = request.POST.get('Phone', '')
        fname = request.POST.get('fname', '') 
        lname = request.POST.get('lname', '')
        name = fname + lname
        school = request.POST.get('school', '')
        # gender = request.POST.get('gender', '')
        course = Course.objects.get(name= 'Free Trial')
        try:
            std = Student.objects.get(email= mail, phone=phnum)
        except Student.DoesNotExist:
            std = Student(name=name,email=mail,phone=phnum,school=school,courseapp=course)
            us = User(username=mail, email=mail)                     # Session Management
            us.set_password(phnum)
            us.save()
            std.active_key = random.randint(100000, 999999)         # generating OTP
            keya = std.active_key    
            std.save()          # creating student
            # sending email
            send_mail('Your OTP is {}'.format(keya),message="", from_email='p.abhijeetp94@gmail.com', recipient_list= [mail], fail_silently= False)
            val = authenticate(username = mail, password = phnum)
            login(request, val)

        datasend = {'email': mail, 'name':name, 'phone':phnum}
        return redirect('PayApp:Verify')
    return render(request, 'PayApp/loginTrial.html')

def Verify(request):
    mail = request.user
    emai = mail.email
    stda = Student.objects.get(email = mail)
    phone = stda.phone
    msg = {}
    if request.method == "POST":
        iOTP = request.POST.get('OTP', '')
        print(stda.active_key)
        print(iOTP)
        if int(iOTP) == int(stda.active_key):
            try:
                stdf = FreeTrialSub.objects.get(user=stda)
            except FreeTrialSub.DoesNotExist:
                stdf = FreeTrialSub(user=stda, phone = phone)
                stdf.save()
            stda.verif = True
            return redirect("PayApp:Calender")
        else:
            print("Some Error")
            msg = messages.info(request, message='Invalid OTP Try Again!!')
    return render(request, 'PayApp/verify.html', msg)

def PaymentLogin(request, course):
    crs = Course.objects.get(name=course)
    if request.method == "POST":
        mail = request.POST.get('email', '')
        phnum = request.POST.get('Phone', '')
        fname = request.POST.get('fname', '') 
        lname = request.POST.get('lname', '')
        name = '{} {}'.format(fname,lname)
        print(name)
        school = request.POST.get('school', '')
        # gender = request.POST.get('gender', '')
        # course = Course.objects.get(name= 'Free Trial')
        try:
            std = Student.objects.get(email= mail,phone = phnum)
        except Student.DoesNotExist:
            std = Student(name=name,email=mail,phone=phnum,school=school,courseapp=crs)
            us = User(username=mail, email=mail)
            
            us.set_password(phnum)
            us.save()
            std.active_key = random.randint(100000, 999999)
            keya = std.active_key
            std.save()
            send_mail('Your OTP for {} course is {}'.format(course, keya),message="", from_email='p.abhijeetp94@gmail.com', recipient_list= [mail], fail_silently= False)
            val = authenticate(username = mail, password = phnum)
            login(request, val)

        datasend = {'email': mail, 'name':name, 'phone':phnum}
        return redirect('PayApp:verifyPay')
    return render(request, 'PayApp/loginPay.html')

def verifyPay(request):
    mail = request.user
    emai = mail.email
    stda = Student.objects.get(email = mail)
    crs = stda.courseapp.name
    phone = stda.phone
    msg = {}
    if request.method == "POST":
        iOTP = request.POST.get('OTP', '')
        print(stda.active_key)
        print(iOTP)
        if int(iOTP) == int(stda.active_key):
            if crs == 'Conquere':
                try:
                    stdc = ConquereSub.objects.get(user=stda)
                except ConquereSub.DoesNotExist:
                    stdc = ConquereSub(user=stda, phone = phone)
                    stdc.save()
            elif crs == 'Explorer':
                try:
                    stde = ExplorerSub.objects.get(user=stda)
                except ExplorerSub.DoesNotExist:
                    stde = ExplorerSub(user=stda, phone = phone)
                    stde.save()
            stda.verif = True
            return redirect("PayApp:create_order")
        else:
            print("Some Error")
            msg = messages.info(request, message='Invalid OTP Try Again!!')
    return render(request, 'PayApp/verifypay.html', msg)

def Calender(request):
    if request.user.is_authenticated:
        us = request.user
        mail = us.email
        std = Student.objects.get(email=mail)
        logout(request)
        us.delete()

        return render(request, 'PayApp/calender.html', context= {'email':mail})
    return redirect('PayApp:Home')

def create_order(request):
    if request.user.is_authenticated:
        us = request.user
        mail = us.email
        std = Student.objects.get(email=mail)
        name = std.name
        phone = std.phone
        course = std.courseapp
        crsname = course.name
        context = {}
        # if request.method == 'POST':
            # print("INSIDE Create Order!!!")
            # name = request.POST.get('name')
            # phone = request.POST.get('phone')
            # email = request.POST.get('email')
            # product = request.POST.get('product')

        order_amount = 0
        order_amount = course.price

        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {
            'Shipping address': 'Bommanahalli, Bangalore'}

        # CREAING ORDER
        response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        order_id = response['id']
        order_status = response['status']

        if order_status=='created':

            # Server data for user convinience
            context['course_name'] = crsname
            context['price'] = order_amount
            context['name'] = name
            context['phone'] = phone
            context['email'] = mail

            # data that'll be send to the razorpay for
            context['order_id'] = order_id
            print(order_id)
            return render(request, 'PayApp/confirm_order.html', context)


        # print('\n\n\nresponse: ',response, type(response))
    return HttpResponse('<h1>Error in  create order function</h1>')



def payment_status(request):

    response = request.POST
    user = request.user
    mail = user.email
    std = Student.objects.get(email=mail)
    logout(request)
    us.delete()
    course = std.courseapp.name
    if course == 'Conquere':
        courseown = ConquereSub.objects.get(user = std)
    elif course == 'Explorer':
        courseown = ExplorerSub.objects.get(user = std)
    courseown.paid = True
    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }


    # VERIFYING SIGNATURE
    try:
        status = client.utility.verify_payment_signature(params_dict)
        if course == 'Conquere':
            courseown = ConquereSub.objects.get(user = std)
        elif course == 'Explorer':
            courseown = ExplorerSub.objects.get(user = std)
        courseown.paid = True
        return render(request, 'PayApp/order_summary.html', {'status': 'Payment Successful'})
    except:
        return render(request, 'PayApp/order_summary.html', {'status': 'Payment Faliure!!!'})

