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
killc=False
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

"""def Calling():
    temp=0
    while(temp==0):
        image1=image
        if(True):
            cv2.putText(image1, 'Turn to your left and stand straight', (150,50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)

        if killc==True:
            break"""
        
"""def StandStraight1():
    #print("hand by side")
    temp=0
    while temp==0:
        image1=image
        angle1 = calculate_angle(ankle_r,knee_r,hip_r)
        #print("elbow in hand by side",elbow_r)
        angle2 = calculate_angle(shoulder_r, hip_r,knee_r)
        angle3 = calculate_angle(wrist_r,elbow_r,shoulder_r)
        
        if(angle1<160 and angle2<160):
            cv2.putText(image1, 'Please Stand Straight', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
        
            
        else:
            temp=1
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print("hbs Heloo P")
            cv2.putText(image1, ' Moving on', (50,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)"""
            
def BendRightForward():
    temp=0
    while temp==0:
        image1=image
        angle1 = calculate_angle(ankle_r,knee_r,hip_r)
        #print("elbow in hand by side",elbow_r)
        angle2 = calculate_angle(ankle_l,knee_l,hip_l)
        angle3 = calculate_angle(knee_r,hip_r,shoulder_r)
        print("Right")
        
        if(angle1>110 or angle1<75):
            cv2.putText(image1, 'Bend your right leg forward ', (750,300), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
        
        #if(angle3<90):
            #print("Back")
            #cv2.putText(image1, 'Your Back should be straight ', (150,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
        
        else:
            temp=1
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print("hbs Heloo P")
            #cv2.putText(image1, ' Moving on', (50,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
        """if(angle2>115):
            print("Left")
            cv2.putText(image1, 'Bend your left leg ', (150,300), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)    
        
        if(angle3<150):
            print("Back")
            cv2.putText(image1, 'Your Back should be straight ', (150,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)"""
            
def StandStraight2():
    #print("hand by side")
    temp=0
    while temp==0:
        image1=image
        angle1 = calculate_angle(ankle_r,knee_r,hip_r)
        #print("elbow in hand by side",elbow_r)
        angle2 = calculate_angle(shoulder_r, hip_r,knee_r)
        angle3 = calculate_angle(wrist_r,elbow_r,shoulder_r)
        
        if(angle1<160 and angle2<160):
            cv2.putText(image1, 'Please Stand Straight', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
        
            
        else:
            temp=1
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print("hbs Heloo P")
            #cv2.putText(image1, ' Moving on', (50,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
"""def BendLeftForward():
    temp=0
    while temp==0:
        image1=image
        angle1 = calculate_angle(ankle_l,knee_l,hip_l)
        #print("elbow in hand by side",elbow_r)
        angle2 = calculate_angle(ankle_r,knee_r,hip_r)
        angle3 = calculate_angle(knee_r,hip_r,shoulder_r)
        print("Left")
        
        if(angle1>110 or angle1<75):
            print("Left left")
            cv2.putText(image1, 'Bend your left leg forward ', (750,300), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
        
        if(angle2>115):
            cv2.putText(image1, 'Bend your right leg ', (150,300), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)    
        
        if(angle3<150):
            cv2.putText(image1, 'Your Back should be straight ', (150,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA) 
        
        else:
            temp=1
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print("hbs Heloo P")
            #cv2.putText(image1, ' Moving on', (50,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
            
            
def StandStraight3():
    #print("hand by side")
    temp=0
    while temp==0:
        image1=image
        angle1 = calculate_angle(ankle_r,knee_r,hip_r)
        #print("elbow in hand by side",elbow_r)
        angle2 = calculate_angle(shoulder_r, hip_r,knee_r)
        angle3 = calculate_angle(wrist_r,elbow_r,shoulder_r)
        print("SS3")
        
        if(angle1<160 and angle2<160):
            cv2.putText(image1, 'Please Stand Straight', (50,50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)
        
            
        else:
            temp=1
            #cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
            #print("hbs Heloo P")
            #cv2.putText(image1, ' Moving on', (50,175), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0,0,0), 1, cv2.LINE_AA)"""           
            
            
def execute():
    global killv,kill1,kill2,kill3,killc
    #tc=threading.Thread(target=Calling)
    tvc=threading.Thread(target=video_capture)
    
    for i in range (1,16):
        print(i)
        if i==1:
            tvc.start()
        sleep(1)
        """if i==20:
            tc.start()
            sleep(1)
        if i==25:
            killc=True
        sleep(1)
    tc.join()"""
    
    for i in range(1,3):
        """tss1=threading.Thread(target=StandStraight1)
        tss1.start()
        tss1.join()
        sleep(2)"""
        print("Right thread")
        tbrf=threading.Thread(target=BendRightForward)
        tbrf.start()
        sleep(2)
        tbrf.join()
        sleep(2)
        print("Stand 2")
        tss2=threading.Thread(target=StandStraight2)
        tss2.start()
        sleep(2)
        tss2.join()
        sleep(2)
        
    for i in range(1,6):
        print(i)
        if i == 5:
            killv=True
        sleep(1)


# In[4]:




