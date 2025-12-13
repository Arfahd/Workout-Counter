# 💪 Workout Counter

AI-powered pushup counter with real-time pose estimation focused on right arm tracking.

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Webcam
- GPU (optional, but recommended for better performance)

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/Arfahd/Workout-Counter.git
cd Workout-Counter
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download YOLO model**:
Download the YOLO11 pose model and place it in the project root:
```bash
# Option 1: Download directly from Ultralytics
wget https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n-pose.pt

# Option 2: The model will auto-download on first run
```

Available models (choose based on your hardware):
- `yolo11n-pose.pt` - Nano (fastest, least accurate) - **Recommended for CPU**
- `yolo11s-pose.pt` - Small
- `yolo11m-pose.pt` - Medium
- `yolo11l-pose.pt` - Large
- `yolo11x-pose.pt` - Extra Large (slowest, most accurate) - **Recommended for GPU**

5. **Configure the model** in `config.py`:
```python
VIDEO_CONFIG = {
    "model": "yolo11n-pose.pt",  # Change to your downloaded model
    "device": "cpu",              # Change to 0 for GPU
    # ... other configs
}
```

## 🎮 Usage

1. **Run the application**:
```bash
streamlit run app.py
```

2. **Start a session**:
   - Click "▶️ Start Session"
   - Allow camera permissions
   - Position yourself in frame
   - Start doing pushups!

3. **Stop and save**:
   - Click "⏹ Stop & Save" to end the session
   - View your statistics and history

## ⚙️ Configuration

Edit `config.py` to customize:

- **Model settings**: Choose YOLO model and device (CPU/GPU)
- **Keypoints**: Specify which keypoints to use for angle calculation (default: right arm)
- **Thresholds**: Adjust up/down angle thresholds for pushup detection
- **UI settings**: Customize line width, max detections, etc.

### Key Configuration Options:

```python
VIDEO_CONFIG = {
    "kpts": [6, 8, 10],           # Right arm: shoulder, elbow, wrist
    "model": "yolo11n-pose.pt",   # Model file
    "device": 0,                   # 0 for GPU, "cpu" for CPU
    "flip_horizontal": True,       # Mirror webcam feed
}
```

## 📝 License

This project is open source.

## 🙏 Acknowledgments

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) for pose estimation models
- [PyTorch](https://pytorch.org/) for deep learning framework
- [Streamlit](https://streamlit.io/) for the web interface
- [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc) for real-time webcam streaming
- [OpenCV](https://opencv.org/) for computer vision and image processing
- [Pandas](https://pandas.pydata.org/) for data management
- [PyAV](https://github.com/PyAV-Org/PyAV) for video frame processing

---

**Note**: Model files (`.pt`) are not included in the repository due to size constraints. Please download them separately as described in the installation section.
