import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 方案1: 用 modelscope 的 snapshot_download
from modelscope.hub.snapshot_download import snapshot_download
from modelscope.hub.api import HubApi

# YOLO11n 在 modelscope 上可能的路径
# 先搜索一下
try:
    api = HubApi()
    # 尝试直接下载 yolov8 模型 (modelscope 上有)
    model_dir = snapshot_download("ultralytics/yolo11n", cache_dir="./modelscope_cache")
    print(f"下载到: {model_dir}")
    import glob
    pt_files = glob.glob(os.path.join(model_dir, "**", "*.pt"), recursive=True)
    print(f"找到 .pt 文件: {pt_files}")
except Exception as e:
    print(f"❌ 方案1失败: {e}")

print("\n--- 尝试方案2: 直接URL下载 ---")
# 方案2: 用 python requests 通过代理或直接下载
import requests

urls = [
    "https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt",
]

for url in urls:
    try:
        print(f"下载 {url}...")
        r = requests.get(url, timeout=30, allow_redirects=True, 
                        headers={"User-Agent": "Mozilla/5.0"})
        with open("yolo11n.pt", "wb") as f:
            f.write(r.content)
        size_mb = len(r.content) / 1024 / 1024
        print(f"✅ 下载成功! 大小: {size_mb:.1f} MB")
        break
    except Exception as e:
        print(f"  ❌ 失败: {e}")
