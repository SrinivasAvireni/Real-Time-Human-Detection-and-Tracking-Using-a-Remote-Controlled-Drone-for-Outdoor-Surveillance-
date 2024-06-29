from ultralytics import YOLO

# load model

model = YOLO(r'C:\Users\srini\OneDrive\Desktop\Yolov8 Final\runs\detect\train\weights\last.pt')
model.resume = True
#Training model for additional 1 epochs

results = model.train(data="custom.yaml", epochs=30)
