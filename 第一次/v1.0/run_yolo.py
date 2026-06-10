import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ultralytics import YOLO
from pathlib import Path

# 用 ultralytics 自带的测试图片
assets_dir = Path("C:/Users/grr1997/AppData/Roaming/Python/Python313/site-packages/ultralytics/assets")
img_path = str(assets_dir / "bus.jpg")

# 加载刚刚下载的模型
model = YOLO("yolo11n.pt")
print("✅ 模型加载成功!")

# 运行检测
results = model(img_path, conf=0.25)

# 打印结果
boxes = results[0].boxes
print(f"\n检测到 {len(boxes)} 个目标:")
for i, box in enumerate(boxes):
    cls_id = int(box.cls[0])
    conf = float(box.conf[0])
    xyxy = box.xyxy[0].tolist()
    cls_name = model.names[cls_id]
    print(f"  [{i}] {cls_name:15s} 置信度={conf:.2f}")

# 保存结果
results[0].save("test_result.jpg")
print(f"\n✅ 检测结果已保存到 test_result.jpg")

# 特别关注自行车(bicycle, class_id=1)
bikes = [b for b in boxes if int(b.cls[0]) == 1]
if bikes:
    print(f"\n🚲 检测到 {len(bikes)} 辆自行车!")
else:
    print(f"\n📌 本图没有自行车，但模型已就绪")
    print(f"   支持 {len(model.names)} 个类别")

print(f"\n可用类别(前10个): {list(model.names.values())[:10]}")
