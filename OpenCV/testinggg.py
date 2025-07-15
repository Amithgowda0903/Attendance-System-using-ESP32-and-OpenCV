import cv2

# Use OpenCV's built-in MJPEG stream reader
url = 'http://192.168.29.185:81/stream'
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("[ERROR] Cannot open ESP32 stream.")
    exit()

print("[INFO] Streaming started. Press ESC to exit.")

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("[WARN] Failed to grab frame.")
        continue

    cv2.imshow("ESP32-CAM Live", frame)

    if cv2.waitKey(10) & 0xFF == 27:
        print("[INFO] ESC pressed. Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
