import cv2
import numpy as np
import mediapipe as mp
import time
import math

# I have used mediapipe module for this project.
# To get more informtion of mediapipe visit "https://google.github.io/mediapipe/"

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

#pTime = 0

count = -1
position = 'up'

cap = cv2.VideoCapture('Pushup_2.mp4')

print("Press q to exit.")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Can't receive frame. Exiting.")
        break
    
    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Get the pose and landmark inofrmation of whole body.
    result = pose.process(frame_RGB)
    
    if result.pose_landmarks:
        # Get landmark position and show them in video.
        mpDraw.draw_landmarks(frame, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for ids, lm in enumerate(result.pose_landmarks.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
            
            # 11, 13, 15 are the landmark ids for left sholder, elbow and arm respectively
            if ids == 11:
                lm_11_x, lm_11_y = lm.x , lm.y
            if ids == 13:
                lm_13_x, lm_13_y = lm.x, lm.y                
            if ids == 15:
                lm_15_x, lm_15_y = lm.x, lm.y

        (a_x, a_y) = (lm_11_x - lm_13_x, lm_11_y - lm_13_y)
        (b_x, b_y) = (lm_15_x - lm_13_x, lm_15_y - lm_13_y)

        mod_a = ((a_x**2) + (a_y**2))**(1/2)
        mod_b = ((b_x**2) + (b_y**2))**(1/2)

        # Get angle between upper arm and lower arm.
        theta = math.degrees(round(math.acos(round(((a_x*b_x + a_y*b_y)/(mod_a * mod_b)),4)),3))

        #print('theta_degree: ', theta)

        if theta > 160 and position == 'up':
            count += 1
            position = 'down'

        if theta < 100 and position == 'down':
            position = 'up'
    
    # Get fps information of a video.
    #cTime = time.time()
    #fps = 1 / (cTime - pTime)
    #pTime = cTime
    
    #cv2.putText(frame, f'fps = {str(int(fps))}', (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0, 0), 3)
    cv2.putText(frame, f'Pushup count = {str(int(count))}', (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0, 0), 3)
    
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()