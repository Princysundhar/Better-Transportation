# from datetime import datetime
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from DriveInnapp.models import *
#
# def view_index(request) :
#     return render(request, 'adminforms/index.html')
#


def forgot_password(request):
    return render(request,"forgot_password.html")

def forgot_password_post(request):
    email = request.POST['textfield2']
    res = login.objects.filter(username=email)
    if res.exists():
        pwd = res[0].password
        import smtplib

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        # s.login("riss.princytv@gmail.com", "dnsb yopn jqxq hrko")
        s.login("demo@gmail.com", "dnsb yopn jqxq hrko")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "demo@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for Easy rent project"
        body = "Your Password is:- - " + str(pwd)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return HttpResponse("<script>alert('Email sended');window.location='/'</script>")
    return HttpResponse("<script>alert('Mail Incorrect');window.location='/'</script>")

def login(request):
    return render(request,'login_index.html')
    # return render(request,'login.html')

def login_post(request):
    usn = request.POST['textfield']
    psw = request.POST['textfield2']
    res = login_table.objects.filter(username=usn, password=psw)
    if res.exists():
        request.session['lid']=res[0].id
        request.session['lg']="lin"
        if res[0].usertype == 'admin':
            return HttpResponse("<script>alert('Successfully logined by admin!'); window.location='/admin_index'</script>")

        elif res[0].usertype == 'worker':
            return HttpResponse("<script>alert('Successfully logined by worker!'); window.location='/worker_index'</script>")


        elif res[0].usertype == 'pending':
            return HttpResponse("<script>alert('WAIT FOR AUTHENTICATION !'); window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('ERROR !'); window.location='/'</script>")

def admin_index(request) :
    return render(request, 'adminforms/admin_index.html')
    # return render(request, 'adminforms/AdminHome.html')

def admin_home(request):
    return render(request, 'adminforms/AdminHome.html')


def view_user(request):
    data = user_table.objects.all()
    return render(request, 'adminforms/ViewUsers.html',{"data":data})


def view_feedback(request):
    data= feedback_table.objects.all()
    return render(request, 'adminforms/ViewFeedback.html', {"data":data})

def view_verify_workers(request):
    data = workers_table.objects.filter(LOGIN_TABLE__usertype='pending')
    return render(request, 'adminforms/ViewVerifyWorkers.html', {"data":data})


def approve_worker(request,id):
    login_table.objects.filter(id = id).update(usertype='worker')
    return HttpResponse("<script>alert('WORKER APPROVED SUCESSSFULLY !'); window.location='/view_verify_workers'</script>")

def reject_worker(request,id):
    login_table.objects.filter(id=id).update(usertype='rejected')
    return HttpResponse("<script>alert('WORKER REJECTED SUCESSSFULLY !'); window.location='/view_verify_workers'</script>")


def view_verified_workers(request):
    data = workers_table.objects.filter(LOGIN_TABLE__usertype='worker')
    return render(request, 'adminforms/ViewVerifiedWorkers.html', {"data":data})

def view_rating_review(request,id):
    data = rating_review_table.objects.filter(WORKER=id)
    return render(request, 'adminforms/ViewReviewRating.html', {"data": data})


def change_password(request):
    return render(request, 'adminforms/ChangePass.html')


def change_password_post(request):
    cur = request.POST['textfield']
    new = request.POST['textfield2']
    cnew = request.POST['textfield3']

    pwd= login_table.objects.filter(password=cur, usertype='admin')
    if pwd.exists():
        if new==cnew:
            pwd.update(password=cnew)
            return HttpResponse("<script>alert('PASSWORD CHANGED SUCESSFULLY'); window.location='/admin_index'</script>")

        else :
            return HttpResponse("<script>alert('CHECK AGAIN'); window.location='/change_password'</script>")

    else:
        return HttpResponse("<script>alert('UNSUCESSFUL  !!!'); window.location='/admin_index'</script>")


def view_complaints(request):
    data = complaints_table.objects.all()
    return render(request, 'adminforms/viewComplaintsReply.html' , {"data":data})

def reply(request,id):
    return render(request, 'adminforms/sendreply.html',{"id":id})

def reply_sent(request,id):
    r = request.POST['textarea']
    d=datetime.datetime.now().strftime("%Y/%m/%d")
    complaints_table.objects.filter(id=id).update(reply=r,rdate =d)
    return HttpResponse("<script>alert('REPLY HAS BEEN SENT'); window.location='/view_complaints'</script>")


