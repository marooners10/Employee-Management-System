from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse
from django.http import HttpResponseNotFound
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q #use to indicate of 'and', 'or' for more than 1 condition

# Create your views here.

def index(request):
    return render(request, 'index.html')

    

def all_emp(request):
    emps=Employee.objects.all()#to view all items in model where Employee is model name
    context={
        'emps': emps
    }
    print(context)
    
    return render(request, 'view_all_emp.html', context)#to transfer all the context to view_all_emp.html page

    
    
    

def add_emp(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        salary=int(request.POST['salary'])
        bonus=int(request.POST['bonus'])
        phone=int(request.POST['phone'])
        dept=int(request.POST['dept'])
        role=int(request.POST['role'])

        try:
            department = Department.objects.get(pk=dept)
            role = Role.objects.get(pk=role)
        except Department.DoesNotExist:
            return HttpResponseNotFound('Department with ID {} does not exist'.format(dept))
        except Role.DoesNotExist:
            return HttpResponseNotFound('Role with ID {} does not exist'.format(role))


        new_emp=Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id=dept, role_id=role.id, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse("Employee Added Successfully!") 

    elif request.method== 'GET':
        return render(request, 'add_emp.html')

    else:
        return HttpResponse('An Exception Occured!, Employee Has Not Been Added')

        
        
        

def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed=Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse ('Employee Deleted Successfully')
        except:
            return HttpResponse('Please, Enter A Valid Employee ID')
    emps=Employee.objects.all()#to view all items in model where Employee is model name
    context={
        'emps':emps
    }
    return render(request, 'remove_emp.html', context)#to transfer all the context to remove_emp.html page

    
    
    
    
    
    

def filter_emp(request):
    if request.method == 'POST':
        name=request.POST['name']
        dept=request.POST['dept']
        role=request.POST['role']
        emps=Employee.objects.all()

        if name:
            emps=emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))#icontains: i is use for case sensative and contains is use to show full name even with half word

        if dept:
            emps=emps.filter(dept__name__icontains=dept)
        
        if role: 
            emps=emps.filter(role__name__icontains=role)
            
        context = {
           "emps":  emps
        }
        return render(request, 'view_all_emp.html', context)#displays the detail of filtered content in view_all_emp.html
        
    elif request.method== 'GET':
        return render(request, 'filter_emp.html')

    else:
        return HttpResponse('An Exception Occured!, Employee Has Not Been Added')
