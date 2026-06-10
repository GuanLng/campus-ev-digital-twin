"""
完整版：YOLO 检测 + 违规停放判断
先点4个点标停车位，再跑检测

操作：
  鼠标左键点4下 → 标出停车位四个角
  按 q 退出
  按 r 重新标定
  按 d 开始/暂停检测
"""
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ultralytics import YOLO
import cv2
import numpy as np

# 全局变量
points = []          # 存储点击的坐标
parking_zone = None  # 最终的多边形
detect_mode = False  # 是否开始检测

# 鼠标回调函数
def mouse_callback(event, x, y, flags, param):
    global points, parking_zone, detect_mode
    if event == cv2.EVENT_LBUTTONDOWN and not detect_mode:
        points.append((x, y))
        print(f"  点击 {len(points)}: ({x}, {y})")
        if len(points) == 4:
            parking_zone = np.array(points, dtype=np.int32)
            print(f"\n✅ 停车位标定完成！四个角坐标:")
            for i, p in enumerate(points):
                print(f"    角{i+1}: {p}")
            print("\n按 d 开始检测 | 按 r 重新标定 | 按 q 退出")

# 加载模型
model = YOLO("yolo11n.pt")

# 打开摄像头
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ 摄像头打开失败，试试 cv2.VideoCapture(1)")
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("❌ 仍然失败，检查摄像头驱动")
        exit()

print("\n" + "="*50)
print("🟡 第1步：标定停车位")
print("   在画面上依次点击停车位的 4 个角")
print("   (建议按顺时针或逆时针顺序)")
print("="*50)

cv2.namedWindow("标定停车位 - 点4个角")
cv2.setMouseCallback("标定停车位 - 点4个角", mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 画已点击的点
    for i, p in enumerate(points):
        cv2.circle(frame, p, 6, (0, 255, 255), -1)
        cv2.putText(frame, str(i+1), (p[0]+10, p[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # 画多边形（如果有4个点）
    if parking_zone is not None:
        cv2.polylines(frame, [parking_zone], True, (0, 255, 255), 3)
        cv2.putText(frame, "PARKING ZONE", (parking_zone[0][0], parking_zone[0][1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # 检测模式
    if detect_mode and parking_zone is not None:
        results = model(frame, classes=[1], conf=0.3)

        total = 0
        violations = 0

        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

            # 判断是否在停车位内
            inside = cv2.pointPolygonTest(parking_zone, (cx, cy), False) >= 0
            color = (0, 255, 0) if inside else (0, 0, 255)
            label = "✅ OK" if inside else "❌ VIOLATION"
            if not inside:
                violations += 1
            total += 1

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, label, (int(x1), int(y1)-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            cv2.circle(frame, (cx, cy), 4, color, -1)

        # 统计
        cv2.putText(frame, f"Total: {total}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"Violations: {violations}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # 操作提示
    mode_text = "🔴 检测中" if detect_mode else "🟡 标定模式"
    cv2.putText(frame, mode_text, (10, frame.shape[0]-20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("标定停车位 - 点4个角", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        points = []
        parking_zone = None
        detect_mode = False
        print("🔄 已重置，重新标定停车位")
    elif key == ord('d') and parking_zone is not None:
        detect_mode = not detect_mode
        print(f"{'▶️ 开始检测' if detect_mode else '⏸️ 暂停检测'}")

cap.release()
cv2.destroyAllWindows()
