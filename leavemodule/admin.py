# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from basic.models import User,DepartmentHead
from .models import Application, Leave_credits, Sanction, Inbox

class SanctionAdmin(admin.ModelAdmin):
    model = Sanction

    fieldsets = [
        (None,{'fields': ['department']}),
        (None, {'fields': ['sanction_cl_rh']}),
        (None, {'fields': ['sanction_others']})
    ]
    list_display = ('department', 'sanction_cl_rh','sanction_others')

# class InboxAdmin(admin.ModelAdmin):
#     model = Inbox
#
#     fieldsets = [
#         (None,{'fields': ['pf_sender']}),
#         (None, {'fields': ['pf_reciever']}),
#         (None, {'fields': ['response']}),
#         (None, {'fields': ['date']}),
#     ]
#     list_display = ('pf_sender', 'pf_reciever','response','date')

class Leave_creditsAdmin(admin.ModelAdmin):
    model = Leave_credits

    fieldsets = [
        (None,{'fields': ['pf']}),
        (None, {'fields': ['casual']}),
        (None, {'fields': ['restricted']}),
        (None, {'fields': ['sp_casual']}),
        (None, {'fields': ['earned']}),
        (None, {'fields': ['commuted']}),
        (None, {'fields': ['vacation']}),
        (None, {'fields': ['year']}),
    ]
    list_display = ('pf', 'casual','restricted','sp_casual','earned','commuted','vacation','year')

class DepartmentHeadAdmin(admin.ModelAdmin):
    model = DepartmentHead

    fieldsets = [
        (None,{'fields': ['department']}),
        (None, {'fields': ['hod']}),
        (None, {'fields': ['temp']}),
        (None, {'fields': ['till']}),
        (None, {'fields': ['from_d']}),

    ]
    list_display = ('department', 'hod', 'temp','till','from_d')

class UserAdmin(admin.ModelAdmin):
    model = User

    fieldsets = [
        (None,{'fields': ['pf']}),
        (None, {'fields': ['name']}),
        (None, {'fields': ['email']}),
        (None, {'fields': ['designation']}),
        (None, {'fields': ['department']}),
        (None, {'fields': ['is_staff']}),
    ]
    list_display = ('pf', 'name','email','designation','department','is_staff')
class ApplicationAdmin(admin.ModelAdmin):
    model = Application

    fieldsets = [
        (None,{'fields': ['pf_in']}),
        (None, {'fields': ['pf_out']}),
        (None, {'fields': ['type_of_leave']}),
        (None, {'fields': ['from_date']}),
        (None, {'fields': ['till_date']}),
        (None, {'fields': ['address']}),
        (None, {'fields': ['purpose']}),
        (None, {'fields': ['acad_pf']}),
        (None, {'fields': ['admin_pf']}),
        (None, {'fields': ['date_of_app']}),
        (None, {'fields': ['is_station']}),
        (None, {'fields': ['status']}),
        (None, {'fields': ['remarks']}),

    ]
    list_display = ('pf_in','pf_out','type_of_leave','from_date','till_date','address','purpose','acad_pf','admin_pf','date_of_app','is_station')






admin.site.register(User, UserAdmin),
admin.site.register(DepartmentHead, DepartmentHeadAdmin),
admin.site.register(Application, ApplicationAdmin),
admin.site.register(Leave_credits,Leave_creditsAdmin),
admin.site.register(Sanction, SanctionAdmin),
admin.site.register(Inbox)
