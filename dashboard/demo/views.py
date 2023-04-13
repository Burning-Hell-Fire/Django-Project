import csv
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from dashboard import settings
from .models import Data,Image
# Create your views here.
def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists! Try again!!')
            return render(request, 'signup.html')
        fname=request.POST['fname']
        lname=request.POST['lname']
        for i in (fname+lname):
            if i not in 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                messages.error(request, 'Name contain only alphabets!!')
                return render(request, 'signup.html')
        email=request.POST['email']
        if '@' not in email and '.com' not in email:
            messages.error(request, 'Enter a valid email address!!')
            return render(request, 'signup.html')
        if User.objects.filter(email=email):
            messages.error(request, 'Email already exists! Try again!!')
            return render(request, 'signup.html')
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if pass1!=pass2:
            messages.error(request, 'Passwords do not match!!')
            return render(request, 'signup.html')
        try:
            myuser = User.objects.create_user (username,email, pass1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.is_active = False
            myuser.save()
        except:
            messages.error(request, 'Error occured!!Please try again!! ')
            return render(request, 'signup.html')
        try:
            subject = 'Activate Your Account'
            message = 'Hi '+ fname +' '+lname+'!!'+'\n\n\nThis is an email regariding the email verification of your account at Employee Management System.\n\n\nWe welcome you onboard and wish you have an wonderful experience using our system.\n\n\nPlease click the link to activate your account: http://{}/activate/{}'.format(request.get_host(), myuser.pk)
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [myuser.email,]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request,"Your account has been created!! Please verify your email!!")
        except:
            messages.error(request, 'Error occured during email verification!!')
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
        data1=User.objects.get(username=request.user)
        for i in name:
            if i not in 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                messages.error(request, 'Name contain only alphabets!!')
                return render(request, 'dashboard.html', {'fname':data1.first_name} )
        age=request.POST['age']
        for i in age:
            if i not in '0123456789':
                messages.error(request, 'Age must contain numbers!!')
                return render(request, 'dashboard.html', {'fname':data1.first_name} )
        if int(age)<5 or int(age)>90:
            messages.error(request, 'Age should be between 5 and 90!!')
            return render(request, 'dashboard.html', {'fname':data1.first_name} )
        dob=request.POST['dob']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        for i in (city+state+country):
            if i not in 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                messages.error(request, 'Places contain only alphabets!!')
                return render(request, 'dashboard.html', {'fname':data1.first_name} )
        phone=request.POST['phone']
        if len(phone)!=10:
            messages.error(request, 'Mobile Number must contain 10 digits!!')
            return render(request, 'dashboard.html', {'fname':data1.first_name} )
        for i in phone:
            if i not in '0123456789':
                messages.error(request, 'Mobile Number should contain numbers!!')
                return render(request, 'dashboard.html', {'fname':data1.first_name} )
        try:
            data=Data(user=request.user, name=name,age=age,dob=dob,city=city,state=state,country=country,phone_number=phone)
            data.save()
        except:
            messages.error(request, "Error Occured!! Try again!!")
        return render(request, 'dashboard.html', {'fname':data1.first_name} )
    return render(request, 'index.html')

def delete(request):
    if request.method=='POST':
        name=request.POST['name']
        try:
            data=Data.objects.get(user=request.user, name=name)
            data.delete()
        except:
            messages.error(request, 'Name not present in the database!!')
            return render(request, 'dashboard.html',{'fname':data.first_name} )
        data=User.objects.get(username=request.user)
        return render(request, 'dashboard.html',{'fname':data.first_name} )
    
    return render(request, 'index.html' )

def filter_data(request):
    if request.method == 'POST':
        search_field = request.POST['search_field']
        search_query = request.POST['search_query']
        data=User.objects.get(username=request.user)
        # Filter objects based on the search parameters
        try:
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
        except:
            messages.error(request, 'Check for a valid entry!!')
            return render(request,'dashboard.html',{'fname':data.first_name})
        # Render the search results template with the filtered objects and search parameters
        return render(request, 'dashboard.html', {'fname':data.first_name ,'objects': filtered_objects, 'search_field': search_field, 'search_query': search_query})
def download(request):
    if request.method=='POST':
        data=Data.objects.filter(user=request.user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        writer = csv.writer(response)
        writer.writerow(['name', 'age', 'dob', 'city','state','country','phone'])
        for item in data:
            writer.writerow([item.name, item.age, item.dob, item.city, item.state,item.country,item.phone_number])
        return response
def activate_account(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        return redirect('signin')
    user.is_active = True
    user.save()
    login(request, user)
    return redirect('home')
def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')
def image_upload(request):
    if request.method=='POST':
        img=request.FILES['image']
        data1=User.objects.get(username=request.user)
        try:
            data=Image(user=request.user, image=img)
            data.save()
            messages.success(request,'Image upload successfull!!')
        except:
            messages.error(request, 'Error occured while uploading image!!')
        return render(request, 'dashboard.html',{'fname':data1.first_name})
    return render(request,'index.html')
def image_view(request):
    if request.method=='POST':
        data=User.objects.get(username=request.user)
        try:
            img=Image.objects.get(user=request.user)
        except:
            messages.error(request,'Error occured while downloading image!!')
            return render(request, 'dashboard.html',{'fname':data.first_name})
        return render(request, 'dashboard.html', {'fname':data.first_name ,'image':'/media/'+str(img.image)})
    return render(request, 'index.html')