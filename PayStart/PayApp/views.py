
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Student, FreeTrialSub, ConquereSub, Course, ExplorerSub, TrialMeeting, UserProfile, Enroll
from django.core.mail import send_mail
import random
import datetime
import razorpay
from django.contrib import messages
# from . import quickstart


client = razorpay.Client(auth=("rzp_test_JvDA7T1fvpIDXj", "4MIuwamLHLmUjrILyXFyiq3U"))                  # Edit your razorpay credentials
# Create your views here.
def Home(request):
    return render(request, 'PayApp/mainpage.html')
def direct1(request):
    return render(request, 'PayApp/verify.html')

def direct2(request):
    return render(request, 'PayApp/calender.html')

def reOTPpay(request):
    if request.user.is_authenticated:
        us = request.user
        mail = us.email
        std = Enroll.objects.get(email=mail)
        course = std.courseapp.name
        std.active_key = random.randint(100000,999999)
        std.save()
        send_mail('OTP Validation',html_message='Your OTP for {} course is {}'.format(course, keya), from_email='kalam-labs@elixarsystem.com', recipient_list= [mail], fail_silently= False)
        return redirect('PayApp:verifyPay')
    return redirect('PayApp:home')

def reOTPtrial(request):
    if request.user.is_authenticated:
        us = request.user
        mail = us.email
        std = Enroll.objects.get(email=mail)
        course = std.courseapp.name
        std.active_key = random.randint(100000,999999)
        std.save()
        send_mail('OTP Validation','Your OTP for {} course is {}'.format(course, std.active_key), from_email='kalam-labs@elixarsystems.com', recipient_list= [mail], fail_silently= False)
        return redirect('PayApp:Verify')
    return redirect('PayApp:home')

def Trial(request):                                           # view for free trial
    if request.method == "POST":
        mail = request.POST.get('email', '')
        phnum = request.POST.get('Phone', '')
        fname = request.POST.get('fname', '') 
        lname = request.POST.get('lname', '')
        name = "{} {}".format(fname, lname)
        school = request.POST.get('school', '')
        # gender = request.POST.get('gender', '')
        course = Course.objects.get(name= 'Free Trial')
        try:
            us = User.objects.get(username=mail)
        except User.DoesNotExist:
            us = User(username=mail, email=mail)
            us.set_password(phnum)
            us.save()
        try:
            usp = UserProfile.objects.get(auth_user = us)
        except UserProfile.DoesNotExist:
            usp = UserProfile(auth_user=us, phone=phnum, college=school)
            usp.save()
        
        try:                                                        
            std = Enroll.objects.get(email= mail)
                                                      #creating session
        except Enroll.DoesNotExist:
            std = Enroll(name=name,email=mail,phone=phnum,school=school,courseapp=course)
        std.active_key = random.randint(100000, 999999)         # generating Activation Key
        keya = std.active_key    
        std.save()                                               # creating student
        # sending email
        send_mail('Your OTP is {}'.format(keya),message="", from_email='kalam-labs@elixarsystems.com', recipient_list= [mail], fail_silently= False)
        val = authenticate(username = mail, password = phnum)
        login(request, val)

        datasend = {'email': mail, 'name':name, 'phone':phnum}
        return redirect('PayApp:Verify')
    return render(request, 'PayApp/registertrial.html')

def Verify(request):
    if request.user.is_authenticated:
        mail = request.user
        emai = mail.email
        stda = Enroll.objects.get(email = emai)
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
                return redirect("PayApp:meeting")
            else:
                print("Some Error")
                messages.info(request, message='Invalid OTP Try Again!!')
                return redirect('PayApp:Verify')
        return render(request, 'PayApp/verify.html')
    else:
        return redirect('PayApp:Trial')

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
            us = User.objects.get(username=mail)
        except User.DoesNotExist:
            us = User(username=mail, email=mail)
            us.set_password(phnum)
            us.save()
        try:
            usp = UserProfile.objects.get(auth_user = us)
        except UserProfile.DoesNotExist:
            usp = UserProfile(auth_user=us, phone=phnum, college=school)
            usp.save()
        
        try:                                                        
            std = Enroll.objects.get(email= mail)
                                                      #creating session
        except Enroll.DoesNotExist:
            std = Enroll(name=name,email=mail,phone=phnum,school=school,courseapp=crs)
        std.active_key = random.randint(100000, 999999)
        keya = std.active_key
        std.save()
        send_mail('Your OTP for {} course is {}'.format(course, keya),message="", from_email='kalam-labs@elixarsystems.com', recipient_list= [mail], fail_silently= False)
        val = authenticate(username = mail, password = phnum)
        login(request, val)

        datasend = {'email': mail, 'name':name, 'phone':phnum}
        return redirect('PayApp:verifyPay')
    return render(request, 'PayApp/register.html')

def verifyPay(request):
    if request.user.is_authenticated:
        mail = request.user
        emai = mail.email
        stda = Enroll.objects.get(email = mail)
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
                stda.save()
                return redirect("PayApp:create_order")
            else:
                print("Some Error")
                messages.info(request, message='Invalid OTP Try Again!!')
                return redirect('PayApp:VerifyPay')
        return render(request, 'PayApp/verifypay.html')
    return redirect('PayApp:home')

