"""
Configuration constants for the Pushup Counter application.
"""

# File paths
TEMP_COUNT_FILE = "temp_pushup_count.json"

# Page configuration
PAGE_CONFIG = {
    "page_title": "Pushup Counter",
    "page_icon": "💪",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}

# Video processing configuration
VIDEO_CONFIG = {
    "kpts": [6, 8, 10],  # Right arm keypoints
    "model": "yolo11x-pose.pt",  # Extra Large model for maximum accuracy
    "line_width": 2,
    "max_det": 1,
    "device": 0,  # Use GPU (0 = first GPU, 'cpu' for CPU only)
    "flip_horizontal": True,  # Flip video horizontally (mirror effect)
    "max_history": 100,  # Maximum number of sessions to keep in memory
}

# WebRTC configuration
RTC_CONFIG = {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}

# Confidence thresholds
CONFIDENCE_THRESHOLDS = {
    "excellent": 80,
    "good": 50,
    "poor": 0,
}

# Confidence colors
CONFIDENCE_COLORS = {
    "excellent": "#10B981",  # Green
    "good": "#F59E0B",  # Yellow/Orange
    "poor": "#EF4444",  # Red
    "none": "#6B7280",  # Gray
}
