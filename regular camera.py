import cv2
from ultralytics import YOLO
import torch

# Load yolov8 model with single class (person)
model = YOLO(r"C:\Users\srini\Downloads\yolov8n_person.pt")

# Load video
video_path = r"C:\Users\srini\Downloads\Untitled video - Made with Clipchamp (17).mp4"
cap = cv2.VideoCapture(video_path)

# Enable OpenCL acceleration
cv2.ocl.setUseOpenCL(True)

# Get video frame rate
frame_rate = cap.get(cv2.CAP_PROP_FPS)

# Create a video writer object
output_width, output_height = 640, 480  # Set your desired output resolution
video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'H264'), frame_rate, (output_width, output_height))

# Process frames
skip_frames = 2
frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    if frame_count % skip_frames != 0:
        continue

    # Detect and track objects
    results = model.track(frame, classes=["person"], persist=True)

    # Draw bounding boxes and labels on the original image for the "person" class
    for box, confidence, class_id in zip(results.xyxy, results.conf, results.classes.int()):
        if class_id == 0:  # Check if the detected class is "person"
            # Convert coordinates to integers
            box = [int(coord) for coord in box]
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            cv2.putText(frame, f'Person:{confidence:.2f}', (box[0], box[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Resize frame to the desired output resolution
    frame_resized = cv2.resize(frame, (output_width, output_height))

    # Write frame to video
    video_writer.write(frame_resized)

    # Visualize
    cv2.imshow('frame', frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release all resources
cap.release()
video_writer.release()
cv2.destroyAllWindows()
