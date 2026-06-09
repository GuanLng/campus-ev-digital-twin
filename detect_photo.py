"""
使用方法：
1. 用手机在校园里拍一张电动车的照片
2. 微信传到电脑，放到本目录
3. 修改下面的 IMAGE_PATH 为你的照片文件名
4. 运行：D:\Anaconda\python.exe detect_photo.py
"""
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ultralytics import YOLO

# ===== 修改这里 =====
IMAGE_PATH = "图片/48c8577053cbc3f4cfe5f5ac15fe7fa3.jpg"   # ← 改成你的照片文件名
# ===================

# 加载模型
model = YOLO("yolo11n.pt")

# 检测
results = model(IMAGE_PATH)

# 打印检测结果
boxes = results[0].boxes
print(f"\n检测到 {len(boxes)} 个目标:")
for i, box in enumerate(boxes):
    cls_id = int(box.cls[0])
    conf = float(box.conf[0])
    xyxy = box.xyxy[0].tolist()
    cls_name = model.names[cls_id]
    print(f"  [{i}] {cls_name:15s} 置信度={conf:.2f}  位置=({xyxy[0]:.0f},{xyxy[1]:.0f})-({xyxy[2]:.0f},{xyxy[3]:.0f})")

# 保存结果（会在图片上画出框）
output_name = IMAGE_PATH.rsplit(".", 1)[0] + "_result.jpg"
results[0].save(output_name)
print(f"\n✅ 结果已保存到: {output_name}")
