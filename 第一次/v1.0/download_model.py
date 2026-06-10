import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import urllib.request

# 尝试多个镜像源下载 yolo11n.pt
urls = [
    "https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt",
    "https://hf-mirror.com/ultralytics/yolo11n/resolve/main/yolo11n.pt",
    "https://huggingface.co/ultralytics/yolo11n/resolve/main/yolo11n.pt",
]

for url in urls:
    try:
        print(f"Trying: {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            with open("yolo11n.pt", "wb") as f:
                f.write(response.read())
        print("✅ 下载成功!")
        break
    except Exception as e:
        print(f"  ❌ 失败: {e}")
else:
    print("\n❌ 所有源都下载失败。请手动下载模型放到当前目录。")
    print("   下载地址: https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt")
