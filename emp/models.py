from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class LeaveModel(models.Model):
    starting_date=models.DateField()
    no_of_days=models.IntegerField()
    reason=models.CharField(max_length=2100)
    date=models.DateTimeField(auto_now_add=True)
    isApproved =models.BooleanField(default=False)
    isRejected=models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reason


class InTimeModel(models.Model):
    in_time=models.DateTimeField(auto_now_add=True)
    ip=models.TextField()
    City=models.CharField(max_length=500,blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.user.username+" "+"on"+" "+str(self.in_time)
class OutTimeModel(models.Model):
    out_time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.user.username+" "+"on"+" "+str(self.out_time)
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.CharField(max_length=50)
    Designation=models.CharField(max_length=50)
    DateOfJoin=models.DateField(default=None)
    avatar=models.ImageField(upload_to='profile_image',blank=True)
    def __str__(self):
        return self.user.username

class production_time(models.Model):
    Production_time=models.TimeField(auto_now=False, auto_now_add=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    dateworked=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return self.user.username+" worked for "+str(self.Production_time)+str(self.dateworked)