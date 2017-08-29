# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render
from basic.models import User
from django.http import HttpResponse
from leavemodule.models import Leave_credits, Application
# Create your views here.
def  index(request):
    if 'email' in request.session:
        # print request.session.get('email')
        email = request.session.get('email').encode('utf-8')
        print (email)
        return render(request,'leavemodule/index.html',{'email':email})
    else:
        return redirect('basic:index')
def logout(request):
    request.session.flush()
    return redirect('/')

def application(request):
    if 'email' in request.session:
        # print request.session.get('email')
        email = request.session.get('email').encode('utf-8')
        user=User.objects.get(email=email)
        lc=Leave_credits.objects.get(pf=user)
        context={
            'cl': lc.casual,
            'rh':lc.restricted,
            'spc':lc.sp_casual,
            'el':lc.earned,
            'col':lc.commuted,
            'vl':lc.vacation,
            'email':email,
        }
        return render(request,'leavemodule/application.html',context)

def response(request):
    if 'email' in request.session:
        # print request.session.get('email')
        email = request.session.get('email').encode('utf-8')
        print (email)
        return render(request,'leavemodule/response.html',{'email':email})

def summary(request):
    if 'email' in request.session:
        # print request.session.get('email')
        email2=request.session.get('email')
        q=User.objects.get(email=email2)
        pf_id=q.pf
        print(q.is_staff)
        leave_credits=Leave_credits.objects.get(pf=pf_id)
        print(leave_credits.earned)
        email = email2.encode('utf-8')
        print (email)

        context={
            'email':email,
            'leave_credits':leave_credits,
        }
        return render(request,'leavemodule/credits.html',context)

# def submit(request):
