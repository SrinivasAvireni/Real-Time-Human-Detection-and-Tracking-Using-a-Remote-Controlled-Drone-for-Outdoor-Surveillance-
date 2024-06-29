from ultralytics import YOLO
import os

# Initialize the YOLO model
model = YOLO(r"C:\Users\srini\OneDrive\Desktop\Yolov8 Final\runs\detect\train42\weights\best.pt")

# Specify the image directory
img_directory = r"C:\Users\srini\OneDrive\Desktop\Camera Project\gd\igk_11802.jpg"

results = model(img_directory, save=True)

# Print the number of humans detected
print(len(results))


