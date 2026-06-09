"""
校园电动车数字孪生监管系统 - 后端
运行：D:\Anaconda\python.exe app.py
然后在浏览器打开 http://localhost:5000
"""
import os, sys
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import Flask, jsonify, request, send_file, render_template
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# 加载YOLO模型
print("正在加载YOLO模型...")
model = YOLO("yolo11n.pt")
print("✅ YOLO模型加载完成")

# 预置图片列表
PRESET_IMAGES = [
    {"file": "图片/48c8577053cbc3f4cfe5f5ac15fe7fa3.jpg", "label": "校园场景1"},
    {"file": "edd8faeddb849e2b4106d30d5fa454be.jpg", "label": "校园场景2"},
    {"file": "车.jpg", "label": "校园场景3"},
]

# ========== API: 获取预置图片列表 ==========
@app.route("/api/images")
def get_images():
    results = []
    for img in PRESET_IMAGES:
        if os.path.exists(img["file"]):
            results.append({
                "file": img["file"],
                "label": img["label"],
                "url": f"/file/{img['file']}"
            })
    return jsonify(results)

# ========== API: YOLO检测单张图片 ==========
@app.route("/api/detect", methods=["POST"])
def detect_image():
    data = request.get_json()
    filepath = data.get("file", "")
    
    if not os.path.exists(filepath):
        return jsonify({"error": "文件不存在"}), 404
    
    results = model(filepath, conf=0.25)
    detections = []
    
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        cls_name = model.names[cls_id]
        detections.append({
            "class": cls_name,
            "confidence": round(conf, 3),
            "is_bicycle": cls_id == 1  # COCO中 bicycle=1
        })
    
    has_bicycle = any(d["is_bicycle"] for d in detections)
    
    return jsonify({
        "file": filepath,
        "detections": detections,
        "has_bicycle": has_bicycle
    })

# ========== 提供文件访问 ==========
@app.route("/file/<path:filepath>")
def serve_file(filepath):
    return send_file(filepath)

# ========== 主页 ==========
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 校园电动车数字孪生监管系统")
    print("   打开浏览器访问: http://localhost:5000")
    print("="*60)
    app.run(debug=True, host="0.0.0.0", port=5000)