def logout(request):
    request.session['lg'] =""
    return HttpResponse("<script>alert(' LOGGED OUT SUCESSFULLY :)  '); window.location='/'</script>")

# ================================================================

def worker_index(request) :
    # return render(request, 'workerforms/WORind.html')
    return render(request, 'workerforms/worker_index.html')

def register(request):
    # return render(request,'workerforms/register.html')
    return render(request, 'worker_register.html')

def register_post(request):
    wname = request.POST['wname']
    wemail = request.POST['wemail']
    wcon = request.POST['wcon']
    wland = request.POST['wland']
    wplace = request.POST['wplace']
    wpost = request.POST['wpost']
    wlat = request.POST['textfield8']
    wlong = request.POST['textfield9']
    wadhaar =request.POST['wadhaar']
    wpass = request.POST['wpass']
    wcpass = request.POST['wcpass']
    wphoto = request.FILES['wphoto']
    d=datetime.datetime.now().strftime("%Y/%m/%d-%H-%M-%S")
    fs=FileSystemStorage()
    fs.save(r"C:\Users\DELL\PycharmProjects\driveinn\DriveInnapp\static\img\\"+d+".jpg",wphoto)
    path="/static/img/"+d+".jpg"
    if wpass == wcpass:
        obj = login_table()
        obj.username = wemail
        obj.password = wcpass
        obj.usertype = "pending"
        obj.save()

        obj1 = workers_table()
        obj1.workername = wname
        obj1.email = wemail
        obj1.contact = wcon
        obj1.landmark = wland
        obj1.place = wplace
        obj1.postcode = wpost
        obj1.latitude = wlat
        obj1.longitude = wlong
        obj1.aadhar = wadhaar
        obj1.photo = path
        obj1.LOGIN_TABLE=obj
        obj1.save()
        return HttpResponse("<script>alert('REGISTERED SUCESSFULLY'); window.location='/'</script>")

    else:
        return HttpResponse("<script>alert('CHECK AGAIN'); window.location='/'</script>")



def profile_update(request):
    obj = workers_table.objects.get(LOGIN_TABLE=request.session['lid'])
    return render(request,'workerforms/profieUPDATE.html', {"data": obj})

def profile_update_post(request):
    wname = request.POST['wname']
    wemail = request.POST['wemail']
    wcon = request.POST['wcon']
    wland = request.POST['wland']
    wplace = request.POST['wplace']
    wpost = request.POST['wpost']
    wlat = request.POST['wlat']
    wlong = request.POST['wlong']
    wadhaar = request.POST['wadhaar']
    wphoto = request.FILES['wphoto']
    d = datetime.datetime.now().strftime("%Y/%m/%d-%H-%M-%S")
    fs = FileSystemStorage()
    fs.save(r"C:\Users\asus\PycharmProjects\driveinn\DriveInnapp\static\img\\" + d + ".jpg", wphoto)
    path = "/static/img/" + d + ".jpg"

    workers_table.objects.filter(LOGIN_TABLE=request.session['lid']).update(workername=wname,email=wemail,contact=wcon,landmark=wland,place=wplace,postcode=wpost,latitude=wlat,longitude=wlong,aadhar=wadhaar,photo=path)

    return HttpResponse("<script>alert('PROFILE UPDATED SUCESSFULLY '); window.location='/profile_update'</script>")


def view_request_verify(request):
    data = request_table.objects.filter(WORKER_TABLE__LOGIN_TABLE__id=request.session['lid'], status="pending")
    return render(request,'workerforms/viewREQverify.html',{"data": data})

def approve_request (request,id):
    request_table.objects.filter(id = id).update(status='approved')
    return HttpResponse("<script>alert('REQUEST APPROVED !'); window.location='/worker_index'</script>")

def reject_request (request,id):
    request_table.objects.filter(id = id).update(status='rejected')
    return HttpResponse("<script>alert('REQUEST REJECTED !'); window.location='/worker_index'</script>")


def view_verified_request(request):
    data = request_table.objects.filter(Q(WORKER_TABLE__LOGIN_TABLE=request.session['lid'],status__in=["approved", "completed"]))
    return render(request,'workerforms/viewVERreq.html' , {"data": data})

