# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render
from basic.models import User , DepartmentHead
from django.http import HttpResponse
from django.contrib import messages
from leavemodule.models import Leave_credits, Application, Sanction, Inbox
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
error_message=""
def index(request):
    error_message=""
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

def applications(request):
    if 'email' in request.session:
        email = request.session.get('email').encode('utf-8')
        user=User.objects.get(email=email)
        try:
            inbox=Inbox.objects.filter(pf_in=user)
        except:
            return redirect('/leave_module/application')
        for inb in inbox:
            print("x")
        context={
            'inbox':inbox,
            'email':email
        }
        return render(request,'leavemodule/applications.html',context)

def application(request):
    error_message=""
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
    error_message=""
    if 'email' in request.session:
        # print request.session.get('email')
        email = request.session.get('email').encode('utf-8')
        user=User.objects.get(email=email)
        application=Application.objects.filter(pf_in=user)
        # application2=Application.objects.filter(acad_pf=user)


        context={
            'application':application,
            'email':email,
            'leaves':LEAVES,
        }
        print (email)
        return render(request,'leavemodule/response.html',context)

def summary(request):
    error_message=""
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
    error_message=""
    if 'email' in request.session:
        # print request.session.get('email')
        email = request.session.get('email').encode('utf-8')
        user=User.objects.get(email=email)
        application=Application.objects.filter(pf_out=user.pf)
        inbox1=Inbox.objects.filter(acad_res_pf=user)
        inbox2=Inbox.objects.filter(admin_res_pf=user)
        xx=0#to check if application accepted
        for app in application:
            if (app.status==0 or app.status==2):
                xx=1
                break
        print(xx)
        passed=[]
        hod=[]
        for app in application:
            if(app.pf_in.is_staff == False):
                dh=DepartmentHead.objects.get(department=app.pf_in.department)
                if(dh.hod.pf==app.pf_in.pf):
                    hod.append(app.pf_in.name)
            print(app.pk)
            inbox=Inbox.objects.get(ap_id=app.pk)
            if(inbox.acad_respo == 1 and inbox.admin_respo == 1):
                passed.append(app.pk)
        context={
            'application':application,
            'email':email,
            'cl_rh':[1,2],
            'others':[3,4,5,6],
            'leaves':LEAVES,
            'check':xx,
            'inbox1':inbox1,
            'inbox2':inbox2,
            'passed':passed,
            'hod':hod
        }
        return render(request,'leavemodule/inbox.html',context)
# def prevsubmit(request):
#     if 'email' in request.session:
#         email = request.session.get('email').encode('utf-8')
#         #Objects
#         user=User.objects.get(email=email)

