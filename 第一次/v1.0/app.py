"""
校园电动车数字孪生监管系统 - 后端
运行：D:\Anaconda\python.exe app.py
然后在浏览器打开 http://localhost:5000
"""
import os, sys, time, urllib.request

# 修复Windows终端GBK编码不支持emoji的问题
if sys.stdout.encoding and "utf" not in sys.stdout.encoding.lower():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        os.environ["PYTHONIOENCODING"] = "utf-8"

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import Flask, jsonify, request, send_file, render_template
import cv2
import numpy as np

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# ---------- YOLO模型下载辅助函数 ----------
MODEL_FILE = "yolo11n.pt"
MODEL_URLS = [
    # 国内镜像加速
    "https://ghp.ci/https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt",
    "https://mirror.ghproxy.com/https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt",
    "https://github.moeyy.xyz/https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt",
    # 官方源
    "https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt",
]

def download_model():
    """尝试从多个源下载模型，返回是否成功"""
    if os.path.exists(MODEL_FILE) and os.path.getsize(MODEL_FILE) > 1024:
        return True

    for url in MODEL_URLS:
        try:
            print(f"⏳ 尝试下载模型: {url}")
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            with urllib.request.urlopen(req, timeout=120) as resp:
                with open(MODEL_FILE, "wb") as f:
                    f.write(resp.read())
            size_mb = os.path.getsize(MODEL_FILE) / 1024 / 1024
            if size_mb > 1:
                print(f"✅ 模型下载成功！大小: {size_mb:.1f} MB")
                return True
            else:
                os.remove(MODEL_FILE)
                print(f"  文件太小({size_mb:.1f} MB)，重试其他源...")
        except Exception as e:
            print(f"  下载失败: {str(e)[:80]}")
            time.sleep(1)
    return False

# ---------- 加载YOLO模型 ----------
model = None
print("正在加载YOLO模型...")

# 优先尝试直接加载（模型已存在时）
if os.path.exists(MODEL_FILE) and os.path.getsize(MODEL_FILE) > 1024:
    try:
        from ultralytics import YOLO
        model = YOLO(MODEL_FILE)
        print("✅ YOLO模型加载完成")
    except Exception as e:
        print(f"模型加载失败: {e}")
        model = None
else:
    print("模型文件不存在，尝试自动下载...")
    if download_model():
        try:
            from ultralytics import YOLO
            model = YOLO(MODEL_FILE)
            print("✅ YOLO模型加载完成")
        except Exception as e:
            print(f"模型加载失败: {e}")
            model = None
    else:
        print("⚠️ 模型下载失败，检测功能将不可用。")
        print("   请手动下载放到当前目录：")
        print("   https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt")

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
    if model is None:
        return jsonify({"error": "模型未加载，请先下载 yolo11n.pt"}), 503

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
