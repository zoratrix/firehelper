from ultralytics import YOLO
import cvzone
import cv2
import math
import serial

# УКАЗАТЬ COM порт к которому подключена arduino
arduino = serial.Serial('COM9', 115200)

# 0 и 1 могут поменяться на другие цифры (особенно если в системе есть еще 3-я вебкамера), cap1 = изображение с левой камеры, cap2 с правой
cap1 = cv2.VideoCapture(0)
model = YOLO('fire.pt')
cap2 = cv2.VideoCapture(1)

# Reading the classes
classnames = ['fire']



while True:
    ret1,frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    frame1 = cv2.resize(frame1,(640,480))
    frame2 = cv2.resize(frame2, (640, 480))
    result1 = model(frame1,stream=True)
    result2 = model(frame2, stream=True)

    # Getting bbox,confidence and class names informations to work with
    for info in result1:
         boxes = info.boxes
         for box in boxes:
             confidence = box.conf[0]
             confidence = math.ceil(confidence * 100)
             Class = int(box.cls[0])
             if confidence > 50:
                 x1,y1,x2,y2 = box.xyxy[0]
                 x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
                 cv2.rectangle(frame1,(x1,y1),(x2,y2),(0,0,255),5)
                 #в аргументе text отображаются координаты и подпись "fire", можно заменить на что то другое
                 cvzone.putTextRect(frame1, f'{classnames[Class]} x:{x1}, y:{y1}', [x1 + 8, y1 + 100], scale=1.5,thickness=1)
                 #coef = (x2-x1)/480 # не нужен
                 x_center = int(x1+(abs(x2 - x1) / 2) - 10) # центр огня Х, 10 = коэффициент расстояния между камерами (приблизительно разница по Х между картинками в пикселях)
                 y_center = int(y1+abs((y2 - y1) / 2)) # центр огня У
                 cv2.circle(frame2, (x_center, y_center), 0, (0, 0, 255), 5) # рисуем точку на 2 камере примерно там где огонь на 1 камере
                 arduino.write(str(int(x_center/10)).encode())




    cv2.imshow('frame1',frame1)
    cv2.imshow('frame2', frame2)
    cv2.waitKey(1)


