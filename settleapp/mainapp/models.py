from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.
class Employee(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50,null=True,blank=True)
    lname = models.CharField(max_length=50,null=True,blank=True)
    designation = models.CharField(max_length=50,null=True,blank=True)
    active = models.BooleanField(default=True)
    joined_on = models.DateField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.fname,self.lname)

class AmountDistribution(models.Model):
    emp = models.ForeignKey(Employee,on_delete=models.CASCADE)
    amount = models.IntegerField(null=True,blank=True)
    created_at = models.DateField(auto_now=True)
    updates_at = models.DateField(auto_now_add=True) 
    remain_amt= models.IntegerField(null=True,blank=True)

class EmpAmountDistribution(models.Model):
    emp = models.ForeignKey(Employee,on_delete=models.CASCADE)
    emp_transtion = models.ForeignKey(AmountDistribution,null=True,blank=True,on_delete=models.SET_NULL)
    emp_amount = models.IntegerField(null=True,blank=True)
    created_at = models.DateField(auto_now=True)
    updates_at = models.DateField(auto_now_add=True) 
    emp_remain_amt= models.IntegerField(null=True,blank=True)

class ProductCosted(models.Model):
    user_emp = models.ForeignKey(Employee,on_delete=models.CASCADE)
    user_transtion = models.ForeignKey(AmountDistribution,null=True,blank=True,on_delete=models.SET_NULL)
    cost_amount = models.IntegerField(null=True,blank=True)
    created_at = models.DateField(auto_now=True)
    updates_at = models.DateField(auto_now_add=True)
    remain_amt = models.IntegerField(null=True,blank=True) 
    purchased = models.TextField(null=True,blank=True,max_length=200)
    