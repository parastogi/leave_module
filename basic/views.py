# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from basic.models import User
from leavemodule.models import Sanction
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import messages


# Create your views here.
def index(request):
    if 'email' in request.session:

        email = request.session.get('email').encode('utf-8')
        # context={
        #     'uname': ,
        # }
        print (email)
        return render(request,'basic/index.html',{'email':email})
    else:
        context={
            'error':request.session.get('error')
        }
        return render(request,'basic/index.html',context)

def login(request):
    try:
        user=User.objects.get(email=request.POST['email'])
    except:
        request.session['error']="Wrong Credentials"
        return redirect('/')
    if user.password==request.POST['password']:
        # request.session['token']=1
        if 'error' in request.session:
            del request.session['error']
        request.session['email']=user.email
        user = authenticate(username=user.email, password=request.POST.get('password'))
        return redirect('/')
    else:
        print("Wrong")
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def enter(request):
    import os
    import csv
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(BASE_DIR+"/basic/Staff.csv") as f:
        reader = csv.reader(f)
        i=0
        for row in reader:
            if(i is 0):
                i+=1
                continue
            _, created = User.objects.get_or_create(
                pf=int(row[1]),
                name=row[2],
                designation=row[3],
                department=row[4],
                email=row[7],
                )
    with open(BASE_DIR+"/basic/Faculty.csv") as f:
        reader = csv.reader(f)
        i=0
        for row in reader:
            if(i is 0):
                i+=1
                continue
            _, created = User.objects.get_or_create(
                pf=int(row[1]),
                name=row[2],
                department=row[3],
                email=row[7],
                is_staff="False"
                )
def enter1(request):
    import os
    import csv
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(BASE_DIR+"/basic/Sheet1.csv") as f:
        reader = csv.reader(f)
        i=0
        for row in reader:
            print(float(row[1]))
            pf1=int(float(row[1]))
            pf2=int(float(row[2]))
            user1=User.objects.get(pf=pf1)
            user2=User.objects.get(pf=pf2)
            _, created = Sanction.objects.get_or_create(
                department=row[0],
                sanction_cl_rh=user1,
                sanction_others=user2
                )
