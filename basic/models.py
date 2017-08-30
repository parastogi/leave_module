# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save

# from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.dispatch import receiver

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
        ('RSPC','RSPC'),
        )

    department=models.CharField(max_length=50,choices=DEPARTMENT,default="CSE")
   
    hod=models.ForeignKey(User,on_delete=models.CASCADE)
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
