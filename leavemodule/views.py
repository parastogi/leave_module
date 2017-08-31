# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render
from basic.models import User , DepartmentHead
from django.http import HttpResponse
from leavemodule.models import Leave_credits, Application, Sanction
from django.utils import timezone
import datetime

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
        user=User.objects.get(email=email)
        head=0
        print (email)
        # head=1
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
        user1=User.objects.all()
        list1=[]
        # list2=[]
        for u in user1:
            list1.append(u.name)
        lc=Leave_credits.objects.get(pf=user)
        context={
            'cl': lc.casual,
            'rh':lc.restricted,
            'spc':lc.sp_casual,
            'el':lc.earned,
            'col':lc.commuted,
            'vl':lc.vacation,
            'email':email,
            'list':list1
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

def submit(request):
    print ("xyz")
    if 'email' in request.session:
        email = request.session.get('email').encode('utf-8')
        user=User.objects.get(email=email)
        credit = Leave_credits.objects.get(pf=user.pf)
        # print(request.POST.get('acad_respo'))
        # print(request.POST.get('admin_respo'))
        user_admin=User.objects.get(name=request.POST.get('admin_respo'))
        user_acad=User.objects.get(name=request.POST.get('acad_respo'))
        if user.is_staff==True:
            sanction=Sanction.objects.get(department=user.department)
            pf_out=sanction.sanction_cl_rh.pf

        else:
            dh=DepartmentHead.objects.get(department=user.department)
            if user.name == dh.hod.name:
                pf_out=1001
            else:
                pf_out=dh.hod.pf
        credit = Leave_credits.objects.get(pf=user.pf)
        from_date=request.POST.get('leave_from')
        from_day=from_date[3:5]
        from_month=from_date[0:2]
        from_year=from_date[6:]
        from_date=from_day+from_month+from_year
        till_date=request.POST.get('leave_till')
        till_day=till_date[3:5]
        till_month=till_date[0:2]
        till_year=till_date[6:]
        till_date=till_day+till_month+till_year
        date_of_app=datetime.datetime.now()

        from_date=datetime.datetime.strptime(from_date, "%d%m%Y").date()
        till_date=datetime.datetime.strptime(till_date, "%d%m%Y").date()
        app_obj=Application(pf_in=user,pf_out=pf_out,status=0,type_of_leave=request.POST.get('leaves'),from_date=from_date,till_date=till_date,date_of_app=date_of_app,purpose=request.POST.get('purpose'),acad_pf=user_acad,admin_pf=user_admin)
        if(request.POST.get('is_station') == '12'):
            app_obj.is_station=True
            address=request.POST.get('address')
        else:
            app_obj.is_station=False

        print(app_obj.pf_in,app_obj.pf_out,app_obj.till_date,app_obj.date_of_app,app_obj.purpose,app_obj.admin_pf,app_obj.acad_pf,app_obj.type_of_leave,app_obj.from_date)
        # num_?of_leaves=diff.days
        app_obj.save()
        num_of_leaves = (app_obj.till_date-app_obj.from_date).days
        print(num_of_leaves)
        ap_id=app_obj.pk
        types = int(app_obj.type_of_leave)
        type_of_leave=LEAVES[types]
        if(types == 1):
            leavecredit=credit.casual
        elif(types == 2):
            leavecredit=credit.restricted
        elif(types == 3):
            leavecredit=credit.sp_casual
        elif(types == 4):
            leavecredit=credit.earned
        elif(types == 5):
            leavecredit=credit.commuted
        elif(types == 6):
            leavecredit=credit.vacation

        if leavecredit < num_of_leaves:
            message = "you don't have enough credit to take this leave"
            context={

            'message': message

            }

            return HttpResponse("teredada")
        else:
            return redirect('/leave_module/application')

    else:
        return redirect('basic:index')


def process(request,ap_id):
    if 'email' in request.session:
        # print request.session.get('email')
        email = request.session.get('email').encode('utf-8')
        user=User.objects.get(email=email)
        application=Application.objects.get(pk=ap_id)
        leave = Leave_credits.objects.get(pf=application.pf_in)
        # x=request.POST.get('submit')
        # print("x=",type(x))
        from_date=application.from_date
        till_date=application.till_date
        delta=till_date-from_date
        print('forcharity')
        print(delta.days)
        leave_type=application.type_of_leave
        print(type(application.status))
        if(request.POST.get('submit') == 'approve'):
            print("1")
            application.status=1
            application.remarks=request.POST.get('remark')
            if (leave_type == 1):
                print(leave.casual)
                leave.casual=leave.casual-delta.days-1
                print('aftermath')
                print(leave.casual)
            elif (leave_type == 2):
                leave.restricted=leave.restricted-delta.days-1
            elif (leave_type == 3):
                leave.sp_casual=leave.sp_casual - delta.days-1
            elif (leave_type == 4):
                leave.earned=leave.earned - delta.days-1
            elif (leave_type == 5):
                leave.commuted=leave.commuted - delta.days-1
            elif (leave_type == 6):
                leave.vacation=leave.vacation - delta.days-1

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
        leave.save()
        return redirect("/leave_module/inbox")
