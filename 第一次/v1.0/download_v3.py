"""尝试多个国内源下载 YOLO 模型"""
import os, sys
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import requests

# 国内常见镜像/站点
urls = [
    # 直接从 github releases 下载 (requests 有时比 urllib 更友好)
    "https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt",
    # 试试不同镜像站
    "https://ghproxy.com/https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt",
]

for url in urls:
    try:
        fname = url.split("/")[-1]
        if os.path.exists(fname) and os.path.getsize(fname) > 1000000:
            print(f"{fname} 已存在 ({os.path.getsize(fname)//1024//1024} MB)，跳过")
            continue
        print(f"下载: {url[:70]}...")
        r = requests.get(url, timeout=60, 
                        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                        stream=True)
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(fname, "wb") as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
        size_mb = downloaded / 1024 / 1024
        print(f"✅ 成功! {fname} ({size_mb:.1f} MB)")
        break
    except Exception as e:
        print(f"  ❌ {e}")
else:
    print("\n❌ 所有源都失败。")
    print("请手动下载模型后放到当前目录:")
    print("  下载地址: https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo11n.pt")
    print("  或使用百度网盘等工具下载后放入项目文件夹")
