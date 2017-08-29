# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from basic.models import User,DepartmentHead
from .models import Application, Leave_credits, Sanction, Inbox

# Register your models here.
admin.site.register(User),
admin.site.register(Application),
admin.site.register(Leave_credits),
admin.site.register(Sanction),
admin.site.register(Inbox),
admin.site.register(DepartmentHead)
