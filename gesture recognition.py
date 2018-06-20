import cv2
import numpy as np
import time 
import math
import serial
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
ab =0
q=0
ser=serial.Serial("COM8",9600)
time.sleep(1)
while True:
    q = 0
    ret,frame = cap.read()
    ret,frame2 = cap.read()

    count = 0
    hsv = cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)
    hmin = np.array([70,70,70],np.uint8)
    hmax = np.array([70,70,70],np.uint8)
    thresh2 = cv2.inRange(hsv,hmin,hmax)

    
    fgmask = fgbg.apply(frame)
    blur = cv2.GaussianBlur(fgmask,(25,25),0)
    ret,thresh = cv2.threshold(blur,100,255,0)
    final = cv2.bitwise_and(frame,frame,mask=thresh)
    cv2.imshow('final',final)
    cv2.imshow('thresh',thresh)
    area =0
    im2,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    try:
        max = cv2.contourArea(contours[0])
        for index in range(len(contours)):
           if cv2.contourArea(contours[index]) > max:
              max = cv2.contourArea(contours[index])
              ab = index
        cv2.drawContours(thresh2, contours, ab, (255,255,255), -1)
        cnt = contours[ab]
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull)
        
        if defects != None:
         for i in range(defects.shape[0]):
           s,e,f,d = defects[i,0]
           start = tuple(cnt[s][0])
           end = tuple(cnt[e][0])
           far = tuple(cnt[f][0])
           cv2.line(frame,start,end,[0,255,0],2)
           cv2.circle(frame,far,5,[0,255,255],-1)
           a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
           b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
           c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
           angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
           if angle <= (math.pi / 2 ):  # angle less than 90 degree, treat as fingers
                        count += 1
                        cv2.circle(frame, far, 8, [255, 255, 0], -1)      
    except:
       print("Sorry")
       q=1
       ser.write('0')
    cv2.imshow('frame',frame)
    cv2.imshow('thresh2',thresh2)
    if q!=1:
       print(count+1)
       if (count+1)==1:
           ser.write('1')
       if (count+1)==2:
           ser.write('2')
       if (count+1)==3:
           ser.write('3')
       if (count+1)==4:
           ser.write('4')
       if (count+1)==5:
           ser.write('5')    
    k = cv2.waitKey(1) & 0xff
    if k ==27:
        break

cap.release()
cv2.destroyAllWindows()
    
