import cv2
import numpy as np
from mss import mss
import torch
import time

# Import YOLOv8 model from ultralytics
from ultralytics import YOLO

# Load custom YOLOv8 model
model_path = r"C:\Users\srini\OneDrive\Desktop\Yolov8 Final\runs\detect\train42\weights\last.pt"
model = YOLO(model_path)

bounding_box = {'top': 340, 'left': 800, 'width': 350, 'height': 400}

sct = mss()

# Desired frame rate
fps = 10  # Set lower FPS to reduce processing speed
delay = 1 / fps

# Enable OpenCL acceleration
cv2.ocl.setUseOpenCL(True)

while True:
    start_time = time.time()

    # Capture screen region
    sct_img = sct.grab(bounding_box)
    scr_img = np.array(sct_img)

    # Check if the image has an alpha channel (RGBA)
    if scr_img.shape[2] == 4:
        # Convert RGBA to RGB
        scr_img = cv2.cvtColor(scr_img, cv2.COLOR_RGBA2RGB)
    else:
        # Convert RGB to BGR
        scr_img = cv2.cvtColor(scr_img, cv2.COLOR_RGB2BGR)

    # Perform object detection with custom YOLOv8 model on the original image
    results = model(scr_img)

    # Get the first result object
    result = results[0]

    # Extract bounding boxes and confidence scores from the result object
    xyxy = result.boxes.xyxy.tolist()
    conf = result.boxes.conf.tolist()

    # Draw bounding boxes and labels on the original image
    for box, confidence in zip(xyxy, conf):
        cv2.rectangle(scr_img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
        cv2.putText(scr_img, f'Human:{confidence:.2f}', (int(box[0]), int(box[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the original image with bounding boxes and labels
    cv2.imshow('Testing', scr_img)

    elapsed_time = time.time() - start_time

    # Introduce a delay to achieve the desired frame rate
    if elapsed_time < delay:
        time.sleep(delay - elapsed_time)

    # Check for user input to quit
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

# Release all resources
cv2.destroyAllWindows()
