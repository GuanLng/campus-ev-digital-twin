"""
USB摄像头实时检测 - 你的电动车检测核心脚本
运行：D:\Anaconda\python.exe detect_camera.py
按 q 键退出
"""
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ultralytics import YOLO
import cv2

# 加载模型
model = YOLO("yolo11n.pt")

# 打开USB摄像头 (0=默认摄像头)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ 摄像头打开失败，检查是否已插入")
    exit()

print("✅ 摄像头已打开")
print("📸 把电动车停在摄像头前，看 YOLO 能不能识别出来")
print("   按 q 键退出\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 检测（只检测 bicycle 效果更好，也可以检测所有）
    results = model(frame, classes=[1])  # classes=[1] 只检测 bicycle

    # 绘制结果
    annotated = results[0].plot()

    # 显示
    cv2.imshow("YOLO Detection - 按q退出", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
