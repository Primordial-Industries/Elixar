from django.contrib import admin
from django.urls import path
from . import views

app_name = 'PayApp'

urlpatterns = [
    path('', views.Home, name = "home"),
    path('FreeTrial/', views.Trial, name = "Trial"),
    path('<str:course>/RegisterPayment/', views.PaymentLogin, name = "PaymentLogin"),
    path('Verify/', views.Verify, name = "Verify"),
    path('Verify_for_payment/', views.verifyPay, name = "verifyPay"),
    path('Calender/', views.Calender, name = "Calender"),
    path('confirm_order', views.create_order, name = 'create_order'),
    path('gcalendar', views.gcalendar, name = 'gcalendar'),
    path('meeting', views.meeting, name = 'meeting'),
    path('datet/', views.datet, name = 'datet'),
    # path('blog/', views.blog, name = 'blog'),
    # path('mainp/', views.mainp, name = 'mainp'),
    path('payment_status', views.payment_status, name = 'payment_status'),
    path('resend_otp/', views.reOTPtrial, name = 'reOTPtrial'),
    path('resend_otp_pay/', views.reOTPpay, name = 'reOTPpay'),
    path('FreeTrial/verify/', views.direct1, name = 'direct1'),
    path('FreeTrial/Calender/', views.direct2, name = 'direct2'),

]

