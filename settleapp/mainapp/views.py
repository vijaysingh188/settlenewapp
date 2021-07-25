from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View,TemplateView
from mainapp.models import *
from .forms import UserLoginForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class Home(TemplateView):
    def get(self, request):
        form = AuthenticationForm(request.POST or None)
        data_response={
           "form":form,
        }
        return render(request, "index.html",data_response)

    def post(self,request):
        form = AuthenticationForm(request.POST or None)    
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("DataAnalysis")
        else:
            return redirect("Home")
    
        data_response={
           "form":form,
        }

        return render(request, "index.html",data_response)

class DataAnalysis(TemplateView):
    def get(self,request,*args,**kwargs):
        data_map = {}
        data_list = []
        if request.user.is_superuser:
            print("yes")
            data_map['alluser'] = Employee.objects.values("id","fname","lname")
            data_map['allemp'] = AmountDistribution.objects.values("emp__fname","emp__lname","amount","created_at","emp__id","remain_amt")

            list_of_emp= list(Employee.objects.values_list("id",flat=True))
            print(list_of_emp,'list_of_emp')

            

            for emp in list_of_emp:
                get_id  = Employee.objects.get(id=emp)
                allemp = ProductCosted.objects.filter(user_emp=get_id).values("user_emp__fname","user_emp__lname","user_transtion","cost_amount","created_at","purchased")
                data_list.append(allemp)
            print(data_list,'********88data_list')




        else:
            get_id = User.objects.get(id=request.user.id)
            get_data = Employee.objects.get(user=get_id).id        
            data_map['get_emp_data'] = list(AmountDistribution.objects.filter(emp=get_data).values())[0]
            if ProductCosted.objects.filter(user_emp=get_data).exists:
                data_map['individualremaining'] = list(ProductCosted.objects.filter(user_emp=get_data).values())


        data_response={
            "data_map":data_map,
            'data_list':data_list
        }
        return render(request, "settleapp.html",data_response)

    def post(self,request):
        data_map = {}
        if "saveemp" in request.POST:
            employee = request.POST.get("employee")
            amount = request.POST.get("amount")
            print(employee)
            print(amount)
            get_id = Employee.objects.get(id=employee)
            if AmountDistribution.objects.filter(emp=get_id).exists():
                realamt  = AmountDistribution.objects.get(emp=get_id).amount
                prevamt  = AmountDistribution.objects.get(emp=get_id).remain_amt
                print(realamt,prevamt)
                amttoincrease = int(prevamt) + int(amount)
                print(amttoincrease)
                object_update = AmountDistribution.objects.filter(emp=get_id).update(amount=amount, remain_amt=amttoincrease)#,
            else:
                object_creation = AmountDistribution.objects.create(emp=get_id,amount=amount,remain_amt=amount)
        if "empproduct" in request.POST:
            purchaseamount = request.POST.get("purchaseamount")
            product = request.POST.get("product")
            mydate = request.POST.get("mydate")      
            hiddenpreviousamt = request.POST.get("hiddenpreviousamt")
            get_id = User.objects.get(id=request.user.id)
            get_data = Employee.objects.get(user=get_id)
            get_foreign = AmountDistribution.objects.get(emp=get_data)
            get_previousdata = AmountDistribution.objects.get(emp=get_data).remain_amt
            calculated_amt = int(get_previousdata) - int(purchaseamount)
            object_creation =ProductCosted.objects.create(user_emp=get_data,user_transtion=get_foreign,cost_amount=purchaseamount,purchased=product,created_at=mydate,remain_amt=calculated_amt)
        if request.user.is_superuser:
            print("yes")
            data_map['alluser'] = Employee.objects.values("id","fname","lname")
            data_map['allemp'] = AmountDistribution.objects.values("emp__fname","emp__lname","amount","created_at","emp__id","remain_amt")

        else:
            get_id = User.objects.get(id=request.user.id)
            get_data = Employee.objects.get(user=get_id).id
            data_map['get_emp_data'] = list(AmountDistribution.objects.filter(emp=get_data).values())[0]
            if ProductCosted.objects.filter(user_emp=get_data).exists:
                data_map['individualremaining'] = list(ProductCosted.objects.filter(user_emp=get_data).values())
       
        data_response={

            "data_map":data_map,
        }
        return render(request, "settleapp.html",data_response)

        
