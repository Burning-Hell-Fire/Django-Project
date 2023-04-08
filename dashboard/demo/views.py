import csv
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Data
# Create your views here.
def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if pass1!=pass2:
            messages.error(request, 'Passwords do not match!!')
            return render(request, 'signup.html')
        try:
            myuser = User.objects.create_user (username,email, pass1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            messages.success(request,"Your account has been created!!")
        except:
            messages.error(request, 'Error occured!!Please try again!! ')
            return render(request, 'signup.html')
        return redirect('signin')
    return render(request,'signup.html')
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        pass1=request.POST['pass1']
        user= authenticate(username=username, password=pass1)
        if user is not None:
            login(request,user)
            fname=user.first_name
            lname=user.last_name
            return render(request, 'dashboard.html', {'fname':fname, 'lname':lname})
        else:
            messages.error(request,'Bad credentials!!')
            return render(request, 'signin.html')
    return render(request,'signin.html')
def signout(request):
    logout(request)
    messages.success(request,"Logout Successfull!!")
    return redirect('home')

def add_data(request):
    if request.method=='POST':
        name=request.POST['name']
        age=request.POST['age']
        dob=request.POST['dob']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        phone=request.POST['phone']
        try:
            data=Data(user=request.user, name=name,age=age,dob=dob,city=city,state=state,country=country,phone_number=phone)
            data.save()
        except:
            messages.error(request, "Error Occured!! Try again!!")
        data=User.objects.get(username=request.user)
        return render(request, 'dashboard.html', {'fname':data.first_name} )
    return render(request, 'index.html')

def delete(request):
    if request.method=='POST':
        name=request.POST['name']
        data=Data.objects.get(user=request.user, name=name)
        data.delete()
        data=User.objects.get(username=request.user)
        return render(request, 'dashboard.html',{'fname':data.first_name} )
    
    return render(request, 'index.html', )

def filter_data(request):
    if request.method == 'POST':
        search_field = request.POST['search_field']
        search_query = request.POST['search_query']

        # Filter objects based on the search parameters
        if search_field == 'dob':
            filtered_objects = Data.objects.filter(user=request.user,dob=search_query)
        elif search_field == 'city':
            filtered_objects = Data.objects.filter(user=request.user,city__icontains=search_query)
        elif search_field == 'state':
            filtered_objects = Data.objects.filter(user=request.user,state__icontains=search_query)
        elif search_field == 'country':
            filtered_objects = Data.objects.filter(user=request.user,country__icontains=search_query)
        else:
            filtered_objects = Data.objects.none()  # Return an empty queryset if the search field is invalid
        data=User.objects.get(username=request.user)
        # Render the search results template with the filtered objects and search parameters
        return render(request, 'dashboard.html', {'fname':data.first_name ,'objects': filtered_objects, 'search_field': search_field, 'search_query': search_query})
def download(request):
    if request.method=='POST':
        #name=request.POST['name']
        data=Data.objects.filter(user=request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        writer = csv.writer(response)
        writer.writerow(['name', 'age', 'dob', 'city','state','country','phone'])
        for item in data:
            writer.writerow([item.name, item.age, item.dob, item.city, item.state,item.country,item.phone_number])
        return response
