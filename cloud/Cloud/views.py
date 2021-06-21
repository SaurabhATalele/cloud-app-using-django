from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth,User
from mycloud.models import Meta
import random,json
from . import otp


class message:
    def __init__(self):
        self.msg = ""

ms = message()

def view_404(request,exeption):
    return render(request,"404.html")

def view_500(request):
    return render(request,"404.html")    

onsignup = {'name':"root",'children':[]}
data = json.dumps(onsignup).encode("utf-8")

def home(request):
    if User.is_authenticated:
        return redirect('/u/')
    else:
        return render(request,"login.html")

def signup(request):
    msg =""
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['First_Name']
        lname = request.POST["Last_Name"]
        email = request.POST['Email']
        pass1 = request.POST['password1']
        pass2 = request.POST['confirm_pass']
        passwd =''
        if pass1 == pass2:
            passwd = pass1
        else:
            messages.info(request,"Passwords Not Matching!!!")
            return redirect( 'signup')
        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already taken!!!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.info(request,"Email already resistered!!!")
            return redirect('signup')
        user = User.objects.create_user(username=username,email=email,password=passwd,first_name = fname,last_name = lname)
        user.save()
        messages.info(request,"Registered Successfully...")
        meta = Meta()
        meta.user = username
        meta.data = data
        meta.save()

        return redirect("signup")
        
    else:
        return render(request,'signup.html',{'msg':msg})


def login(request):
    

    if request.method=='POST':
        email = request.POST['email']
        passwd = request.POST['password1']

        user = auth.authenticate(username=email,password= passwd)

        if user is not None:
            auth.login(request,user)
            return redirect("/u/")

        else:
            ms.msg = "Invalid Credentials..."
            return redirect('home_login')

    
    
    return render(request, "login.html",{'msg':ms.msg})

def logout(request):
    auth.logout(request)
    return  render(request, "login.html",{'msg':''})

def forgot_pass(request):
    if request.method == "POST":
        msg = ''
        email = request.POST["email"]
        OTP =str(random.randint(100000,999999))
        if User.objects.filter(email = email).exists():
            user = email
            msg: str ='exists'
        else:
            msg = "not exists"
            messages.info(request,msg)
            return redirect('forgot_pass')

        otp.send_otp(user,OTP,"forgot")

        messages.info(request,msg)
        print(type(messages))
        return redirect('forgot_pass')

    else:
        return render(request,'Forgot.html')

def loginmanual(request,username,password):
    user = auth.authenticate(username=username, password=password)
    msg = ''
    if user is not None:
        auth.login(request, user)
        return redirect("/u/")


    return render(request, "login.html", {'msg': msg})