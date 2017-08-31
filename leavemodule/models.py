# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from basic.models import User

# Create your models here.
class Leave_credits(models.Model):
    pf=models.ForeignKey(User, on_delete=models.CASCADE)
    casual=models.IntegerField()
    restricted=models.IntegerField()
    sp_casual=models.IntegerField()
    earned=models.IntegerField()
    commuted=models.IntegerField()
    vacation=models.IntegerField()

    def __str__(self):
        return self.pf.name

class Application(models.Model):
    from datetime import datetime
    
    pf_in=models.IntegerField()
    pf_out=models.IntegerField()
    type_of_leave=models.IntegerField()
    from_date=models.DateField()
    till_date=models.DateField()
    acad_pf=models.ForeignKey(User,on_delete=models.CASCADE,related_name='acad_pf')
    admin_pf=models.ForeignKey(User,on_delete=models.CASCADE,related_name='adin_pf')
    address=models.CharField(max_length=500)
    purpose=models.CharField(max_length=500)
    date_of_app=models.DateField()
    is_station=models.BooleanField(default="false")
    st_from_date=models.DateField(null=True, blank=True)
    st_till_date=models.DateField(null=True, blank=True)
    status=models.IntegerField()
    remarks=models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.pk)


class Sanction(models.Model):
    DEPARTMENT = (
        ('FA','Finance and Accounts'),
        ('EST','Establishment'),
        ('Academics','Academics'),
        ('CC','Computer Center'),
        ('ECE','ECE'),
        ('CSE','CSE'),
        ('ME','ME'),
        ('Design','Design'),
        ('Mechatronics','Mechatronics'),
        ('NS','Natural Science'),
        ('PC','Placement Cell'),
        ('IWD','IWD'),
        ('R&D','Office of The Dean R&D'),
        ('Directorate','Directorate'),
        ('Library','Library'),
        ('P&D','Office of The Dean P&D'),
        ('Student Affairs','Student Affairs'),
        ('GA','General Administration'),
        ('RO','Registrar Office'),
        ('PS','Purchase and Store'),
        ('Workshop','Workshop'),
        ('EST-PS','Establishment & P&S'),
        ('FA-GA','F&A & GA'),
        ('Security','Security and Central Mess'),
        ('RTI','Establishment, RTI and Rajbhasha'),

        )
    department=models.CharField(max_length=50)
    sanction_cl_rh=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cl_rh')
    sanction_others=models.ForeignKey(User,on_delete=models.CASCADE,related_name='others')

class Inbox(models.Model):
    pf_sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='pf_sender')
    pf_reciever=models.ForeignKey(User,on_delete=models.CASCADE,related_name='pf_reciever')
    response=models.CharField(max_length=200)
    date=models.DateTimeField()

    def __str__(self):
        return "receiver="+str(self.pf_reciever.pk)+"  "+"sender="+str(self.pf_sender.pk)