def Calender(request):
    if request.user.is_authenticated:
        us = request.user
        mail = us.email
        std = Enroll.objects.get(email=mail)
        logout(request)
        date = datetime.date.today()
        nextday = date + datetime.timedelta(days = 1)
        return render(request, 'PayApp/calender.html', context= {'email':mail, 'today':date, 'tomorrow':nextday})
    return redirect('PayApp:home')

def create_order(request):
    if request.user.is_authenticated:
        us = request.user
        mail = us.email
        std = Enroll.objects.get(email=mail)
        name = std.name
        phone = std.phone
        course = std.courseapp
        crsname = course.name
        context = {}
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
    if request.user.is_authenticated:
        response = request.POST
        user = request.user
        mail = user.email
        std = Enroll.objects.get(email=mail)
        logout(request)
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
            courseown.save()
            return render(request, 'PayApp/order_summary.html', {'status': 'Payment Successful'})

        except:
            return render(request, 'PayApp/order_summary.html', {'status': 'Payment Faliure!!!'})
    else:
        return redirect('PayApp:home')



def gcalendar(request):
    # build_service()
    if request.user.is_authenticated:
        us = request.user
        mail = us.email
        std = Enroll.objects.get(email=mail)
        logout(request)
        if request.method == "POST":
            dt = request.POST.get('tools', '')
            print(dt)
            print(type(dt))
            hour = request.POST.get('budget', '')
            print(hour)
            time = datetime.time(hour=int(hour),minute= 00,second= 00)
            meeter = TrialMeeting(user = std, meetdate=dt, meettime=time, mailID=mail)
            meeter.save()
            send_mail('Invitation', 'Your meeting is confirmed with elixar systems on {} {}'.format(dt, time), 'kalam-labs@elixarsystems.com', [mail])
            return redirect('PayApp:home')
        else:
            print("Some error")
    print("Some Error")
    return redirect('PayApp:home')

def meeting(request):
    # build_service()
    if request.user.is_authenticated:
        date = datetime.date.today()
        day2 = date + datetime.timedelta(days = 1)
        day3 = date + datetime.timedelta(days = 2)
        day4 = date + datetime.timedelta(days = 3)
        day5 = date + datetime.timedelta(days = 4)
        day6 = date + datetime.timedelta(days = 5)
        day7 = date + datetime.timedelta(days = 6)
        days = {'today': date, 'day2': day2, 'day3': day3, 'day4': day4, 'day5': day5, 'day6': day6, 'day7': day7}
        us = request.user
        mail = us.email
        std = Enroll.objects.get(email=mail)
        if request.method == "POST":
            dt = request.POST.get('tools', '')
            print(dt)
            print(type(dt))
            hour = request.POST.get('budget', '')
            print(hour)
            time = datetime.time(hour=int(hour),minute= 00,second= 00)
            meeter = TrialMeeting(user = std, meetdate=dt, meettime=time, mailID=mail)
            send_mail('Invitation', 'Your meeting is confirmed with elixar systems on {} {}'.format(dt, time), 'kalam-labs@elixarsystems.com', [mail])
            return redirect('PayApp:home')
        else:
            print("Some error")
        return render(request, 'PayApp/meeting.html', days)
    return redirect('PayApp:home')

def datet(request):
    return render(request, "PayApp/meeting.html")



# def build_service():
#     service_account_email = 'abhijeet-pandey@quickstart-1599466419791.iam.gserviceaccount.com'         # google credentials service account

#     CLIENT_SECRET_FILE = 'PayApp/Calendar/crede.p12'                                                    # google credentials .p12 file load

#     SCOPES = 'https://www.googleapis.com/auth/calendar'
#     scopes = [SCOPES]
#     credentials = ServiceAccountCredentials.from_p12_keyfile(
#         service_account_email=service_account_email,
#         filename=CLIENT_SECRET_FILE,                                        # Enter your google credentials here
#         scopes=SCOPES
#     )

#     http = credentials.authorize(httplib2.Http())

#     service = build('calendar', 'v3', http=http)

#     return service


# def create_event(date, time):
#     service = build_service()
#     start_datetime = datetime.datetime.combine(date=date, time=time)
#     tz = pytz.UTC
#     start_datetime_zone = start_datetime.replace(tzinfo=tz)
#     # start_datetime = datetime.datetime.now(tz=pytz.utc)
#     event = service.events().insert(calendarId='primary', body={
#         'summary': 'Meet',
#         'description': 'Google meetings',
#         'start': {'dateTime': start_datetime_zone.isoformat()},
#         'end': {'dateTime': (start_datetime_zone + timedelta(minutes=60)).isoformat()},
#     }).execute()
#     print(event)

# def blog(request):
#     return render(request, 'PayApp/blog.html')

# def mainp(request):
#     return render(request, 'PayApp/mainpage.html')