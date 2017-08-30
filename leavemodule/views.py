# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render
from basic.models import User
from django.http import HttpResponse
from leavemodule.models import Leave_credits, Application, Sanction
# Create your views here.

# class leaves():
LEAVES={
    1:'Casual Leave',
    2:'Restricted Leave',
    3:'Special Casual Leave',
    4:'Earned Leave',
    5:'Commuted Leave',
    6:'Vacation Leave'
}
def index(request):
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
        user=User.objects.get(email=email)
        application=Application.objects.filter(pf_in=user)
        context={
            'application':application,
            'email':email,
            'leaves':LEAVES
        }
        print (email)
        return render(request,'leavemodule/response.html',context)

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

def inbox(request):
    if 'email' in request.session:
        # print request.session.get('email')
        email = request.session.get('email').encode('utf-8')
        user=User.objects.get(email=email)
        application=Application.objects.filter(pf_out=user.pf)
        xx=0
        for app in application:
            if (app.status==0 or app.status==2):
                xx=1
                break
        context={
            'application':application,
            'email':email,
            'cl_rh':[1,2],
            'others':[3,4,5,6],
            'leaves':LEAVES,
            'check':xx
        }
        return render(request,'leavemodule/inbox.html',context)

def process(request,ap_id):
    if 'email' in request.session:
        # print request.session.get('email')
        email = request.session.get('email').encode('utf-8')
        user=User.objects.get(email=email)
        application=Application.objects.get(pk=ap_id)
        # x=request.POST.get('submit')
        # print("x=",type(x))
        print(type(application.status))
        if(request.POST.get('submit') == 'approve'):
            print("1")
            application.status=1
            application.remarks=request.POST.get('remark')
        elif(request.POST.get('submit') == 'reject'):
            print("2")
            application.status=3
            application.remarks=request.POST.get('remark')
        elif(request.POST.get('submit') == 'forward'):
            application.status=2
            if application.pf_in.is_staff == False:
                application.pf_out=1001
            else:
                sanction=Sanction.objects.get(department=application.pf_in.department)
                application.pf_out=sanction.sanction_others
        application.save()
        return redirect("/leave_module/inbox")

# def reject(request):



# def submit(request):
