import cv2
import numpy as np
from datetime import datetime

# Load face recognizer and Haar cascade
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Replace with your actual ID-name mapping
names = ['None', 'Amith1', 'Amith2', 'Gayathri', 'Harry']  # ID 1 = Amith

# Open the video stream
url = 'http://10.4.122.200:81/stream'
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("[ERROR] Cannot open ESP32 stream.")
    exit()

font = cv2.FONT_HERSHEY_SIMPLEX

def markAttendance(name):
    try:
        with open('Attendance.csv', 'a+') as f:
            f.seek(0)
            lines = f.readlines()
            nameList = [line.strip().split(',')[0] for line in lines]
            if name not in nameList:
                now = datetime.now()
                f.write(f'\n{name},{now.strftime("%H:%M:%S")}')
                print(f"[INFO] Marked attendance for {name}")
    except Exception as e:
        print(f"[ERROR] Could not mark attendance: {e}")

print("[INFO] Starting Face Recognition Stream...")

while True:
    ret, frame = cap.read()

    if not ret:
        print("[WARN] Failed to grab frame.")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 100:
            name = names[id] if id < len(names) else "Unknown"
            confidence_text = f"{round(100 - confidence)}%"
            markAttendance(name)
        else:
            name = "Unknown"
            confidence_text = f"{round(100 - confidence)}%"

        cv2.putText(frame, str(name), (x+5, y-5), font, 1, (255, 255, 255), 2)
        cv2.putText(frame, str(confidence_text), (x+5, y+h-5), font, 1, (255, 255, 0), 1)

    cv2.imshow('ESP32-CAM Face Recognition', frame)

    if cv2.waitKey(10) & 0xFF == 27:  # ESC to quit
        print("[INFO] ESC pressed. Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
