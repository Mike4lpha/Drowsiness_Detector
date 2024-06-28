import cv2 as cv
import mediapipe as mp
import FaceMeshModule as fmm
from scipy.spatial import distance as dist
import time
import RPi.GPIO as GPIO

buzzer=12

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)

def eye_aspect_ratio(eye):
    p2_minus_p6 = dist.euclidean(eye[1], eye[5])
    p3_minus_p5 = dist.euclidean(eye[2], eye[4])
    p1_minus_p4 = dist.euclidean(eye[0], eye[3])
    ear = (p2_minus_p6 + p3_minus_p5) / (2.0 * p1_minus_p4)
    return ear

cap=cv.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)

detector=fmm.FaceMeshDetector()
faces=[]

EAR_THRESHOLD = 0.26
WAIT_TIME = 5

state_tracker = { "start_time": time.perf_counter(), "DROWSY_TIME": 0.0}

while True:
    success, img=cap.read()
    img,faces=detector.findFaceMesh(img,draw=False)
    if len(faces)!=0:
        right_eye=[faces[0][362],faces[0][385],faces[0][387],faces[0][263],faces[0][373],faces[0][380]]
        left_eye=[faces[0][33],faces[0][160],faces[0][158],faces[0][133],faces[0][153],faces[0][144]]
        # print(left_eye)
        leftEAR = eye_aspect_ratio(left_eye)
        rightEAR= eye_aspect_ratio(right_eye)
        EAR=(leftEAR+rightEAR)/2.0

        if EAR < EAR_THRESHOLD:
            end_time = time.perf_counter()
            state_tracker["DROWSY_TIME"] += end_time - state_tracker["start_time"]
           
            if state_tracker["DROWSY_TIME"] >= WAIT_TIME:
                GPIO.output(buzzer, GPIO.HIGH)
                # cv.putText(img, "DROWSY!", (10,70), cv.FONT_HERSHEY_COMPLEX, 14, (255,255,0), 5)
                # print(0)
                
        else:
            state_tracker["start_time"] = time.perf_counter()
            state_tracker["DROWSY_TIME"] = 0.0
            # cv.putText(img, "NORMAL", (10,70), cv.FONT_HERSHEY_COMPLEX, 14, (255,255,0), 5)
            GPIO.cleanup(buzzer)
    
    cv.imshow("Image", img)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv.destroyAllWindows() 
