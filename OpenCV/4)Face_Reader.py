import cv2
import numpy as np
import os 

# === Replace this with your ESP32-CAM stream URL ===
ESP32_STREAM_URL = 'http://192.168.112.44/640x480.jpg'

# === Load Recognizer and Classifier ===
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

# === Names related to ID ===
names = ['None', 'Amith1', 'Amith2', 'Gayathri', 'Harry'] 

# === Use ESP32-CAM Stream ===
cam = cv2.VideoCapture(ESP32_STREAM_URL)
cam.set(3, 640)  # width
cam.set(4, 480)  # height

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()
    if not ret:
        print("[WARN] Unable to read from ESP32-CAM. Retrying...")
        continue

    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 100:
            id_text = names[id]
            confidence_text = "  {0}%".format(round(100 - confidence))
        else:
            id_text = "unknown"
            confidence_text = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(id_text), (x+5, y-5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence_text), (x+5, y+h-5), font, 1, (255, 255, 0), 1)

    cv2.imshow('ESP32-CAM Face Recognition', img)

    if cv2.waitKey(10) & 0xFF == 27:  # ESC key
        break

print("\n[INFO] Exiting Program and cleaning up.")
cam.release()
cv2.destroyAllWindows()
