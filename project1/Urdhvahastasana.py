#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyttsx3
import threading
from time import *
import cv2
import os
import numpy as np
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


# In[2]:


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 


# In[3]:


kill1=False
kill2=False
killv=False
elbow_r = [0,0]
wrist_r = [0,0]
shoulder_r = [0,0]
knee_r = [0,0]
ankle_r = [0,0] 
hip_r = [0,0]
knee_l = [0,0]
ankle_l =[0,0]
hip_l = [0,0]
wrist_l = [0,0]
elbow_l = [0,0]
shoulder_l = [0,0]
foot_r = [0,0]
foot_l = [0,0]
image = None

def video_capture():
    #print("Hello")
    cap = cv2.VideoCapture(0)
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            global image
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (1280, 720))
            image.flags.writeable = False
            

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                global wrist_r,elbow_r,shoulder_r,knee_r,ankle_r,hip_r,knee_l,ankle_l,hip_l,wrist_l,elbow_l,shoulder_l,foot_r,foot_l
                # Get coordinates
                wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                foot_r = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
                foot_l = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
#                 print("elbow in vedio func",elbow_r)
                #handsBySide(self,elbow_r,shoulder_r,hip_r,elbow_l,shoulder_l,hip_l)

            except:
                pass


            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )               

            image = cv2.resize(image, (1280, 720))  
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        
            if killv==True:
                break

        cap.release()
        """cv2.waitKey(0)
        cv2.destroyAllWindows()"""

def handsBySide():
    #print("hand by side")
    temp=0
    while temp==0:
        image1=image
        angle1 = calculate_angle(elbow_r, shoulder_r, hip_r)
        #print("elbow in hand by side",elbow_r)
        angle2 = calculate_angle(elbow_l,shoulder_l, hip_l)
        
        if(angle1 > 20 or angle2 > 20):
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print(" hbs Hello P")
            cv2.putText(image1, 'Keep your hands by your side', (50,25), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

        else:
            temp=1
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print("hbs Heloo P")
            cv2.putText(image1, ' hands Perfect', (50,300), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)


def feetTogether():
    #print("feet")
    temp=0
    while temp==0:
        image1=image
        #print("kneer in feet",knee_r)
        angle1 = calculate_angle(knee_r, hip_r, hip_l)
        angle2 = calculate_angle(knee_l, hip_l, hip_r)

        if((angle1> 95) or (angle2 > 95)):
            #cv2.rectangle(image1, (500,0), (750,50), (245,117,16), -1)
            #print("ft Hello P")
            cv2.putText(image1, 'Stand straight and keep your feet together', (50,25), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

        else:
            temp=1
            #cv2.rectangle(image1, (500,0), (750,50), (245,117,16), -1)
            #print("ft Heloo P")
            cv2.putText(image1, ' legs Perfect', (50,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

def Urdhvahastasana():
    temp=0
    while temp==0:
        image1=image
        angle1= calculate_angle(wrist_l, elbow_l, shoulder_l)
        angle2= calculate_angle(wrist_r, elbow_r, shoulder_r)
        angle3= calculate_angle(elbow_l, shoulder_l, hip_l)
        angle4= calculate_angle(elbow_r, shoulder_r, hip_r)
        angle5 = calculate_angle(knee_r, hip_r, hip_l)
        angle6 = calculate_angle(knee_l, hip_l, hip_r)
        
        if angle1 < 170 or angle2<170:
            #cv2.rectangle(image, (0,0), (200,50), (245,117,16), -1)
            cv2.putText(image1,'Your arms should be straight', (50,25), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

        if angle3 < 170 or angle4 < 170:
            #cv2.rectangle(image, (250,0), (450,50), (245,117,16), -1)
            cv2.putText(image1,'arms should be vertical and straight', (50,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

        if angle5 > 95 or angle6 > 95 :
            #cv2.rectangle(image, (0,250), (200,300), (245,117,16), -1)
            cv2.putText(image1,'legs should be straight', (50,325), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

        if(angle1>170 and angle2>170 and angle3>170 and angle4>170 and angle5<95 and angle6<95):
            cv2.putText(image1,'Good Job', (50,500), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
        
        if kill1==True:
            break

def tadasana():
    #print("last ")
    temp=0
    while temp==0:
        image1=image
        angle1 = calculate_angle(elbow_r, shoulder_r, hip_r)
        #print("elbow in hand by side",elbow_r)
        angle2 = calculate_angle(elbow_l,shoulder_l, hip_l)
        angle3 = calculate_angle(knee_r, hip_r, hip_l)
        angle4 = calculate_angle(knee_l, hip_l, hip_r)

        if(angle1 > 20 or angle2 > 20 or angle3> 95 or angle4 > 95):
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print(" hbs Hello P")
            cv2.putText(image1, 'Keep your hands by your side, feet together, in tadasana ', (50,25), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

        else:
            temp=1
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print("hbs Heloo P")
            cv2.putText(image1, ' aasan finish', (50,25), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
        
        if kill2==True:
            break



def execute():
    global kill1,kill2,killv
    thbs= threading.Thread(target=handsBySide)
    tft=threading.Thread(target=feetTogether)
    tvc=threading.Thread(target=video_capture)
    tu=threading.Thread(target=Urdhvahastasana)
    tt=threading.Thread(target=tadasana)

    for i in range (1,22):
        print(i)
        if i==1:
            tvc.start()
        
        if i==20: 
            thbs.start()
        sleep(1)

    thbs.join()
    sleep(2)
    tft.start()
    tft.join()
    sleep(2)
    tu.start()

    for i in range(1,11):
        print(i)
        if i == 10:
            kill1=True
        sleep(1)

    tu.join()
    tt.start()
    for i in range(1,11):
        print(i)
        if i == 10:
            kill2=True
            killv=True
        sleep(1)

    #print("finally done")


# In[ ]:




