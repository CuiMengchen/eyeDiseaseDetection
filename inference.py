import torch

# train
# python train.py --weights weights/yolov5m.pt --cfg models/yolov5m_eye.yaml --data data/eye.yaml --epoch 200 --batch-size 8 --img 640 --device 0
# python train.py --weights weights/yolov5l.pt --cfg models/yolov5l_eye_efficientnet.yaml --data data/eye.yaml --epoch 300 --batch-size 8 --img 640 --device 0

# Model
model = torch.hub.load('./', 'custom', 'best_eye.pt', source='local')

# Images
# img = 'dataset/images/train2017/8_left.jpg'  # or file, Path, PIL, OpenCV, numpy, list
img = 'myDataset/images/cataract_0050.png'
# Inference
results = model(img)


# Results

# a = results.save(save_dir="./run/exp")  # or .show(), .save(), .crop(), .pandas(), etc.
print(results.print())
print(results.xyxy[0][0][5] == 1)
print(results.pandas().xyxy[0])