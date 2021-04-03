from django.shortcuts import render
from django.http import HttpResponse
from .import models
from .models import  *
from . import Forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.utils import timezone
import datetime
import time
import json
import requests
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return not_logged(request)
    #print(request.user.id)
    #print(request.user)
    return render(request,"Homepage.html")

def not_logged(request):
    return render(request,"index.html")
def logout_view(request):
    logout(request)
    return not_logged(request)

def request_leave(request):
    leave_form=Forms.LeaveModelForm(initial={'starting_date':'yyyy-mm-dd'})
    if request.method=="POST":
        data=request.POST
        user=User.objects.get(id=request.user.id)
        print(data)
        obj=LeaveModel()
        obj.user=user
        obj.starting_date=data["starting_date"]
        print(obj.starting_date)
        obj.no_of_days=data["no_of_days"]
        obj.reason=data["reason"]
        obj.save()
        return index(request)
        leave_form.user=None
    data={
        "form":leave_form
    }

    return render(request,"RequestLeave.html",data)

def login_view(request):
    if request.method=="POST":
        print(request.POST)
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            a=login(request,user)
            return index(request)
        else:
            return HttpResponse("invalid credentails")
        return HttpResponse("IN login post")

    return render(request,"LoginPage.html")    
def user_leaves_all(request):
    #print(request.user)
    total_leaves=LeaveModel.objects.filter(user=request.user)
    leaves=[obj.__dict__ for obj in total_leaves]
    leaves=leaves[::-1]
    #print(leaves)
    return render(request,"user_leaves.html",{"leaves":leaves})
def compare_dates(todaydate,lastlogindate):
    if todaydate==lastlogindate:
        return True
    else:
        return False    
def profile(request):
    if not request.user.is_authenticated:
        return not_logged(request)
    details=Profile.objects.filter(user=request.user)
    detail_pro=[obj.__dict__ for obj in details]
    #print(detail_pro[0]['avatar'])
    # det=obj.__dict__ 
    # print(det)
    
    return render(request,"profile.html",{"detail_pro":detail_pro})        
def manage_user_attendance(request):
    current_date=datetime.date.today()
    todaydate=str(current_date.day)+str(current_date.month)+str(current_date.year)
    in_times=InTimeModel.objects.filter(user=request.user)
    currt=time.localtime()
    clock=time.strftime("%H:%M:%S",currt)
    # print(clock)
    
    in_times=[i for i in in_times]
    try:

        last_in=in_times[-1]
    except:
        return render(request,"Attendence.html",{"is_logged_in":False,"is_logged_out":False})
    _month=last_in.__dict__['in_time'].month
    _year=last_in.__dict__['in_time'].year
    _day=last_in.__dict__['in_time'].day
    lastlogindate=str(_day)+str(_month)+str(_year)
    is_already_logged_in=compare_dates(todaydate,lastlogindate)
    # print(is_already_logged_in)
    context={
        "is_logged_in":is_already_logged_in,
        "is_logged_out":False
    }
    out_times=OutTimeModel.objects.filter(user=request.user)
    out_times=[i for i in out_times]
    try:
        last_out=out_times[-1]
    except:
        return render(request,"Attendence.html",{"is_logged_in":True,"is_logged_out":False})

    try:

        out_month=last_out.__dict__['out_time'].month
        out_year=last_out.__dict__['out_time'].year
        out_day=last_out.__dict__['out_time'].day
        last_logout_date=str(out_day)+str(out_month)+str(out_year)
    except:
        print("render 2")
        #return render(request,"Attendence.html",{"is_logged_in":True,"is_logged_out":False})
    print("------------->>--------",last_logout_date,todaydate)
    if last_logout_date==todaydate:
        return render(request,"popup.html")
        #return HttpResponse("YOU ALREADY COMPLETED TODAY SHIFT")
    else:
        context={
        "is_logged_in":is_already_logged_in,
        "is_logged_out":False
        }
        if True:
            return render(request,"Attendence.html",context)
            
    return HttpResponse("Attedance mangnnt")

# def visitor_ip_address(request):
    
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


def do_user_IN(request):

    obj=InTimeModel()
    # print("-------------IN TIME-------------")
    # print(obj)
    obj.user=request.user
    # print("--------->>>>>>>",visitor_ip_address(request))
    user_ip=get_client_ip(request)
    user_ip=list(user_ip)
    obj.ip=user_ip[0]
    url = f"http://api.ipstack.com/43.241.120.33?access_key=0a1666aa8f7b829ab5c4af3b8895742c"
    response = requests.get(url)
    responses=response.__dict__
    dictionary=responses['_content']
    geodata=json.loads(dictionary.decode('utf-8'))
    obj.City=geodata['city']
    obj.save()
    return index(request)

def do_user_OUT(request):
    obj=OutTimeModel()
    obj.user=request.user
    obj.save()
  
    enter = InTimeModel.objects.filter(user=request.user)
    out = OutTimeModel.objects.filter(user=request.user)
    out_times=[i for i in out]
    todayout=out_times[-1]
    in_times=[i for i in enter]
    todayin=in_times[-1]
    # print(todayin.time())
    a=todayout.out_time-todayin.in_time
    data=production_time()
    data.user=request.user
    data.Production_time=str(a)
    
    print(data)
    data.save()
    return index(request)
