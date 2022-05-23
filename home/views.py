import PIL.Image as Image
import io
import base64
import urllib.request
import cv2
import numpy as np
import face_recognition
import os
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from home.models import Login, Session
from django.http.response import StreamingHttpResponse
from home.camera import VideoCamera
from datetime import datetime
from django.template.defaulttags import register


username=""
global tloggedin
tloggedin=False
global end
end=False
# Create your views here.
def index(request):
    # context={
    #     'company':"attendees"
    # }
    return render(request, 'index.html')
    # return render(request, 'index.html',context)

def register(request):
    if request.method == "POST":
        id = request.POST.get('empid')
        name = request.POST.get('name')
        email = request.POST.get('email')
        passw = request.POST.get('emppass')
        base64str = request.POST.get('base64')
        # image = base64.b64decode(str(base64str))       
        # fileName = 'test.jpeg'
        # imagePath = ('D:\\base64toImage\\'+"test.jpeg")
        # img = Image.open(io.BytesIO(image))
        # img.save(imagePath, 'jpeg')
        # image = open("image.png", "wb")
        # imgdata = base64.b64decode(str(base64str))
        # image.write(imgdata.decode('base64'))
        # b=base64.b64decode(str(base64str))
        # img=Image.open(io.BytesIO(b))
        # img.show()
        filename=id
        response = urllib.request.urlopen(base64str)
        with open('media/'+filename+'.jpg', 'wb') as f:  
            f.write(response.file.read())
        # return HttpResponse(base64str)
        logindet = Login(empid=id, empname=name, empemail=email,emppass=passw,userimg=filename+'.jpg')
        logindet.save()
    return render(request,'register.html')

def login(request):
    if request.method == "POST":
        id = request.POST.get('empid')
        name=identifyuser(VideoCamera())
        passw=request.POST.get('emppass')
        email=request.POST.get('email')
        usern=request.POST.get('name')
        data=Login.objects.get(empid=id)
        if(id==name)and(passw==data.emppass)and(email==data.empemail):
            global username 
            username = Login.objects.get(empid=id).empid
            global tloggedin 
            tloggedin = True
            return HttpResponseRedirect('/user')
        else:
            return render(request, 'index.html')
    return render(request, 'login.html')

def gen(camera):
    while True:
        frame,matched,name=camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpg\r\n\r\n'+frame+b'\r\n\r\n')

def identifyuser(camera):
    name=''
    frame,matched,name=camera.get_frame()
    if(matched):
        return name
    else:
        return name

def video_feed(request):
    obj = VideoCamera()
    return StreamingHttpResponse(gen(obj),content_type='multipart/x-mixed-replace; boundary=frame')

def user(request,user=""):
    global tloggedin
    if not tloggedin:
        return render(request,'index.html')
    global username
    user=username
    VideoCamera.teacherlogged=True
    return render(request, 'homepage.html', {"username":Login.objects.get(empid=user).empname})

def session(request,user=""):
    global tloggedin
    if not tloggedin:
        return render(request,'index.html')
    global username
    user=username
    session=Session.objects.all()
    allsesh=[]
    emptylist=[]
    # students=Login.objects.all()
    for cls in session:
        if(cls.date.strftime("%b %d, %Y") not in allsesh) and cls.host==user:
            allsesh.append(cls.date.strftime("%b %d, %Y"))
    if request.method=='POST':
        sdate=request.POST.get('inputdate')
        presentstu=[]
        studentnames={}
        for cls in session:
            if cls.date.strftime("%b %d, %Y") == sdate and cls.host==user:
                print("")
                presentstu.append(cls)
                studentnames[cls.empid]=Login.objects.get(empid=cls.empid).empname
        return render(request,'session.html', {"username":Login.objects.get(empid=user).empname,"dates":allsesh,"present":presentstu,"users":studentnames})
    return render(request,'session.html', {"username":Login.objects.get(empid=user).empname,"dates":allsesh,"present":emptylist,"users":emptylist})

def logout(request):
    global tloggedin
    tloggedin=False
    global username
    username=""
    VideoCamera.teacherlogged=False
    return render(request, "index.html")

def sessionend(request):
    global end
    end=False
    global username
    user=username
    if(request.method=='POST'):
        end=True
        VideoCamera.saveattendance(user)
    return render(request,"sessionsaved.html")