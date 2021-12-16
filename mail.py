import RPi.GPIO as GPIO #라즈베리파이 GPIO모듈

import time #제목에 들어갈 현재시간 time 모듈

from datetime import datetime #제목에 들어갈 현재시간 time 모듈

from picamera import PiCamera #pi카메라 모듈

import smtplib #메일 전송할때 필요한 모듈

from email.mime.text import MIMEText #메일 전송할때 필요한 모듈

from email.mime.base import MIMEBase #메일 전송할때 필요한 모듈

from email.mime.image import MIMEImage #메일 전송할때 필요한 모듈

from email.mime.multipart import MIMEMultipart #메일 전송할때 필요한 모듈

from email import encoders #메일 전송할때 필요한 모듈

GPIO.setmode(GPIO.BCM) #GPIO모듈셋팅

 

pirPin = 25 #pir센서가 라즈베리파이 GPIO25번에 연결되어 있음

GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)

camera = PiCamera() #카메라 모듈 변수설정

s = smtplib.SMTP('smtp.gmail.com', 587) #smtplib 포트번호와, 서버메일 설정
print('f')
s.starttls() #시작

s.login('yeerim0403@gmail.com', 'dwpfjpxggsvkobvj') #수신자 설정

now=datetime.now() #현재시간 변수now 설정

filename='image.jpg' #카메라 모듈 동작 시 사진촬영된 파일 이름


attachment=open(filename,'rb') #파일 가져오는 변수

while True:

       
    try:
        print('f2')
        if GPIO.input(pirPin) == GPIO.LOW: #pir센서가 동작할때
            print('f2')
            camera.start_preview() #카메라 동작
            camera.capture('/home/pi/image.jpg' ) #사진 촬영 및 저장경로 설정


 

            camera.start_recording('/home/pi/savevideo/%s.%s.%s %s:%s.h264'%(now.year,now.month,now.day,now.hour,now.minute)) #동영상 촬영 및 저장경로 설정

            time.sleep(5) #카메라 5초 휴식

            camera.stop_recording() #동영상 촬영 완료
            camera.stop_preview() #사진촬영 완료

            filename='image.jpg'

            attachment=open(filename,'rb')

            msg = MIMEMultipart() #메시지 설정 변수


 

            msg['Subject']="%s.%s.%s  %s:%s  Detected at the Door-LOCKLOCK "%(now.year,now.month,now.day,now.hour,now.minute) #메일이름 설정 _ 현재 년도, 날짜, 시간첨부

            part=MIMEBase('application','octet-stream')

   

            part.set_payload((attachment).read())


 

            encoders.encode_base64(part)


 

            part.add_header('Content-Disposition','attachment; filename='+filename)


 

            msg.attach(part)

            s.sendmail("peldmw@gmail.com", "gyr1094@naver.com", msg.as_string()) #메일보내기


 

            


 

 

    except:

           

            camera.stop_preview()

            time.sleep(3)

    