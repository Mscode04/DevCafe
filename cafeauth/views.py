from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserProfile,LoginTable
from cafeapp.models import MainItem
# Create your views here.

def UserRegistration(request):
    login_table=LoginTable()
    userprofile=UserProfile()
    if request.method=='POST':
        userprofile.firstname=request.POST['firstname']
        userprofile.lastname=request.POST['lastname']
        userprofile.username=request.POST['username']
        userprofile.email=request.POST['email']
        userprofile.phonenumber=request.POST['phonenumber']
        userprofile.password=request.POST['password']
        userprofile.password2=request.POST['password1']

        login_table.username=request.POST['username']
        login_table.password=request.POST['password']
        login_table.password2=request.POST['password1']
        login_table.type='user'

        if request.POST['password']==request.POST['password1']:
            userprofile.save()
            login_table.save()

            messages.info(request,'Registration Completed')
            return redirect('login')
        else:
            messages.info(request, 'password not match')
            return redirect('register')
    return render(request,'auth-form/register.html')



def LoginPage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=LoginTable.objects.filter(username=username,password=password,type='user').exists()
        try:
            if user is not None:
                user_details=LoginTable.objects.get(username=username,password=password)
                user_name=user_details.username
                type=user_details.type
                if type=='user':
                    request.session['username']=user_name
                    return redirect('user_view')

                elif type=='admin':
                    request.session['username']=user_name
                    return redirect('admin_view')

            else:
                messages.error(request,'invalid username or password')
        except :
            messages.error(request,'invalid role')
    return render(request,'auth-form/login.html')


def adminView(request):
    user_name=request.session['username']
    total_products = MainItem.objects.count()
    return render(request,'admin-temp/admin-dashbord.html', {'user_name': user_name,'total_products': total_products})

def userView(request):
    user_name = request.session['username']
    return render(request,'user-temp/user-dashbord.html',{'user_name': user_name})

def Logout(request):
    return render(request,'auth-form/login.html')


