import cv2 

import numpy as np 
from PIL import Image

import os

# Path for face image database #사진경로설정

path = '/home/pi/dataset' #경로-dataset폴더

recognizer = cv2.face.LBPHFaceRecognizer_create() #LBPH를 사용할 새 변수 생성

detector = cv2.CascadeClassifier("/home/pi/haarcascade_frontalface_default.xml");


 

# function to get the images and label data

def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]    

    faceSamples=[]

    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale

        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])

        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:

            faceSamples.append(img_numpy[y:y+h,x:x+w]) #얼굴부분만 가져오기

            ids.append(id)

    return faceSamples,ids

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")

faces,ids = getImagesAndLabels(path) #matrix 만들기

recognizer.train(faces, np.array(ids)) #dataset폴더에 존재하는 이미지파일들을 불러와서 np.array로 만들고 이를 학습시킨다.

recognizer.write('trainer/trainer.yml') # trainer.yml파일로 저장한다.

# Print the numer of faces trained and end program

print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids)))) # 모든 학습이 끝나면 문장을 출력해준다.
