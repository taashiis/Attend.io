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

# username to keep tracked of logged in user
username="" 
# variable to check if someone is logged in or not
global tloggedin
tloggedin=False
# variable to check if a session ended or not
global end
end=False
# Create your views here.
def index(request):
    return render(request, 'index.html')


# register new users. Takes credentials such as id, name, email, password and 
# photo of user and stores it to database
def register(request):
    if request.method == "POST":
        id = request.POST.get('empid')
        name = request.POST.get('name')
        email = request.POST.get('email')
        passw = request.POST.get('emppass')
        base64str = request.POST.get('base64')
        filename=id
        response = urllib.request.urlopen(base64str)
        with open('media/'+filename+'.jpg', 'wb') as f:  
            f.write(response.file.read())
        logindet = Login(empid=id, empname=name, empemail=email,emppass=passw,userimg=filename+'.jpg')
        logindet.save()
    return render(request,'register.html')


# takes credentials such as id , email, password and identifies the user in front of camera
# and if the details match it redirects the user to homepage
def login(request):
    obj = VideoCamera()
    if request.method == "POST":
        id = request.POST.get('empid')
        name=identifyuser(obj)
        passw=request.POST.get('emppass')
        email=request.POST.get('email')
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

# generates continous stream of images after openCV processes the image and identifies the
# face, and sends it as a video stream
def gen(camera):
    while True:
        frame,matched,name=camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpg\r\n\r\n'+frame+b'\r\n\r\n')

# identify the user in the login part of the interface and returns the username
def identifyuser(camera):
    name=''
    frame,matched,name=camera.get_frame()
    if(matched):
        return name
    else:
        return name

# calls openCV function to capture the video of the user and send back video after
#recognising and processing
def video_feed(request):
    obj = VideoCamera()
    return StreamingHttpResponse(gen(obj),content_type='multipart/x-mixed-replace; boundary=frame')


# redirected to this view - homepage after a user logs in succesfully. in case of failure to login redirects to
# index page of website
def user(request,user=""):
    global tloggedin
    if not tloggedin:
        return render(request,'index.html')
    global username
    user=username
    VideoCamera.teacherlogged=True
    return render(request, 'homepage.html', {"username":Login.objects.get(empid=user).empname})

# displays all the sessions. When user selects a date, a POST request gets made and data is retrived from 
# the database where the host of the session is the user logged in, and the date matches the selected one
def session(request,user=""):
    global tloggedin
    if not tloggedin:
        return render(request,'index.html')
    global username
    user=username
    session=Session.objects.all()
    allsesh=[]
    emptylist=[]
    for cls in session:
        if(cls.date.strftime("%b %d, %Y") not in allsesh) and cls.host==user:
            allsesh.append(cls.date.strftime("%b %d, %Y"))
    if request.method=='POST':
        sdate=request.POST.get('inputdate')
        presentstu=[]
        studentnames={}
        sessions={}
        for cls in session:
            if cls.date.strftime("%b %d, %Y") == sdate and cls.host==user:
                if cls.sno not in sessions.keys():
                    if(cls.empid==""):
                        sessions[cls.sno]=0
                    else:
                        sessions[cls.sno]=1
                else:
                    if (cls.empid != ""):
                        sessions[cls.sno]+=1
                if cls.empid == "":
                    studentnames[""]=""
                else:
                    studentnames[cls.empid]=Login.objects.get(empid=cls.empid).empname
                presentstu.append(cls)
        return render(request,'session.html', {"username":Login.objects.get(empid=user).empname,"dates":allsesh,"present":presentstu,"users":studentnames,"sessions":sessions})
    return render(request,'session.html', {"username":Login.objects.get(empid=user).empname,"dates":allsesh,"present":emptylist,"users":emptylist,":session":emptylist})

# logging out the user
def logout(request):
    global tloggedin
    tloggedin=False
    global username
    username=""
    VideoCamera.teacherlogged=False
    return render(request, "index.html")

# when a session ends the POST request is made and attendance of all the attendees get saved to database
def sessionend(request):
    global end
    end=False
    global username
    user=username
    if(request.method=='POST'):
        end=True
        VideoCamera.saveattendance(user)
    return render(request,"sessionsaved.html")