def work_complete(request,id):
    request_table.objects.filter(id=id).update(status='completed')
    return HttpResponse("<script>alert('WORK COMPLETED !'); window.location='/worker_index'</script>")

def view_work_history(request):
    data = request_table.objects.filter(status='completed')
    return render(request,'workerforms/viewWORKhist.html' , {"data": data})

def view_work_history_date(request):
    date=request.POST['textfield']
    data = request_table.objects.filter(date=date,status='completed')
    if data.exists():
        return render(request,'workerforms/viewWORKhist.html' , {"data": data})
    else:
        return HttpResponse("<script>alert('CHOOSE CORRECT DATE !'); window.location='/view_work_history'</script>")



def view_wrating(request):
    res =rating_review_table.objects.filter(WORKER__LOGIN_TABLE=request.session['lid'])
    fs = "/static/star/full.jpg"
    hs = "/static/star/half.jpg"
    es = "/static/star/empty.jpg"
    data = []

    for rt in res:
        print(rt)
        a = float(rt.rating)
        if a >= 0.0 and a < 0.4:
            print("eeeee")
            ar = [es, es, es, es, es]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })

        elif a >= 0.4 and a < 0.8:
            print("heeee")
            ar = [hs, es, es, es, es]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })

        elif a >= 0.8 and a < 1.4:
            print("feeee")
            ar = [fs, es, es, es, es]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })

        elif a >= 1.4 and a < 1.8:
            print("fheee")
            ar = [fs, hs, es, es, es]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })

        elif a >= 1.8 and a < 2.4:
            print("ffeee")
            ar = [fs, fs, es, es, es]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })

        elif a >= 2.4 and a < 2.8:
            print("ffhee")
            ar = [fs, fs, hs, es, es]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })

        elif a >= 2.8 and a < 3.4:
            print("fffee")
            ar = [fs, fs, fs, es, es]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })

        elif a >= 3.4 and a < 3.8:
            print("fffhe")
            ar = [fs, fs, fs, hs, es]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })

        elif a >= 3.8 and a < 4.4:
            print("ffffe")
            ar = [fs, fs, fs, fs, es]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })

        elif a >= 4.4 and a < 4.8:
            print("ffffh")
            ar = [fs, fs, fs, fs, hs]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })

        elif a >= 4.8 and a <= 5.0:
            print("fffff")
            ar = [fs, fs, fs, fs, fs]
            data.append({
                'USER': rt.USER,
                'WORKER': rt.WORKER,
                'review': rt.review,
                'date': rt.date,
                'rating': ar,

            })
        print(data,"data")
    return render(request,'workerforms/viewRATING.html', {"data":data})


def view_wcomplaints(request):
    data = complaints_table.objects.filter(LOGIN_TABLE=request.session['lid'])
    return render(request,'workerforms/viewCOMP.html', {"data": data})


def send_wcomplaints(request):
    return render(request,'workerforms/sendCOMP.html')


def send_wcomplaints_post(request):
    comp = request.POST['comp']
    c = complaints_table()
    c.date=datetime.datetime.now().strftime("%Y/%m/%d-%H-%M-%S")
    c.complaint=comp
    c.LOGIN_TABLE_id = request.session['lid']
    c.ctype='worker'
    c.reply='pending'
    c.rdate='pending'
    c.save()
    return HttpResponse("<script>alert('COMPLAINT SEND !'); window.location='/worker_index'</script>")


def chatt(request,u):
    request.session['u'] = u
    return render(request,'workerforms/chat.html',{'u':u})


def chatsnd(request,u):
  if request.method=="POST":
    d=datetime.datetime.now().strftime("%Y-%m-%d")
    c = request.session['lid']
    m=request.POST['m']
    cc = workers_table.objects.get(LOGIN_TABLE__id=c)
    uu = user_table.objects.get(id=request.session['u'])
    obj=chat()
    obj.date=d
    obj.type='worker'
    obj.WORKER_TABLE=cc
    obj.USER_TABLE=uu
    obj.chat=m
    obj.save()
    if int(obj.id) > 0:
        return JsonResponse({"status":"ok"})
    else:
        return JsonResponse({"status": "no"})



