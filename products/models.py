
from django.db import models
from django.db.models import CharField, Case, Value, When
from django.contrib.auth.models import AbstractUser
# Create your models here.
# class Product(models.Model):
# 	title 			= models.CharField(max_length=50, default='',)

# 	description 	= models.TextField()

# 	deadline 		= models.DateField()

from django.contrib.auth.models import User
import os
from datetime import datetime

from django.utils import timezone
from django.conf import settings

class User(AbstractUser):
    is_DEVELOPER = models.BooleanField(default=False)
    is_PRODUCT_OWNER = models.BooleanField(default=False)
    is_SCRUM_MASTER = models.BooleanField(default=False)
    is_project = models.BooleanField(default=False)
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    scrum_master = models.CharField(max_length=200)
    SPRINT_CHOICES = [
        ('START', 'start'),
        ('FINISH', 'finish'),
        ('NOT_YET_START', 'Not yet start'),
    ]
    sprint_status = models.CharField(max_length=200,choices=SPRINT_CHOICES,default='NOT_YET_START')

    def __str__(self):
        return self.name

    def sprintreturn(self):
        return self.sprint_status




class PBI(models.Model):
    #product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    priority = models.PositiveIntegerField()
    description = models.TextField(max_length=1000, null=True)
    story_point = models.PositiveIntegerField()
    cumulative_story_point = models.PositiveIntegerField(default=0, editable=False)
    STATUS_CHOICES = [
        ('DONE', 'Done'),
        ('IN_PROCESSING', 'In process'),
        ('NOT_YET_START', 'Not yet start'),
        ('UNFINISHED', 'Unfinished')
    ]
    status = models.CharField(max_length=200,choices=STATUS_CHOICES,default='NOT_YET_START')
    in_sprint = models.BooleanField(default=False)
    total_effort_hours = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return "/viewPBI/"

    def save(self, *args, **kwargs):
        object1 = Product.objects.get(pk=1)
        sprintSTAT = object1.sprintreturn()
        #print(sprintSTAT)
        if self.status != 'DONE':
            if self.in_sprint == True:
                self.status = 'IN_PROCESSING'
            elif self.in_sprint == False:
                if sprintSTAT == 'FINISH':
                    self.status = 'UNFINISHED'
                elif sprintSTAT == 'NOT_YET_START':
                    self.status = 'NOT_YET_START'
        super(PBI, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class Task(models.Model):
    pbi = models.ForeignKey(PBI, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    hour = models.PositiveIntegerField()
    #owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    owner = models.CharField(max_length=200, blank=True)

    STATUS_CHOICES = [
        ('DONE', 'Done'),
        ('IN_PROCESSING', 'In process'),
        ('NOT_YET_START', 'Not yet start')
    ]
    status = models.CharField(max_length=200,choices=STATUS_CHOICES,default='NOT_YET_START')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        #if not self.id:
    #        self.name = self.user.first_name + self.user.last_name
    #    super(Task, self).save(*args, **kwargs)
        if self.owner != '' and self.status != 'DONE':
            self.status = 'IN_PROCESSING'
        super(Task, self).save(*args, **kwargs)
