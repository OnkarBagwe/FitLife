#!/usr/bin/env python
# coding: utf-8

# In[7]:


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


# In[8]:


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle


# In[9]:


kill1=False
killv=False
kill2=False
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
extend_rep = True

def video_capture():
    print("Hello")
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
            if killv ==True:
                break

        cap.release()
        """cv2.waitKey(0)
        cv2.destroyAllWindows()"""

def plank():
    temp=0
    while temp==0:
        image1=image
        angle1 = calculate_angle(wrist_r, elbow_r, shoulder_r)
        angle2 = calculate_angle(wrist_l, elbow_l, shoulder_l)

        #print("elbow in hand by side",elbow_r)
        angle3 = calculate_angle(ankle_r,knee_r, hip_r)
        angle4 = calculate_angle(ankle_l,knee_l,hip_l)
        angle5 = calculate_angle(elbow_l, shoulder_l, hip_l)
        angle6 = calculate_angle(elbow_r, shoulder_r, hip_r)
        
        if(angle1 > 100 or angle1 < 60 or angle2 >100 or angle2 < 60):
            cv2.putText(image1, 'Position your elbows directly beneath your shoulders.', (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            
        if(angle3<155 or  angle4<155):
            cv2.putText(image1, 'Keep your legs straight', (25,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)

        if (angle5>100 or angle5<60 or angle6>100 or angle6<60 ):
            cv2.putText(image1, 'keep your body straight', (25,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (225,255,255), 1, cv2.LINE_AA)

        if ((angle1<100 or angle1>60) and (angle2<100 or angle2>60) and angle3>155 and angle4>155 and (angle5<100 or angle5>60) and (angle6<100 or angle6>60)):
            cv2.putText(image1, 'Parfact! Keep it up', (25,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (225,255,255), 1, cv2.LINE_AA)

        if kill1==True:
            temp=1;
            break

def execute():

    tvc=threading.Thread(target=video_capture)
    tp=threading.Thread(target=plank)

    for i in range (1,32):
        print(i)
        if i==1:
            tvc.start()
        
        if i==30: 
            tp.start()
        sleep(1)
        
    for i in range(1,16):
        print(i)
        sleep(1)
        if i == 10: 
            kill1=True
            killv=True


# In[ ]:




