# 🚲 校园电动车数字孪生监管系统

基于 **YOLOv8/v11 + MediaPipe Hands + Three.js** 的校园电动车智能监管系统，支持实时目标检测、违规行为识别、3D 数字孪生场景及手势交互。

---

## 📋 功能特性

### 🔍 目标检测
- 电动车识别与定位
- 车牌检测
- 违规行为识别（违停、超载、逆行等）
- 合规/违规统计看板

### 🖐️ 手势交互
- 基于 MediaPipe Hands 的手部关键点检测
- 捏合手势进行 3D 场景漫游和对象拖拽
- 实时手势状态反馈

### 🏢 3D 数字孪生
- Three.js 构建的校园 3D 场景
- 建筑、道路、树木、路灯等环境要素
- 检测结果实时映射到 3D 场景
- 拖拽旋转查看

### 🌐 Web 管理界面
- 实时视频流检测
- 统计仪表盘
- 历史记录查看

---

## 🚀 快速开始

### 1️⃣ 克隆仓库

```bash
git clone https://github.com/GuanLng/campus-ev-digital-twin.git
cd campus-ev-digital-twin
```

### 2️⃣ 安装依赖

```bash
# 建议使用虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

> **GPU 加速**（推荐）：若需 CUDA 加速，安装 PyTorch GPU 版：
> ```bash
> pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
> ```

### 3️⃣ 下载 YOLO 模型

```bash
# 自动下载 YOLO 模型（首次运行会自动下载）
python download_model.py
```

> **国内用户**：可使用 ModelScope 镜像加速下载
> ```bash
> pip install modelscope
> python download_via_modelscope.py
> ```

### 4️⃣ 启动系统

```bash
python app.py
```

浏览器访问 **http://localhost:5000**

---

## 📁 项目结构

```
├── app.py                     # Flask Web 主程序
├── build.py                   # 构建/部署版本（单文件含前端）
├── check_env.py               # 环境检测（PyTorch/CUDA）
│
├── detect_camera.py           # 摄像头实时检测
├── detect_photo.py            # 图片检测
├── detect_with_violation.py   # 违规行为检测
├── run_yolo.py                # YOLO 推理封装
│
├── download_model.py          # 模型下载
├── download_via_modelscope.py # ModelScope 国内镜像下载
│
├── requirements.txt           # Python 依赖
├── .gitignore                 # Git 忽略规则
│
├── templates/
│   └── index.html             # Web 前端页面（含 Three.js 3D 场景）
│
├── static/
│   ├── three.min.js           # Three.js 3D 引擎
│   ├── hand_landmark_full.tflite  # 手部关键点模型
│   ├── hands.js               # MediaPipe Hands 库
│   ├── hands_solution_*.wasm  # WebAssembly 推理引擎
│   ├── camera_utils.js        # 摄像头工具
│   └── drawing_utils.js       # 手势绘制工具
│
└── 第一次/v1.0/               # v1.0 初始版本存档
```

---

## 🧩 技术栈

| 技术 | 用途 |
|------|------|
| **Python / Flask** | Web 后端 |
| **YOLOv8 / YOLOv11** | 电动车目标检测 |
| **OpenCV** | 图像处理与视频流 |
| **MediaPipe Hands** | 手势关键点识别 |
| **Three.js** | 3D 数字孪生场景 |
| **WebAssembly (WASM)** | 手势推理引擎（浏览器端） |
| **PyTorch** | 深度学习框架 |

---

## 📷 截图

> *（运行后截图可在此处添加）*

---

## 📄 许可证

本项目仅供学习与科研用途。
