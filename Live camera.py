import cv2
from ultralytics import YOLO
from datetime import datetime  # Import the datetime module

# Load YOLOv8 model
model = YOLO(r"C:\Users\srini\OneDrive\Desktop\Yolov8 Final\runs\detect\train42\weights\last.pt")

# Open camera
cap = cv2.VideoCapture(0)

# Get video frame rate
frame_rate = cap.get(cv2.CAP_PROP_FPS)

# Get video frame size
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set output video resolution
output_width = 640
output_height = 514

# Generate a dynamic output video filename based on the current timestamp
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
output_filename = f'output_{current_time}.mp4'

# Create a video writer object with the dynamic filename, resolution, and frame rate
video_writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'MP4V'), frame_rate, (output_width, output_height))

# Read frames
while True:
    # Capture the next frame from the camera
    ret, frame = cap.read()

    # Check if the frame is empty
    if frame is None:
        break

    # Rotate the frame by 180 degrees
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # Detect and track objects
    results = model.track(frame, persist=True)

    # Extract bounding boxes and confidence scores
    xyxy = results[0].boxes.xyxy.tolist()
    conf = results[0].boxes.conf.tolist()

    # Draw bounding boxes and labels on the original image
    for box, confidence in zip(xyxy, conf):
        # Convert coordinates to integers
        box = [int(coord) for coord in box]
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        cv2.putText(frame, f'Human:{confidence:.2f}', (box[0], box[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Resize frame to the desired output resolution
    frame = cv2.resize(frame, (output_width, output_height))

    # Write frame to video
    video_writer.write(frame)

    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release all resources
cap.release()
video_writer.release()
cv2.destroyAllWindows()
