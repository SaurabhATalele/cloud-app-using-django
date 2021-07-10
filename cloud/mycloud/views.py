from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import render,redirect
import pyodbc,math,json,datetime,os,requests,razorpay

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,FileResponse
from .models import Meta,devs,projects,slaves, storage
from . import space_avl_client as c 
from . import SaveClient as sc
from .payments import client
from . import dirs,dfc,rfc,Deleter
from django.contrib.auth.models import auth,User



# Create your views here.
from django.template import loader


# _________________________________________________________________________
#                               connection and cursor object
# _________________________________________________________________________

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-P3BU85V\MSSQLSERVER01;DATABASE=mycloud_db;UID=saurabh;PWD=saurabh@123')
cnxn.autocommit=True
cursor = cnxn.cursor()




hosts = [] #file hosts connected______________________________

s = slaves.objects.all()
for slave in s:
    hosts.append(slave.address)



columns = []
datalist = []
Data =[]
query=""

output = "Query Executed Successfully..."



# _________________________________________________________________________
#                               Error handlers
# _________________________________________________________________________
def view_404(request,exeption):
    return render(request,"404.html")

def view_500(request):
    return render(request,"404.html") 

# _________________________________________________________________________
#                               methods for views
# _________________________________________________________________________


def storage_usage(request):
    size = 0
    data = []
    owner = request.user.username
    password = devs.objects.filter(username=owner).values_list('user_password',flat=True)
    for s in password:
        password1 = s
    password2 = password1.decode("utf-8")
        
    con = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-P3BU85V\MSSQLSERVER01;DATABASE=master;UID="+owner+";PWD="+password2)
    con.autocommit=True
    cur = con.cursor()
    table = cur.execute("exec sp_databases")
    for d in table:
        for dat in d:
            b = dat
            data.append(dat)
        size += int(data[1])
        data = []
    cur.close()
    con.close()
    meta1 = Meta.objects.filter(user=request.user.username).values_list('id', flat=True)
    for s in meta1:
        size = size + int(s)
    total = convert_size(size)
    return [total,size]

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def check_hosts(size,h):

    for host in hosts:
        if host == h:
            continue
        else:
            if c.Check_space(host,size):
                return host
    return False

# _______________________________________________________________________
#                           files class
# _______________________________________________________________________
class fsc:
    def __init__(self) -> None:
        self.fs = dirs.fs({'name':"root",'children':[]})

class msg:
    def __init__(self)->None:
        self.msg = ""      

fsco = fsc()
message = msg()
errormsg = ""


    # ____________________________________________________________________________
    #                               views here 
    # ____________________________________________________________________________