def submit(request):
    error_message=""
    print ("xyz")
    if 'email' in request.session:
        email = request.session.get('email').encode('utf-8')
        #Objects
        user=User.objects.get(email=email)
        user_admin=User.objects.get(name=request.POST.get('admin_respo'))
        user_acad=User.objects.get(name=request.POST.get('acad_respo'))
        credits = Leave_credits.objects.get(pf=user.pf)
        # inbox=Inbox.objects.get(pf_in=user,ap_id)

        # print("x",credit.year)
        print(user.department)
        #Finding the person to which the application is to be forwarded
        dh = DepartmentHead.objects.get(department=user.department)
        if (dh.temp != dh.hod and dh.till < datetime.date.today()):
            print(dh.hod)
            dh.hod = dh.temp
            print(dh.temp)

            dh.save()

        if user.is_staff==True:
            sanction=Sanction.objects.get(department=user.department)
            pf_out=sanction.sanction_cl_rh.pf

        else:
            if user.pf == dh.hod.pf:
                pf_out=1001
            else:
                pf_out=dh.hod.pf


        # credit = Leave_credits.objects.get(pf=user.pf)

        #calculating time
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
        types = int(app_obj.type_of_leave)

        if(request.POST.get('is_station') == '12'):
            app_obj.is_station=True
            app_obj.address=request.POST.get('address')
            app_obj.st_from_date=request.POST.get('station_from')
            app_obj.st_till_date=request.POST.get('station_till')
        else:
            app_obj.is_station=False

        # print(app_obj.pf_in,app_obj.pf_out,app_obj.till_date,app_obj.date_of_app,app_obj.purpose,app_obj.admin_pf,app_obj.acad_pf,app_obj.type_of_leave,app_obj.from_date)
        num_of_leaves = (app_obj.till_date-app_obj.from_date).days
        print(credits.casual)
        ap_id=app_obj.pk
        if(app_obj.from_date.year>credits.year and app_obj.till_date.year>credits.year):
            credits.casual=8
            credits.restricted=2
            credits.sp_casual=credits.sp_casual+10*(app_obj.from_date.year-credits.year)
            credits.commuted=credits.commuted+20*(app_obj.from_date.year-credits.year)
            if user.is_staff == True:
                credits.earned=credits.earned+30*(app_obj.from_date.year-credits.year)
                credits.vacation=0
            else:
                credits.earned=credits.earned+(credits.vacation/2)+30*(app_obj.from_date.year-credits.year-1)
                credits.vacation=60

        if (app_obj.from_date.year<app_obj.till_date.year):
            if(types == 1):
                if(credits.casual>31-from_date.day):
                    credits.casual=credits.casual-(31-from_date.day)
            elif(types == 2):
                if(credits.restricted>31-from_date.day):
                    credits.restricted=credits.restricted-(31-from_date.day)
            elif(types == 3):
                if(credits.sp_casual>31-from_date.day):
                    credits.sp_casual=credits.sp_casual-(31-from_date.day)
            elif(types == 4):
                if(credits.earned>31-from_date.day):
                    credits.earned=credits.earned-(31-from_date.day)
            elif(types == 5):
                if(credits.commuted>31-from_date.day):
                    credits.commuted=credits.commuted-(31-from_date.day)
            elif(types == 6):
                if(credits.vacation>31-from_date.day):
                    credits.vacation=credits.vacation-(31-from_date.day)

            num_of_leaves=num_of_leaves-(31-from_date.day)

            credits.casual=8
            credits.restricted=2
            credits.sp_casual=credits.sp_casual+10
            credits.commuted=credits.commuted+20
            if user.is_staff == True:
                credits.earned=30+credits.earned
                credits.vacation=0
            else:
                credits.earned=credits.earned+(credits.vacation/2)
                credits.vacation=60

        type_of_leave=LEAVES[types]
        if(types == 1):
            leavecredit=credits.casual
        elif(types == 2):
            leavecredit=credits.restricted
        elif(types == 3):
            leavecredit=credits.sp_casual
        elif(types == 4):
            leavecredit=credits.earned
        elif(types == 5):
            leavecredit=credits.commuted
        elif(types == 6):
            leavecredit=credits.vacation

        if(num_of_leaves < 0 ):
            error_message="The Till Date is smaller"
        elif leavecredit < num_of_leaves:
            error_message = "you don't have enough credit to take this leave"


        if (len(error_message)!=0):
            messages.error(request, error_message)
            return redirect('/leave_module/application')
        else:
            app_obj.save()
            inbox=Inbox(ap_id=app_obj,acad_respo=0,admin_respo=0,pf_in=user,acad_res_pf=user_acad,admin_res_pf=user_admin)
            inbox.save()
            succ_mess="Your request has gone to The Respective Replacements"
            messages.success(request, succ_mess)
        return redirect('/leave_module/applications')

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

            if application.pf_in.is_staff == True:
                print('hwygadsf')
                sanction = Sanction.objects.get(department=user.department)
                user_admin = User.objects.get(name=application.admin_pf.name)
                if (sanction.sanction_cl_rh.pf == application.pf_in):
                    sanction.sanction_cl_rh = user_admin
                    sanction.save()
            else:
                dh = DepartmentHead.objects.get(department=application.pf_in.department)
                user_admin = User.objects.get(pf=application.admin_pf.pf)
                print('fadfasfadfa')
                if application.pf_in.pf == dh.hod.pf:
                    dh.temp = dh.hod
                    print('for temp')
                    print(dh.temp)
                    dh.till = application.till_date
                    print('application date')
                    print(dh.till)
                    dh.hod = user_admin
                    print(user_admin)
                    print("checkthisout")
                    print(dh.hod)
                    dh.save()

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

def rep_request(request,ap_id):
    if 'email' in request.session:
        email = request.session.get('email').encode('utf-8')
        user=User.objects.get(email=email)
        # application=Application.objects.get(pk=ap_id)
        inbox=Inbox.objects.get(ap_id=ap_id)
        if(request.POST.get('submit') == 'approve'):
            print("x")
            if (inbox.admin_res_pf.pf == user.pf):
                inbox.admin_respo=1

        elif(request.POST.get('submit') == 'reject'):
            print("y")
            if (inbox.admin_res_pf.pf == user.pf):
                inbox.admin_respo=2

        elif(request.POST.get('submit1') == 'approve'):
            print("x")
            if (inbox.acad_res_pf.pf == user.pf):
                inbox.acad_respo=1

        elif(request.POST.get('submit1') == 'reject'):
            print("y")
            if (inbox.acad_res_pf.pf == user.pf):
                inbox.acad_respo=2

        inbox.save()
        return redirect("/leave_module/inbox")
