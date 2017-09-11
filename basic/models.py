# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save

# from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.dispatch import receiver
from django.utils import timezone
import datetime

class User(models.Model):
    pf=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=250)
    DESIGNATION=(
    	('SA','Senior Assistant'),
    	('JA','Junior Assistant'),
    	('ST','Senior Technician'),
    	('JT','Junior Technician'),
    	('JE','Junior Engineer'),
    	('Driver','Driver'),
    	('JS','Junior Superintendent'),
    	('EXE','Executive Engineer (Civil)'),
    	('AR','Assistant Registrar'),
    	('DR','Deputy Registrar'),
    	('P','Professor'),
    	('AP','Assistant Professor'),
    	('AsP','Associate Professor'),
    	('RE','Research Engineer'),
    	('AP','Assistant Professor'),
    	('D','Director'),
        ('Registrar','Registrar'),
    	)
    designation=models.CharField(max_length=50,choices=DESIGNATION)
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
    department=models.CharField(max_length=50,choices=DEPARTMENT)
    is_staff=models.BooleanField(default="True")
    password=models.CharField(max_length=1000,default=123)

    def __str__(self):
        return  self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    from leavemodule.models import Leave_credits
    if created:
        print(instance.is_staff,instance.name)
        if instance.is_staff is True:
            Leave_credits.objects.create(pf=instance, casual=8, restricted=2, sp_casual=10 , earned=30,commuted=20,vacation=0)
        else:
            Leave_credits.objects.create(pf=instance, casual=8, restricted=2, sp_casual=10 , earned=0,commuted=20,vacation=60)


class DepartmentHead(models.Model):
    department=models.CharField(max_length=50)
    hod=models.ForeignKey(User,on_delete=models.CASCADE,related_name='hod')
    temp=models.ForeignKey(User,on_delete=models.CASCADE,related_name='temp',null=True)
    till=models.DateField()
    from_d=models.DateField(null=True)

# from django.dispatch import receiver
#
# class User_profile:
#         @receiver(post_save, sender=User)
# 	def create_user_profile(sender, instance, created, **kwargs):
# 		if created:
# 			Person.objects.create(username = instance)
#
# 	@receiver(post_save, sender=User)
# 	def save_user_profile(sender, instance, **kwargs):
# 		instance.person.save()
