import cv2 #openCV모듈

import numpy as np #numpy모듈

import os #라즈비안

import RPi.GPIO as GPIO #라즈베리파이 GPIO



import time #time모듈

from bluetooth import * # 블루투스모듈

import re

client_socket = BluetoothSocket(RFCOMM) #블루투스 소켓설정

client_socket.connect(("00:20:10:08:AC:1E", 1))#블루투스 연결

msg="0" #메시지설정

GPIO.setmode(GPIO.BCM)# GPIO설정

GPIO.setup(24,GPIO.IN)

GPIO.setmode(GPIO.BCM)

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('trainer/trainer.yml') #데이터 학습파일 _  yml파일 가져오기

cascadePath = "/home/pi/haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

pirPin=24 #라즈베리파이 GPIO25번에 pir센서 연결

GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)#GPIO설정

id = 0

cam = cv2.VideoCapture(0)

cam.set(3, 640) # set video widht

cam.set(4, 480) # set video height

minW = 0.1*cam.get(3)

minH = 0.1*cam.get(4)

#names = ['1', '2', '3', '4', '5', '2', '3', '4', '5', '2', '3', '4', '5','1', '2', '3', '4', '5', '2', '3', '4', '5', '2', '3', '4', '5','1', '2', '3', '4', '5', '2', '3', '4', '5', '2', '3', '4', '5','1', '2', '3', '4', '5', '2', '3', '4', '5', '2', '3', '4', '5','1', '2', '3', '4', '5', '2', '3', '4', '5', '2', '3', '4', '5']
names = ['1','2','3','4','5']

while True:

    if  GPIO.input(pirPin)==GPIO.LOW:

        ret, img =cam.read()

        #img = cv2.flip(img,-1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

       

        faces = faceCascade.detectMultiScale(

            gray,

            scaleFactor = 1.2,

            minNeighbors = 5,

            minSize = (int(minW), int(minH)),

           )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

           

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
           

            # Check if confidence is less them 100 ==> "0" is perfect match

           

            if (confidence < 100):
                id = names[id-1]

                confidence1= "  {0}%".format(round(100 - confidence))

                confidence2="{0}%".format(round(100 - confidence))

               

            else:

                id = "unknown"

                confidence1= "  {0}%".format(round(100 - confidence))

                confidence2="{0}%".format(round(100 - confidence))

                

            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)

            cv2.putText(img, str(confidence1), (x+5,y+h-5), font, 1, (255,255,0), 1)

           

            cv2.imshow('camera',img)

           

            b=re.findall("\d+", confidence2)

            b=[int(i) for i in b]

           

            if (b[0]>=50):# 정확도가 60%가 넘으면

                client_socket.send("0") #블루투스로 아두이노에게 0을 보냄

                cv2.waitKey(3)

                time.sleep(5)
                print("dd")

                continue   

                   
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video

        if k == 27:

            break

    # Do a bit of cleanup

print("\n [INFO] Exiting Program and cleanup stuff")

cam.release()

cv2.destroyAllWindows()