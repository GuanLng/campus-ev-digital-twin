import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 试试 modelscope 或者 OpenI 下载
urls = [
    # 直接下载链接 - 用 curl 试试
    "https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt",
]

# 用 requests 试试
import subprocess
# 试试用 curl 加代理或直接访问
cmd = ["curl", "-L", "-o", "yolo11n.pt", "--connect-timeout", "10", urls[0]]
print(f"Running: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
print(result.stdout[-200:] if len(result.stdout) > 200 else result.stdout)
print(result.stderr[-200:] if len(result.stderr) > 200 else result.stderr)
if os.path.exists("yolo11n.pt") and os.path.getsize("yolo11n.pt") > 1000000:
    print(f"✅ 下载成功! 大小: {os.path.getsize('yolo11n.pt')} bytes")
else:
    print(f"❌ 下载失败或文件太小: {os.path.getsize('yolo11n.pt') if os.path.exists('yolo11n.pt') else 0} bytes")
