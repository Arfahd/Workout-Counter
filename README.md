# 💪 Workout Counter

AI-powered pushup counter with real-time pose estimation and full body skeleton visualization.

## ✨ Features

- **Real-time Pushup Counting**: Automatic pushup detection and counting using YOLO pose estimation
- **Full Body Skeleton Visualization**: Display all 17 COCO keypoints with color-coded highlighting
- **Angle Calculation**: Track elbow angle in real-time for form analysis
- **Confidence Monitoring**: Visual confidence indicators for pose detection quality
- **Session History**: Track and export workout sessions
- **Personal Best Tracking**: Keep track of your highest pushup count
- **Professional UI**: Clean, modern interface with gradient backgrounds

## 🎯 How It Works

The application uses YOLO11 pose estimation to:
1. Detect body keypoints (17 COCO points: shoulders, elbows, wrists, hips, knees, etc.)
2. Calculate the angle at the right elbow joint using shoulder-elbow-wrist points
3. Count pushups based on angle thresholds:
   - **Up position**: Elbow angle > 145°
   - **Down position**: Elbow angle < 90°
   - **Rep counted**: When transitioning from up → down → up

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

## 📁 Project Structure

```
Workout-Counter/
├── app.py                  # Main Streamlit application
├── video_processor.py      # Video processing and pose detection
├── components.py           # UI components
├── config.py              # Configuration settings
├── styles.py              # CSS styles
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

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

## 🎨 Features Breakdown

### Full Body Visualization
- All 17 COCO keypoints displayed with skeleton lines
- Color-coded keypoints:
  - 🔴 **Red**: Right arm (used for angle calculation)
  - 🟡 **Yellow**: Head/face
  - 🟢 **Green**: Other body parts

### Angle Calculation
- Real-time elbow angle measurement
- Highlighted right arm for form checking
- Angle displayed on video feed

### Session Tracking
- Real-time pushup counter
- Session duration timer
- Pushup rate (reps/minute)
- Confidence score indicator

## 🛠️ Troubleshooting

### Camera not working
- Ensure camera permissions are granted
- Check if another application is using the camera
- Try refreshing the page

### Low FPS / Lag
- Switch to a lighter model (e.g., `yolo11n-pose.pt`)
- Use GPU if available (set `device: 0` in config)
- Reduce `max_det` in config

### Pushups not counting
- Ensure your full body is visible in frame
- Check that right arm is clearly visible
- Adjust lighting for better detection
- Lower the confidence threshold

## 📊 Technical Details

- **Framework**: Streamlit + WebRTC
- **Pose Estimation**: Ultralytics YOLO11-pose
- **Keypoint Format**: COCO (17 points)
- **Angle Calculation**: Three-point angle using arctangent
- **Tracking**: Single-person tracking with confidence filtering

## 📝 License

This project is open source.

## 🙏 Acknowledgments

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) for pose estimation
- [Streamlit](https://streamlit.io/) for the web framework
- [OpenCV](https://opencv.org/) for image processing

---

**Note**: Model files (`.pt`) are not included in the repository due to size constraints. Please download them separately as described in the installation section.
