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
import datetime

username=""
global tloggedin
tloggedin=False
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
        data=Login.objects.get(empid=id)
        if(id==name)and(passw==data.emppass):
            global username 
            username = Login.objects.get(empid=id)
            global tloggedin 
            tloggedin = True
            return user(request,username)
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
    return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')

def user(request,user=""):
    global tloggedin
    if not tloggedin:
        return render(request,'index.html')
    global username
    user=username
    obje = VideoCamera()
    obje.loggedin()
    if(request.method=='POST'):
        VideoCamera.saveattendance()
    return render(request, 'homepage.html', {"username":user})