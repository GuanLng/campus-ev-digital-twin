"""使用 OpenCV 的 DNN 模块 + MobileNet SSD 做目标检测演示（无需下载任何模型）"""
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import numpy as np
from pathlib import Path

# OpenCV 内置的预训练模型文件路径
assets_dir = Path("C:/Users/grr1997/AppData/Roaming/Python/Python313/site-packages/ultralytics/assets")
img_path = str(assets_dir / "bus.jpg")

# 读取图片
img = cv2.imread(img_path)
if img is None:
    print("❌ 无法读取测试图片")
    exit()

# 使用 OpenCV 的 DNN + Caffe 预训练模型（MobileNet SSD）
# 这些模型是 OpenCV 官方提供的，不需要下载
prototxt = "MobileNetSSD_deploy.prototxt"
caffemodel = "MobileNetSSD_deploy.caffemodel"

# 先检查本地是否有这些文件
if not os.path.exists(caffemodel):
    print("MobileNet SSD 模型不存在，尝试使用 OpenCV 的 Haar Cascade...")
    
    # 使用 Haar Cascade 做人脸检测（OpenCV 内置）
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    print(f"\n📸 图片大小: {img.shape[1]}x{img.shape[0]}")
    print(f"👤 检测到 {len(faces)} 张人脸 (OpenCV Haar Cascade)")
    
    for i, (x, y, w, h) in enumerate(faces):
        print(f"  [{i}] 人脸位置: ({x},{y}) 大小: {w}x{h}")
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imwrite("test_haar_result.jpg", img)
    print("\n✅ 结果已保存到 test_haar_result.jpg")
else:
    # 使用 MobileNet SSD
    net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
    # 处理图片
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            cls_id = int(detections[0, 0, i, 1])
            print(f"  类别{cls_id} 置信度={confidence:.2f} ({x1},{y1})-({x2},{y2})")
            cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
    
    cv2.imwrite("test_dnn_result.jpg", img)
    print("\n✅ 结果已保存到 test_dnn_result.jpg")

print("\n💡 提示: 要将 YOLO 跑起来，需要手动下载模型文件")