class view:
    fs = dirs.fs({"name":'root','children':[]}) #Fs obj____________________________
    

    
    @login_required
    def home(request):
        
        data={}

        meta = Meta.objects.filter(user = request.user.username)
        meta = meta.values_list('data',flat=True)
        for a in meta:
            d = a.decode("utf-8")
            data = json.loads(d)
        if fsco.fs.cur_dir == "root":
            fsco.fs = dirs.fs(data) 

        print(hosts)
        folders = fsco.fs.folders('')
        
        files = fsco.fs.files(".")

        cur_dir = fsco.fs.cur_dir
        path = cur_dir.split("/")
        #['root','new folder']
        

 
        return render(request,'Home.html',{'files' :files,'folders':folders,'path':path,'errormsg':errormsg})



    # _____________________________________________________________________
    #                               The profile page
    # _____________________________________________________________________


    @login_required
    def profile(request):   
        try: 
            st = storage.objects.get(user = request.user.username)
            if st != None:
                limit = 10
        except:
            limit = 5
        a = fsco.fs.cur_dir_items                       
        
        total = convert_size(fsco.fs.storage_used())
        return render(request, 'profile.html',{'used':total,"limit":limit})



    # ___________________________________________________________________________
    #                               Search for the file 
    # ___________________________________________________________________________
    @login_required
    def search(request):
        data1 = []
        data = request.POST['Search']
        files = fsco.fs.files(data)
        folders =fsco.fs.folders(data)
        cur_dir = fsco.fs.cur_dir
        path = cur_dir.split("/")
                    
        return render(request,'Home.html',{'files' :files,'folders':folders,'path':path})


    # _______________________________________________________________________________
    #                               Edit profile page
    # _______________________________________________________________________________

    @login_required()
    def editProfile(request):
        
        return render(request,"EditProfile.html",{"msg":message.msg})

 # ________________________________________________________________________________
 #                               creating folder
 # ________________________________________________________________________________

    @login_required()
    def create_folder(request):
        if request.method == 'POST':
            fname = request.POST['foldername']
            user = request.user.username
            meta = Meta.objects.get(user=request.user.username)
            fsco.fs.add_item(fname,"dir")
            dat = fsco.fs.data()
                
            data = json.dumps(dat).encode('utf-8')
            meta.data = data
            meta.save(update_fields=["data"])
        return redirect('home')


    # _______________________________________________________________________________
    #                                uploading new file
    # _______________________________________________________________________________
    @login_required()
    @csrf_exempt
    def upload(request):
        file = ''
        file_data = b''
        host1= ""
        host2 = ""
        lim = 0

        try:
            st = storage.objects.get(user = request.user.username)
            lim = 10737418240
        except:
            lim = 5368709120

        free = lim-fsco.fs.storage_used()



        if  'file1' in request.FILES:

            file = request.FILES['file1']
            uname = request.user.username
            file_name = str(file)
            file_data = file.read()

            if free < file.size:
                for i in range(2):
                    checked =""
                    if i == 0:
                        checked = check_hosts(file.size,"")
                        host1 = sc.save(uname,file_name,file.size,file_data,checked)
                    else:
                        checked2 = check_hosts(file.size,checked)
                        host2 = sc.save(uname,file_name,file.size,file_data,checked2)
                
                if checked != False:
                    
                    
                    meta = Meta.objects.get(user=request.user.username)
                    
                    t = file_name.split('.')
                    type = t[-1]
                    fsco.fs.add_item(file_name,type,file.size,host1,host2)
                    dat = fsco.fs.data()
                    
                    data = json.dumps(dat).encode('utf-8')
                    meta.data = data

                    # meta.host = Uploaded_details[2]
                    # meta.loc = Uploaded_details[1]
                    # meta.filename = file_name
                    # meta.filesize = file.size
                    # meta.date_created = date_today
                    meta.save(update_fields=['data'])
            
            else:
                return redirect("home")

        data = 'http://127.0.0.1:5500/saurabh/'

        return HttpResponse(data)


    # _________________________________________________________________________
    #                               deleting the file
    # __________________________________________________________________________
    def delete(request,filename):
        host = ""
        h2 = ''
        curdir= fsco.fs.cur_dir.split('/')
        curdir.pop(0)
        curdiritem = []
        for item in fsco.fs.cur_dir_items:
            if item['name'] == filename:
                try:
                    if item['host']:
                        host = item['host']
                        h2 = item['host2']
                except:
                    pass
        
        if filename.__contains__("."):
            errormsg = dfc.deletefile(request.user.username,filename,host)
            errormsg = dfc.deletefile(request.user.username,filename,h2)
            if errormsg == "100":
                errormsg = "File/Folder deleted Successfully..."
            else:
                errormsg = "File/Folder cannot be deleted"
            fsco.fs.remove_item(filename)
        else:
            
            Deleter.deleter(request.user.username,fsco.fs.cur_dir_items,filename)
            fsco.fs.remove_item(filename)
       
          
        meta = Meta.objects.get(user=request.user.username)
        dat = fsco.fs.data()
            
        data = json.dumps(dat).encode('utf-8')
        meta.data = data
        
         
        meta.save(update_fields=['data'])
        print("gone")
        return redirect("home")


 # _________________________________________________________________________
    #                               Updating user details
    # __________________________________________________________________________

    def edit_Profile(request,username):
        
        user = username
        u = User.objects.get(username=user)
        print(message.msg)
        if request.method == "POST":
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            email = request.POST["address"]
            username = request.POST["username"]
            if not username == request.user.username:
                if User.objects.filter(username = username).exists():
                    message.msg = "username already Exists..."
                    return redirect('edit')
            
            oldpass = request.POST["oldpass"]
            if oldpass != "":
                user = auth.authenticate(username = user,password = oldpass)
                if user is not None:
                    newpass = request.POST["newpass"]
                    conpass = request.POST['conpass']
                    if newpass == conpass:
                        u.set_password(newpass)
                        
                        message.msg = 'Password Changed Successfully...'
                    else:
                        message.msg = "Passwords don't match..."
                        return redirect("edit")
                
                else:
                    message.msg = "Old password is wrong..."

            #changing username for metadata
            meta = Meta.objects.get(user = request.user.username)
            meta.user = username
            meta.save()

            #updating user details
            u.first_name = fname
            u.last_name = lname
            u.username = username
            u.email = email
            u.save()

            
        return redirect("edit")

         # _________________________________________________________________________
    #                               renaming the file
    # __________________________________________________________________________

    def renamefile(request,filename,newname):
        host = ''
        h2 = ''
        newname = newname

        if request.method == "POST":
            print("post")
            newname = request.GET['filenew']
        for item in fsco.fs.cur_dir_items:
            if item['name']==filename:
                if item['type'] == "dir":
                    item['name']= newname
                
                else:
                    if item['host']:
                        host = item['host']
                        h2 = item['host2']

                    msg = rfc.renamefile(request.user.username,filename,newname,host)
                    msg = rfc.renamefile(request.user.username,filename,newname,h2)
                    
                    if msg == "100":
                        item['name'] = newname

        meta = Meta.objects.get(user=request.user.username)
        dat = fsco.fs.data()
            
        data = json.dumps(dat).encode('utf-8')
        meta.data = data
        
         
        meta.save(update_fields=['data'])
               
        return redirect("home")

    # _________________________________________________________________________
    #                               acccessing the file
    # __________________________________________________________________________

    def file(request,filename):
        host =''
        type = ''
        h2 = ""
        name = ''
        date_created= ''
        size = 0
        filename = filename
        items = fsco.fs.cur_dir_items
        for item in items:
            if item['name'] == filename:
                host = item['host']
                type = item['type']
                name = item['name']
                size = convert_size(item['size'])
                date_created = item['date_created']
                h2 = item['host2']

        try:
            x = requests.get("http://"+host+"8800")
        except:
            host = h2
            
        # meta = Meta.objects.filter(user=request.user.username, loc=filename).values_list('host', flat=True)
        # for s in meta:
        #     tp = filename.split('.')[1]
        print(host)
        location = "http://"+host+":8800/"+request.user.username+'/'+filename
        print(location)
        return render(request,"file.html",{'location':location,"type":type,'name':name,"size":size,"date":date_created})


    # ________________________________________________________________________________________
    #                                       Change dir
    # ________________________________________________________________________________________
    def changedir(request,folder):
        if request.method == "GET":
            fsco.fs.cd(folder)
            
        return redirect('home')

    # ________________________________________________________________________________________
    #                                       Change dir
    # ________________________________________________________________________________________

    def back(request):
        fsco.fs.back()
        return redirect('home')

    # ________________________________________________________________________________________
    #                                       devloper tools
    # ________________________________________________________________________________________
    def devconsole(request):
        projects = []
        names = []
        user =request.user.username
        if devs.objects.filter(username=user).exists():
            sql = "select * from mycloud_projects where owner = '"+user+"'"
            data = cursor.execute(sql)
            for d in data:
                for dat in d:
                    names.append(dat)
                pdata = {
                    'name':names[2],
                    'id':names[3]
                } 
                names = []
                projects.append(pdata) 
            return render(request, 'dev_console.html',{'projects':projects})
        else:
            return redirect('user_agreement')

    # ________________________________________________________________________________________
    #                                       Buy storage
    # ________________________________________________________________________________________

    def buy_storage(request):
        try:
            st = storage.objects.get(user = request.user.username)
            return render(request,"subscribed.html")
        except:
            c = razorpay.Client(auth=("rzp_test_881nU5d1hQtVkz", "ymv2KRqSpwTgXi4UirDHx5Ie"))
            DATA = {
                'amount' : 4900,
            'receipt' : 'order_rcptid_11',
            "currency": 'INR'
            }
        
            
            a  = c.order.create(data = DATA)
            id = a['id']
            return render(request,"buy.html",{"id":id})


    def success(request,pid,oid,sign):
        payment_id = pid 
        order_id = oid 
        signature = sign
        c = razorpay.Client(auth=("rzp_test_881nU5d1hQtVkz", "ymv2KRqSpwTgXi4UirDHx5Ie"))
        params_dict ={
            'razorpay_order_id': order_id,
    'razorpay_payment_id': payment_id,
    'razorpay_signature': signature
        }

        c.utility.verify_payment_signature(params_dict)

        st = storage()
        st.user = request.user.username
        st.payment_id = payment_id
        st.order_id = order_id
        st.save()
        
        return render(request,"success.html",{"tid":payment_id,"oid":order_id})
    # ______________________________________________________________________________________
    #                           developer Agreement
    # ______________________________________________________________________________________
    def dev_agreement(request):
        return render(request,'Agreement.html')


    # _______________________________________________________________________________________
    #                         Creating developer user
    # _______________________________________________________________________________________
    def create_devuser(request):
        pass1 = request.GET['pass1']
        pass2 = request.GET['pass2']
        if pass1 == pass2:
            password = pass1
        try:
            names=[]
            cursor.execute("create login "+request.user.username+" with password = '"+password+"'")
            cursor.execute("EXEC sp_addsrvrolemember @loginame = N'"+request.user.username+"',@rolename = N'dbcreator';")
            data = cursor.execute("select suser_sid('"+request.user.username+"')")
            
            for d in data:
                for dat in d:
                    b = dat
                    names.append(b)
                
            Dev = devs()
            Dev.username = request.user.username
            Dev.user_sid = names[0]
            Dev.user_password = bytes(password,"utf-8")
            Dev.date_joined = datetime.datetime.now()
            Dev.save()
            

        
        except Exception as a:
            string = str(a)
            l = string.split("]")
            l= l[4].split(".")
        return redirect('dev_console')


    # _____________________________________________________________________________________
    #                   developer project view
    # _____________________________________________________________________________________

    def project_view(request,projectname):
        owner = request.user.username
        password = devs.objects.filter(username=owner).values_list('user_password',flat=True)
        for s in password:
            password1 = s
            password2 = password1.decode("utf-8")
            
        pn = projectname
        tables = []
        tabledata ={}
        columns = []
        datalist = []
        Data =[]
        query=""
        custcols = []
        output = "Welcome to the Database Editor..."

        con = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-P3BU85V\MSSQLSERVER01;DATABASE="+pn+";UID="+owner+";PWD="+password2)
        con.autocommit=True
        cur = con.cursor()
        table = cur.execute("select sys.tables.name from sys.tables")
        
        for tab in table:
            for t in tab:
                t = str(t)
                tables.append(t)
        for t in  tables:
            cols = cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+t+"'")
            for col in cols:
                for c in col:
                    custcols.append(c)
                    tabledata[t]= custcols
                    
            custcols =[]     
        
        
        data = {"tables":tabledata}
        if request.method=="POST":
            
            owner = request.user.username
            query = request.POST['query']
            password = devs.objects.filter(username=owner).values_list('user_password',flat=True)
            for s in password:
                    password1 = s
                    password2 = password1.decode("utf-8")
            
            try:
                query2 = query.split("from")

                # checking custom column names 
                if query2[0].__contains__('*'):
                    custcol = []
                else:
                    cc =query2[0].split("select")
                    cc1 = cc[1]
                    cc1=cc1.replace(' ','')
                    if cc1.__contains__(","):
                        custcol = cc1.split(",")
                
                    else:
                        custcol =[cc1]

                    

                query3 = query2[1]
                
                query4 = query3.split(" ")
                
                table = query4[1]
                
                try:
                    con = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-P3BU85V\MSSQLSERVER01;DATABASE="+pn+";UID="+owner+";PWD="+password2)
                    con.autocommit=True
                    cur = con.cursor()
                    table = cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+table+"';")
                    
                    if len(custcol) >= 1:  
                        for d in table:
                            
                            for dat in d:
                                data = dat
                                for b in custcol:
                                    if b == data:
                                        columns.append(b)
                    else:
                        for d in table:
                            
                            for dat in d:
                                b = dat
                                columns.append(b)
                    
                    
                except Exception as a:
                    string = str(a)
                    l = string.split("]")
                    l= l[0].split(".")
            except Exception as e:
                print(e)
            try:
                con = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-P3BU85V\MSSQLSERVER01;DATABASE="+pn+";UID="+owner+";PWD="+password2)
                con.autocommit=True
                cur = con.cursor()
                data = cur.execute(query)
                
                try:
                    for d in data:
                        for dat in d:
                            b = dat
                            datalist.append(b)
                        Data.append(datalist)
                        datalist = []
                except:
                    pass
                output = "Query executed successfully..."
                cur.close()
                
            except Exception as a:
                string = str(a)
                l = string.split("]")
                l= l[4].split(".")
                output = l[0]

            
            return  render(request,'database_editor.html',{'project':pn,'query':query,'data':Data,'cols':columns,'output':output,"tables":tabledata})
            
        
        return  render(request,'database_editor.html',{'project':pn,'query':query,'data':Data,'cols':columns,'output':output,"tables":tabledata})


    # ________________________________________________________________________________
    #                   Creating new development project
    # ________________________________________________________________________________

    def create_project(request):
        if request.method == "POST":
            name = request.POST["project_name"]
            p_id = request.POST["project_id"]
            owner = request.user.username

            password = devs.objects.filter(username=owner).values_list('user_password',flat=True)
            for s in password:
                password1 = s
            password2 = password1.decode("utf-8")
            try:
                con = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-P3BU85V\MSSQLSERVER01;DATABASE=master;UID="+owner+";PWD="+password2)
                con.autocommit=True
                cur = con.cursor()
                cur.execute("create database "+p_id)
                cur.close()
                con.close()
                sql = "INSERT INTO mycloud_projects VALUES('"+owner+"','"+name+"','" + p_id + "')"
                cursor.execute(sql)
            except Exception as a:
                string = str(a)
                l = string.split("]")
                l= l[4].split(".")
            return redirect('dev_console')



    
