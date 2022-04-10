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
kill3=False
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
            global image,kill1,kill2,kill3,killv
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
        
            if (killv==True):
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
            cv2.putText(image1, 'Keep your hands by your side', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

        else:
            temp=1
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print("hbs Heloo P")
            cv2.putText(image1, ' hands Perfect', (50,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)


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
            cv2.putText(image1, 'Stand straight and keep your feet together', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

        else:
            temp=1
            #cv2.rectangle(image1, (500,0), (750,50), (245,117,16), -1)
            #print("ft Heloo P")
            cv2.putText(image1, ' legs Perfect', (50,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
            
def rightLegBend():
    temp=0
    while temp==0:
        image1=image
        #print("kneer in feet",knee_r)
        angle1 = calculate_angle(hip_r, knee_r, ankle_r)
        angle2 = calculate_angle(hip_l, knee_l, ankle_l)
        angle3 = calculate_angle( knee_l,hip_l, shoulder_l)

        if(angle1> 75) :
            #cv2.rectangle(image1, (500,0), (750,50), (245,117,16), -1)
            #print("ft Hello P")
            #print("Raise right leg properly")
            cv2.putText(image1, 'Raise right leg properly', (25,500), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
        if(angle2< 160) :
            #cv2.rectangle(image1, (500,0), (750,50), (245,117,16), -1)
            #print("ft Hello P")
            #print("Raise right leg properly 1")
            cv2.putText(image1, 'Keep your left leg straight', (700,500), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
        if(angle3<160) :
            #cv2.rectangle(image1, (500,0), (750,50), (245,117,16), -1)
            #print("ft Hello P")
            #print("Raise right leg properly 2")
            cv2.putText(image1, 'Stand Straight', (600,25), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
        if (kill1==True):
            break

def tadasana1():
    #print("last ")
    temp=0
    while temp==0:
        image1=image
        angle1 = calculate_angle(elbow_r, shoulder_r, hip_r)
        #print("elbow in hand by side",elbow_r)
        angle2 = calculate_angle(elbow_l,shoulder_l, hip_l)
        angle3 = calculate_angle(ankle_r,knee_r, hip_r)
        angle4 = calculate_angle(ankle_l,knee_l, hip_l)

        if(angle1 > 30 or angle2 > 30 or angle3< 160 or angle4 < 160):
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print(" hbs Hello P")
            cv2.putText(image1, 'Stand in tadasana ', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

        else:
            temp=1
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print("hbs Heloo P")
            cv2.putText(image1, ' Moving on', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
            
def leftLegBend():
    temp=0
    while temp==0:
        image1=image
        #print("kneer in feet",knee_r)
        angle1 = calculate_angle(hip_r, knee_r, ankle_r)
        angle2 = calculate_angle(hip_l, knee_l, ankle_l)
        angle3 = calculate_angle( knee_l,hip_l, shoulder_l)

        if(angle2> 75) :
            #cv2.rectangle(image1, (500,0), (750,50), (245,117,16), -1)
            #print("ft Hello P")
            print("Raise left leg properly 4")
            cv2.putText(image1, 'Raise left leg properly', (700,500), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
        if(angle1< 160) :
            #cv2.rectangle(image1, (500,0), (750,50), (245,117,16), -1)
            #print("ft Hello P")
            print("Raise left leg properly 5")
            cv2.putText(image1, 'Keep your right leg straight', (25,500), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
        if(angle3<160) :
            #cv2.rectangle(image1, (500,0), (750,50), (245,117,16), -1)
            #print("ft Hello P")
            print("Raise left leg properly 6")
            cv2.putText(image1, 'Stand Straight', (600,25), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
            
        if (kill2==True):
            break
def tadasana2():
    #print("last ")
    temp=0
    while temp==0:
        image1=image
        angle1 = calculate_angle(elbow_r, shoulder_r, hip_r)
        #print("elbow in hand by side",elbow_r)
        angle2 = calculate_angle(elbow_l,shoulder_l, hip_l)

        if (angle1 > 20 or angle2 > 20 or angle3< 160 or angle4 < 160):
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            print(" hbs Hellow P")
            cv2.putText(image1, 'Stand in tadasana ', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
            
        if (kill3==True):
            break
        
            
            
def execute():
    global killv,kill1,kill2,kill3
    thbs= threading.Thread(target=handsBySide)
    tft=threading.Thread(target=feetTogether)
    trlb = threading.Thread(target=rightLegBend)
    tvc=threading.Thread(target=video_capture)
    tt1=threading.Thread(target=tadasana1)
    tllb = threading.Thread(target=leftLegBend)
    tt2=threading.Thread(target=tadasana2)
    for i in range (1,22):
        print(i)
        if i==1:
            tvc.start()
        
        if i==20: 
            thbs.start()
        sleep(1)

    thbs.join()
    tft.start()
    tft.join()
    trlb.start()
    for i in range(1,11):
        if i==10:
            kill1 = True
        sleep(1)
    trlb.join()
    tt1.start()
    tt1.join()
    tllb.start()
    for i in range(1,11):
        if i==10:
            kill2 = True
        sleep(1)
    tllb.join()
    tt2.start()
    for i in range(1,11):
        print(i)
        if i == 10:
            kill3=True
            killv=True
        sleep(1)
    tt2.join()
    


# In[4]:




