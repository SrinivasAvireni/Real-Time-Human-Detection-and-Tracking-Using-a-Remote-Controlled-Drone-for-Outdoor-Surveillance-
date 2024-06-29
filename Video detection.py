import cv2
from ultralytics import YOLO

# Load yolov8 model
model = YOLO(r"C:\Users\srini\OneDrive\Desktop\Yolov8 Final\runs\detect\train42\weights\last.pt")

# Load video
video_path = r"C:\Users\srini\Downloads\Untitled video - Made with Clipchamp (17).mp4"
cap = cv2.VideoCapture(video_path)

# Enable OpenCL acceleration
cv2.ocl.setUseOpenCL(True)

# Get video frame rate
frame_rate = cap.get(cv2.CAP_PROP_FPS)

# Create a video writer object
output_width, output_height = 640, 480 # Set your desired output resolution
video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), frame_rate, (output_width, output_height))

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
  results = model.track(frame, persist=True)

  # Resize frame to the desired output resolution
  frame_resized = cv2.resize(results[0].plot(), (output_width, output_height))

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
