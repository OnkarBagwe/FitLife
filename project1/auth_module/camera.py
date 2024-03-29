import cv2,os,urllib.request
import numpy as np
from django.conf import settings
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

kill1=False
killv=False
kill2=False
kill_q = False
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
image1 = None
extend_rep = True



class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	# def get_frame(self):
	# 	success, image = self.video.read()
	# 	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# 	frame_flip = cv2.flip(image,1)
	# 	ret, jpeg = cv2.imencode('.jpg', frame_flip)
	# 	return jpeg.tobytes()

	def get_frame(self):
		print("Hello")
		# cap = cv2.VideoCapture(0)
		with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
			while self.video.isOpened():
				global image
				ret, frame = self.video.read()

				# Recolor image to RGB
				image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				# image = cv2.resize(image, (1280, 720))
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

				VideoCamera.execute()       

				# frame_flip = cv2.flip(image,1)
				ret, jpeg = cv2.imencode('.jpg', image)
				return jpeg.tobytes()			  
			
	def calculate_angle(a,b,c):
		a = np.array(a) # First
		b = np.array(b) # Mid
		c = np.array(c) # End
		
		radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
		angle = np.abs(radians*180.0/np.pi)
		
		if angle >180.0:
			angle = 360-angle
			
		return angle 

	def quadrupule():
		print("start exercise")
		cv2.putText(image, 'Sit in a quadrupule position', (50,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
		temp=0
		while temp==0:
		
			angle1 = VideoCamera.calculate_angle(ankle_r, knee_r, hip_r)
			#print()
			angle2 = VideoCamera.calculate_angle(knee_r,hip_r, shoulder_r)
			angle3 = VideoCamera.calculate_angle(shoulder_r, elbow_r, wrist_r)
			angle4 = VideoCamera.calculate_angle(hip_r,shoulder_r,elbow_r)
			
			if(angle1 > 90 or angle1 < 60 or angle2 >110 or angle2 < 90 or angle3 < 160 or angle4 > 90 or angle4 <60 ):
				#cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
				#print(" hbs Hello P")
				cv2.putText(image, 'Not in proper quadrupule position', (50,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)

			else:
				temp=1
				#cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
				#print("hbs Heloo P")
				cv2.putText(image, ' Perfect', (50,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (120,120,120), 1, cv2.LINE_AA)
			
			ret, jpeg = cv2.imencode('.jpg', image)
			return jpeg.tobytes()	

			if kill_q==True:
				break    
                  
	def extend():
		#cv2.putText(image, 'Extend your left leg and your right arm', (50,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
		temp=0
		while temp==0:
			image1=image
			angle1 = VideoCamera.calculate_angle(ankle_r, knee_r, hip_r)#90
			#print()
			angle2 = VideoCamera.calculate_angle(knee_r,hip_r, shoulder_r)#90
			angle3 = VideoCamera.calculate_angle(shoulder_r, elbow_r, wrist_r) #180 
			angle4 = VideoCamera.calculate_angle(hip_r,shoulder_r,elbow_r)#180
			angle5 = VideoCamera.calculate_angle(ankle_l, knee_l, hip_l) #180
			angle6 = VideoCamera.calculate_angle(knee_l,hip_l, shoulder_l) #180
			angle7 = VideoCamera.calculate_angle(shoulder_l, elbow_l, wrist_l) #180 
			angle8 = VideoCamera.calculate_angle(hip_l,shoulder_l,elbow_l)#90
			
			
			
			"""if(angle1 > 100 or angle1 < 60 or angle2 >1300 or angle2 < 90 or angle7 < 165 or angle8 < 65 or angle8 >90 ):
				#cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
				#print(" hbs Hello P")
				extend_rep = False
				cv2.putText(image1, 'Not extended properly', (50,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255), 1, cv2.LINE_AA)"""


			if(angle3<160 or angle4<60 or angle5<160):
				extend_rep=False
				if(angle3<160) :
					#extend_rep = False
					cv2.putText(image1, 'Keep your right hand straight', (50,125), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)

				if(angle4<60) :
					#extend_rep = False
					cv2.putText(image1, 'Extend your right hand', (150,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)

				if(angle5<160):
					#extend_rep = False
					cv2.putText(image1, 'Keep your left leg straight', (150,125), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)

				"""if(angle6<160) :
					extend_rep = False
					cv2.putText(image1, 'Extend your left leg', (250,225), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)"""

				"""if(extend_rep):
					counter  = counter + 1
					extend_rep = False
					print(counter)
					cv2.putText(image1, counter
								, (250,225), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)"""
			else:
				extend_rep=True
				"""counter  = counter + 1
				print("count=",counter)"""
				temp=1
				"""cv2.putText(image1, counter
							, (250,225), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)"""
			
			"""else:
				temp=1
				#cv2.rectangle(image1, (0,0), (250,50), (245,117,16), -1)
				#print("hbs Heloo P")
				cv2.putText(image1, ' Perfect', (50,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (120,120,120), 1, cv2.LINE_AA)"""
		
	def execute():    
		tq= threading.Thread(target=VideoCamera.quadrupule)
		# tvc=threading.Thread(target=VideoCamera.video_capture)
		#te=threading.Thread(target=extend)
	
		# for i in range (1,20):
		# 	#print(i)
		# 	if i==1:
		# 		tvc.start()

		# 	if i==15: 
		# 		tq.start()
		sleep(1)

		# tq.join()
		#te.start()

		"""for i in range(1,11):
			print(i)
			if i == 10:
				kill2=True
			sleep(1)"""
		#kill2 = True
		""" for i in range(1,6):
			print("loop=", i)
			te1 = threading.Thread(target=extend)
			te1.start()
			te1.join()
			print("Extend thread start")
			sleep(2)
			tq1= threading.Thread(target=quadrupule)
			tq1.start()
			tq1.join()
			print("quad thread start")
			sleep(2)

		#kill2 = True    

		for i in range(1,4):
			#print(i)
			if i == 10:
				#kill1=True
				#kill2=True
				killv = True
			sleep(1) """

		# for i in range(1,4):
		# 	tq1= threading.Thread(target=quadrupule)
		# 	tq1.start()
		# 	tq1.join()
		# 	sleep(1)
			
		kill_q = True


		