def chatrply(request):
    c = request.session['lid']
    cc=workers_table.objects.get(LOGIN_TABLE=c)
    uu=user_table.objects.get(id=request.session['u'])
    res = chat.objects.filter(WORKER_TABLE=cc,USER_TABLE=uu)
    v = []
    if len(res) > 0:
        print(len(res))
        for i in res:
            v.append({
                'type':i.type,
                'chat':i.chat,
            })
        # print(v)
        return JsonResponse({"status": "ok", "data": v, "id": cc.id})
    else:
        return JsonResponse({"status": "error"})

# def reply(request):
#     return render(request,'workerforms/')



#.........................................................................................

def view_wpayhistory(request):
    total = 0
    data = payment_table.objects.filter(USER_TABLE__LOGIN_TABLE_id=request.session['lid'])
    for i in data:
        total+=i.amount
    return render(request,'workerforms/viewPAYhist.html',{"data":data, "total": total})


def view_wpayhistory_post(request):
    date = request.POST['textfield']
    data = payment_table.objects.filter(USER_TABLE__LOGIN_TABLE_id=request.session['lid'], date=date)
    total = 0
    for i in data:
        total+=i.amount
    return render(request,'workerforms/viewPAYhist.html',{"data":data, "total":total})



def secret_code(request):
    return render(request,'workerforms/secCODE.html')

def change_pass(request):
    return render(request,'workerforms/changePASS.html')

def change_pass_post(request):
    cp = request.POST['textfield']
    np = request.POST['textfield2']
    rnp = request.POST['textfield3']

    pwd = login_table.objects.filter(password=cp, id=request.session['lid'])
    if pwd.exists():
        if np == rnp:
            pwd.update(password=rnp)
            return HttpResponse("<script>alert('PASSWORD CHANGED SUCESSFULLY'); window.location='/worker_index'</script>")

        else:
            return HttpResponse("<script>alert('CHECK AGAIN'); window.location='/change_pass'</script>")

    else:
        return HttpResponse("<script>alert('UNSUCESSFUL  !!!'); window.location='/worker_index'</script>")

# ===================================== ANDROID


def android_login(request):
    usn = request.POST['u']
    psw = request.POST['p']
    res = login_table.objects.filter(username=usn, password=psw)
    if res.exists():
        return JsonResponse({"status":"ok","lid":res[0].id,"type":res[0].usertype})
    else:
        return JsonResponse({"status":"no"})


def android_register(request):
    uname = request.POST['name']
    uemail = request.POST['email']
    ucon = request.POST['contact']
    upass = request.POST['password']
    uphoto = request.FILES['pic']
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs = FileSystemStorage()
    fs.save(r"C:\Users\DELL\PycharmProjects\driveinn\DriveInnapp\static\photo\\" + d + ".jpg", uphoto)
    path = "/static/photo/" + d + ".jpg"


    obj = login_table()
    obj.username = uname
    obj.password = upass
    obj.usertype = "user"
    obj.save()

    obj1 = user_table()
    obj1.name = uname
    obj1.email = uemail
    obj1.contact = ucon
    obj1.photo = path
    obj1.LOGIN_TABLE = obj
    obj1.save()

    return JsonResponse({"status":"ok"})


def android_view_worker(request):
    wt=workers_table.objects.all()
    ar=[]
    for i in wt :
        ar.append(
            {
                "id":i.id,
                "img":i.photo,
                "name":i.workername,
                "email":i.email,
                "contact":i.contact,
                "landmark":i.landmark,
                "place":i.place,
                "adno":i.aadhar,
                "latitude":i.latitude,
                "longitude":i.longitude
            }
        )

    if len(ar)>0:
        return JsonResponse({"status": "ok","data":ar})

    else:
        return JsonResponse({"status": "no"})

def android_send_request(request):
    lid = request.POST['lid']
    rid = request.POST['rid']
    date = request.POST['date']
    remark = request.POST['remark']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    obj = request_table()
    obj.USER = user_table.objects.get(LOGIN_TABLE=lid)
    obj.WORKER_TABLE_id = rid
    obj.remark = remark
    obj.date = date
    obj.status = 'pending'
    obj.latitude = latitude
    obj.longitude = longitude
    obj.save()
    return JsonResponse({"status":"ok"})


def android_view_request_status(request):
    lid=request.POST['lid']
    rs=request_table.objects.filter(USER_TABLE__LOGIN_TABLE=lid,status='completed')
    ar=[]
    for i in rs:
        ar.append(

            {
                "id": i.id,
                "name": i.WORKER_TABLE.workername,
                "date": i.date,
                "query": i.remark,
                "status": i.status,
                "latitude":i.latitude,
                "longitude":i.longitude,
                "amount":i.amount
            }
        )

    if len(ar) > 0:
        return JsonResponse({"status": "ok", "data": ar})
    else:
        return JsonResponse({"status": "no"})

def android_rental_service(request):
    return JsonResponse({"status": "ok"})


def android_request_history(request):
    lid = request.POST['lid']
    res = payment_table.objects.filter(REQUEST_TABLE__USER_TABLE__LOGIN_TABLE_id=lid,payment_mode__in=["online","offline"])
    ar = []
    for i in res:
        ar.append(
            {
                "hid":i.id,
                "requests":i.REQUEST_TABLE.remark,
                "amount":i.amount,
                "date":i.date,
                "payment_mode":i.payment_mode
            }
        )
    print(ar)
    return JsonResponse({"status": "ok","data":ar})


def android_send_rating(request):
    ratings = request.POST['rating']
    reviews = request.POST['review']
    lid = request.POST['lid']
    wid = request.POST['rid']

    obj = rating_review_table()
    obj.date = datetime.datetime.now().strftime("%Y/%m/%d")
    obj.rating = ratings
    obj.review = reviews
    obj.USER = user_table.objects.get(LOGIN_TABLE=lid)
    obj.WORKER_id = wid
    obj.save()


    return JsonResponse({"status": "ok"})


def android_view_rating(request):
    rid = request.POST['rid']
    res = rating_review_table.objects.filter(WORKER=rid)
    ar = []
    for i in res:


        ar.append(
            {
                "rid":i.id,
                "rating":i.rating,
                "review":i.review,
                "date":i.date,
                "worker_info":i.WORKER.workername,
                "userinfo":i.USER.name
            }
        )
    return JsonResponse({"status": "ok","data":ar})


def android_send_feedback(request):
    fdback=request.POST['feedback']
    lid = request.POST['lid']
    d = datetime.datetime.now().strftime("%Y/%m/%d")

    obj = feedback_table()
    obj.feedback=fdback
    obj.date=d
    obj.USER_TABLE = user_table.objects.get(LOGIN_TABLE=lid)
    obj.save()

    return JsonResponse({"status": "ok"})


def android_send_complaint(request):
    complaints = request.POST['c']
    lid = request.POST['lid']
    obj = complaints_table()
    obj.complaint = complaints
    obj.date = datetime.datetime.now().strftime("%d/%m/%Y")
    obj.ctype ='user'
    obj.reply ="pending"
    obj.rdate ="pending"
    obj.LOGIN_TABLE_id = lid
    obj.save()
    return JsonResponse({"status": "ok"})


def android_view_reply(request):
    lid = request.POST['lid']
    res = complaints_table.objects.filter(LOGIN_TABLE=lid)
    ar = []
    for i in res:
        ar.append(
            {
                "cid":i.id,
                "complaint":i.complaint,
                "date":i.date,
                "reply":i.reply,
                "reply_date":i.rdate,
                "ctype":i.ctype

            }
        )
    return JsonResponse({"status":"ok","data":ar})


# def android_payment_history(request):
#     return JsonResponse({"status": "ok"})
#
#
# def android_credit_points(request):
#     return JsonResponse({"status": "ok"})


def android_change_password(request):
    lid = request.POST['lid']
    current_password = request.POST['crp']
    new_password = request.POST['new_password']
    confirm_password =request.POST['confirm_password']
    data = login_table.objects.filter(password=current_password,id= lid)
    if data.exists():
        if new_password == confirm_password:
            if login_table.objects.filter(password=new_password).exists():
                return JsonResponse({"status":"No"})
            else:
                login_table.objects.filter(id=lid).update(password=confirm_password)
                return JsonResponse({"status":"ok"})
        else:
            return JsonResponse({"status":"mismatch"})
    else:
        return JsonResponse({"status":"error"})



# .........ANDROID CHAT

def android_add_chat(request):
    lid = request.POST['lid']
    aid = request.POST['toid']
    message = request.POST['message']
    print(lid)
    print(aid)
    obj = chat()
    obj.chat = message
    obj.date = datetime.datetime.now().strftime("%Y-%m-%d")
    obj.type = 'user'
    obj.USER = user_table.objects.get(LOGIN_TABLE=lid)
    obj.WORKER_TABLE_id = aid
    obj.save()

    return JsonResponse({"status":"Inserted"})

def android_view_chat(request):
    lid = request.POST['lid']
    toid = request.POST['toid']
    lastid = request.POST['lastid']
    res = chat.objects.filter(Q(USER_TABLE=user_table.objects.get(LOGIN_TABLE=lid)),Q(id__gt=lastid))
    ar = []
    for i in res:
        ar.append(
            {
                "id": i.id,
                "date": i.date,
                "userid": i.USER_TABLE.id,
                "sid": i.type,
                "chat": i.chat,

            })

    return JsonResponse({'status': "ok", 'data': ar})



# ..................payment................

def and_offline_payment(request):
    lid = request.POST['lid']
    aid = request.POST['aid']
    amount = request.POST['amount']
    obj = payment_table()
    obj.payment_mode = 'offline'
    obj.amount = amount
    obj.date = datetime.datetime.now().strftime("%Y-%m-%d")
    obj.USER = user_table.objects.get(LOGIN_TABLE=lid)
    obj.USERREQUEST = request_table.objects.get(id=aid)
    obj.save()
    return JsonResponse({"status":"ok"})

def android_online_payment(request):
    lid = request.POST['lid']
    aid = request.POST['aid']
    amount = request.POST['amount']
    obj = payment_table()
    obj.payment_mode = 'online'
    obj.amount = amount
    obj.date = datetime.datetime.now().strftime("%Y-%m-%d")
    obj.USER = user_table.objects.get(LOGIN_TABLE=lid)
    obj.USERREQUEST = request_table.objects.get(id=aid)
    obj.save()
    return JsonResponse({"status":"ok"})

def android_view_payment_history(request):
    res = payment_table.objects.filter(payment_mode__contains=["online","offline"])
    ar = []
    for i in res:
        ar.append(
            {
                "pid":i.id,
                "name":i.USER_TABLE.name,
                "email":i.USER_TABLE.email,
                "amount":i.amount,
                "date":i.date,
                "payment_mode":i.payment_mode
            }
        )

    return JsonResponse({"status":"ok","data":ar})




#........................... CREDIT POINT PAYMENT ...................................

def mode(request):
    re=request.POST['reqid']
    mode=request.POST['m']


    request_table.objects.filter(id=re).update(payment_status=mode)
    return JsonResponse({'status': 'ok'})

def payment(request):
    re=request.POST['reqid']

    amt=request.POST['amount']
    bn=request.POST['bank']
    ifs=request.POST['ifs']
    acno=request.POST['acn']
    cid=request.POST['cid']
    lid=request.POST['log']
    print("amount",amt)
    print("cid",cid)
    # contractorinstance=login.objects.get(id=cid)

    res=bank.objects.filter(bname=bn,ifsc=ifs,accno=acno,HOLDER=lid)
    print(res)
    if res.exists():
        print("aaaaaaa")
        if res[0].balance >= amt:
            if int(amt) >= 1000:
                userbank = bank.objects.get(HOLDER=lid)
                print(userbank,"asdfghjkl")
                b_user=userbank.balance
                print(b_user)
                print(amt)
                balance_amount = int(b_user) - int(amt)
                print(balance_amount)
                bank.objects.filter(HOLDER=lid).update(balance=balance_amount)
                contrctr=workers_table.objects.get(id=cid)
                print("cccccccccccccc",cid)
                contractorbank = bank.objects.get(HOLDER=contrctr.LOGIN)
                b_contrctr=contractorbank.balance
                balance = int(b_contrctr) + int(amt)
                bank.objects.filter(HOLDER=contrctr.LOGIN).update(balance=balance)
                request_table.objects.filter(id=re).update(payment_status='Online')

                # =======credit========
                qry=credit_point_table.objects.filter(LOGIN=lid)
                if qry.exists():
                    cp=qry[0].creditpoints
                    total_credit=int(cp)+10
                    credit_point_table.objects.filter(LOGIN=lid).update(creditpoints=total_credit)
                else:
                    obj=credit_point_table()
                    obj.LOGIN=lid
                    obj.creditpoints=10
                    obj.save()

                return JsonResponse({'status': 'ok'})
            else:

                # ============no credit points================
                userbank = bank.objects.get(HOLDER=lid)
                print(userbank, "asdfghjkl")
                b_user = userbank.balance
                print(b_user)
                print(amt)
                balance_amount = int(b_user) - int(amt)
                print(balance_amount)
                bank.objects.filter(HOLDER=lid).update(balance=balance_amount)
                contrctr = workers_table.objects.get(id=cid)
                print("cccccccccccccc", cid)
                contractorbank = bank.objects.get(HOLDER=contrctr.LOGIN)
                b_contrctr = contractorbank.balance
                balance = int(b_contrctr) + int(amt)
                bank.objects.filter(HOLDER=contrctr.LOGIN).update(balance=balance)
                request_table.objects.filter(id=re).update(payment_status='Online')
                return JsonResponse({'status': 'ok'})

        return JsonResponse({'status': 'insufficient'})

    return JsonResponse({'status': 'no such account'})




#####################################################################################




def and_ajax_view_credit_points(request):
    amt = request.POST['amt']
    lid = request.POST['log']
    q = credit_point_table.objects.filter(LOGIN_TABLE = login_table.objects.get(id=lid))

    if q.exists():
        if int(q[0].creditpoints)>0:
            payable = float(q[0].creditpoints)/10
            # credit point to amount conversion (10 points = 1rupee)
            balance = int(amt) - int(payable)  # calculating balance amount
            # request.session['gtm'] = balance
            # request.session['credit'] = payable

            return JsonResponse({"status": "ok", "credit": q[0].creditpoints, "payable": payable, "balance": balance})
        else:
            return JsonResponse({"status": "no"})  # no credit points

    else:
        return JsonResponse({"status": "no"})  # no credit points




def android_credit_point_payment(request):
    re=request.POST['reqid']

    amt=request.POST['amount']
    bn=request.POST['bank']
    ifs=request.POST['ifs']
    acno=request.POST['acn']
    cid=request.POST['cid']
    lid=request.POST['log']

    # amount = request.POST['amount']
    creditss = request.POST['credits']
    logininstance = login_table.objects.get(id=lid)
    # print("widddddd",wid)

    res = bank.objects.filter(bname=bn, ifsc=ifs, accno=acno, HOLDER=lid)
    print(res)
    if res.exists():
        print("aaaaaaa")
        if res[0].balance >= amt:
            userbank = bank.objects.get(HOLDER=lid)
            print(userbank, "asdfghjkl")
            b_user = userbank.balance
            print(b_user)
            print(amt)
            balance_amount = int(b_user) - int(amt)
            print(balance_amount)
            bank.objects.filter(HOLDER=lid).update(balance=balance_amount)
            contrctr = workers_table.objects.get(id=cid)
            print("cccccccccccccc", cid)
            contractorbank = bank.objects.get(HOLDER=contrctr.LOGIN)
            b_contrctr = contractorbank.balance
            balance = int(b_contrctr) + int(amt)
            bank.objects.filter(HOLDER=contrctr.LOGIN).update(balance=balance)
            request_table.objects.filter(id=re).update(payment_status='Online')
            # if request.session['paymod  e'] == 'using credit point':

            ucredit = credit_point_table.objects.filter(LOGIN_TABLE=login_table.objects.get(id=lid))
            if ucredit.exists():
                cr = int(ucredit[0].creditpoints) - int(creditss)
                ucredit.update(creditpoints=cr)

            if int(amt) >= 1000:

                ucredit = credit_point_table.objects.filter(LOGIN_TABLE = login_table.objects.get(id=lid))
                if ucredit.exists():
                    cr = int(ucredit[0].creditpoints) + 10
                    ucredit.update(creditpoints = cr)
                else:

                    cobj = credit_point_table()  # Adding Credit point
                    cobj.creditpoints = 10
                    cobj.LOGIN_TABLE = login_table.objects.get(id=lid)
                    cobj.save()

                # bobj = job_request.objects.get(id=re)
                contrctr = workers_table.objects.get(id=cid)
                wcredit = credit_point_table.objects.filter(LOGIN_TABLE=contrctr.LOGIN_TABLE)
                if wcredit.exists():
                    cr = int(wcredit[0].credit_point) + 10
                    wcredit.update(credit_point=cr)
                else:
                    crobj = credit_point_table()
                    crobj.creditpoints = 10
                    crobj.LOGIN_TABLE = contrctr.LOGIN_TABLE
                    crobj.save()

                return JsonResponse({"status":"ok"})
        else:
            return JsonResponse({"status":"insufficient"})
    else:
        return JsonResponse({"status":"no"})















