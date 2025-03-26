import cv2
from ultralytics import YOLO
import serial
import time

# Set up serial communication (adjust 'COM3' to your port and baud rate to match Arduino)
arduino = serial.Serial('COM11', 9600)  # For Windows use COM port (e.g., COM3), for Linux use '/dev/ttyUSB0'
time.sleep(2)  # Wait for the connection to establish

# Load the YOLO model
model = YOLO("last.pt")

# Open the video file (0 for webcam)
video_path = 2
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO inference on the frame
        results = model(frame)

        # Initialize counters for people and cars
        violence_cnt = len(results[0].boxes)

        # Send the violence count to the Arduino
        arduino.write(f"{violence_cnt}\n".encode())  # Send the count as a string followed by a newline

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the counts on the frame
        cv2.putText(annotated_frame, f"violence count: {violence_cnt}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if(violence_cnt):
            cv2.putText(annotated_frame, f"Warning! Violence Detection", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the annotated frame
        cv2.imshow("Violence Detection", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

# Close the serial communication
arduino.close()
