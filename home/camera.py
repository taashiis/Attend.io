import cv2
import numpy as np
import face_recognition
from django.conf import settings
import os
from home.models import Login

class VideoCamera(object):
    path='media'
    images=[]
    names=[]
    list=os.listdir(path)
    # print(list)
    name=''
    # data=Login.objects.all()

    # for cls in data:
    #     curr=cv2.imread(cls.userimg.url)
    #     images.append(curr)
    #     names.append(cls.empname)

    for cls in list:
        curr=cv2.imread(f'{path}/{cls}')
        images.append(curr)
        names.append(os.path.splitext(cls)[0])

    # print(names)

    def __init__(self):
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()

    # def returnname(self):
    #     return self.name

    def findencoding(images):
        encodelist=[]
        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist

    encodelistknown=findencoding(images)
    print("encoding done")
    matched=False

    def get_frame(self):
        # cap=cv2.VideoCapture(0)
        name=''
        matched=False
        success, img = self.video.read()
        imgs=cv2.resize(img,(0,0),None, 0.25,0.25)
        imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
        # print(imgs)
        facecurr= face_recognition.face_locations(imgs)
        encode=face_recognition.face_encodings(imgs,facecurr)

        for encodeface,faceloc in zip(encode,facecurr):
            matches=face_recognition.compare_faces(self.encodelistknown,encodeface)
            facedis=face_recognition.face_distance(self.encodelistknown,encodeface)
            matchindex=np.argmin(facedis)

            if matches[matchindex]:
                matched=True
                name = self.names[matchindex].lower()
                username=Login.objects.get(empid=name)
                # print(self.name)
                y1,x2,y2,x1= faceloc
                y1,x2,y2,x1= y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,str(username),(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),2)
            # cv2.imshow('webcam',img)
            # cv2.waitKey(1)
        # self,image=self.video.read()
        # frame_flip=cv2.flip(img,1)
        ret,jpeg=cv2.imencode('.jpg',img)
        return jpeg.tobytes(),matched,name
