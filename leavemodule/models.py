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
    year=models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.pf.name

class Application(models.Model):
    from datetime import datetime

    pf_in=models.ForeignKey(User,on_delete=models.CASCADE,related_name='pf_in',null=True)
    pf_out=models.IntegerField()
    type_of_leave=models.IntegerField()
    from_date=models.DateField()
    till_date=models.DateField()
    acad_pf=models.ForeignKey(User,on_delete=models.CASCADE,related_name='acad_pf')
    admin_pf=models.ForeignKey(User,on_delete=models.CASCADE,related_name='adin_pf')
    address=models.CharField(max_length=500, null=True)
    purpose=models.CharField(max_length=500)
    date_of_app=models.DateField()
    is_station=models.BooleanField(default="false")
    st_from_date=models.DateField(null=True, blank=True)
    st_till_date=models.DateField(null=True, blank=True)
    status=models.IntegerField()
    remarks=models.CharField(max_length=100, null=True)
    # inbox_id=models.ForeignKey(Inbox,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.pk)


class Sanction(models.Model):
    DEPARTMENT = (
    	('Finance and Accounts','Finance and Accounts'),
    	('Establishment','Establishment'),
    	('Academics','Academics'),
    	('Computer Center','Computer Center'),
    	('ECE','ECE'),
    	('CSE','CSE'),
    	('ME','ME'),
    	('Design','Design'),
    	('Mechatronics','Mechatronics'),
    	('Natural Science','Natural Science'),
    	('Placement Cell','Placement Cell'),
    	('IWD','IWD'),
    	('Office of The Dean R&D','Office of The Dean R&D'),
    	('Directorate','Directorate'),
    	('Library','Library'),
    	('Office of The Dean P&D','Office of The Dean P&D'),
    	('Student Affairs','Student Affairs'),
    	('General Administration','General Administration'),
    	('Registrar Office','Registrar Office'),
    	('Purchase and Store','Purchase and Store'),
    	('Workshop','Workshop'),
    	('Establishment & P&S','Establishment & P&S'),
    	('F&A & GA','F&A & GA'),
    	('Security and Central Mess','Security and Central Mess'),
    	('Establishment, RTI and Rajbhasha','Establishment, RTI and Rajbhasha'),
        ('Registrar Office','Registrar Office'),
    	)
    department=models.CharField(max_length=50)
    sanction_cl_rh=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cl_rh')
    sanction_others=models.ForeignKey(User,on_delete=models.CASCADE,related_name='others')

class Inbox(models.Model):
    acad_respo=models.IntegerField(default=0)
    admin_respo=models.IntegerField(default=0)
    acad_res_pf=models.ForeignKey(User,on_delete=models.CASCADE,related_name='acad_res_pf',null=True)
    admin_res_pf=models.ForeignKey(User,on_delete=models.CASCADE,related_name='admin_res_pf',null=True)
    ap_id=models.ForeignKey(Application,on_delete=models.CASCADE,null=True)
    pf_in=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    # def __str__(self):
    #     return "receiver="+str(self.pf_reciever.pk)+"sender="+str(self.pf_sender.pk)
