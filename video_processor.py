"""
Video processor for the Pushup Counter application.
Handles video frame processing and pose detection using YOLO.
"""

import av
import json
import cv2
from streamlit_webrtc import VideoProcessorBase
from ultralytics import solutions

from config import VIDEO_CONFIG, TEMP_COUNT_FILE


class GymProcessor(VideoProcessorBase):
    """Video processor that detects and counts pushups using YOLO pose detection."""

    def __init__(self):
        """Initialize the GymProcessor with AIGym solution."""
        # Initialize AIGym with default settings
        self.gym = solutions.AIGym(
            show=False,
            kpts=VIDEO_CONFIG["kpts"],
            model=VIDEO_CONFIG["model"],
            line_width=VIDEO_CONFIG["line_width"],
            max_det=VIDEO_CONFIG["max_det"],
            device=VIDEO_CONFIG.get("device", "cpu"),  # Use GPU if configured
        )
        self.max_count = 0
        self.current_confidence = 0.0

    def recv(self, frame):
        """
        Process a video frame and detect pushups.

        Args:
            frame: Input video frame from webrtc stream

        Returns:
            av.VideoFrame: Annotated video frame with pose detection overlays
        """
        try:
            # Convert the video frame to a numpy array
            img = frame.to_ndarray(format="bgr24")

            # Flip horizontally if configured (to remove mirror effect)
            if VIDEO_CONFIG.get("flip_horizontal", False):
                img = cv2.flip(img, 1)

            # Pass the image to AIGym for processing
            results = self.gym(img)

            # Extract confidence score from detections
            confidence = self._extract_confidence()
            self.current_confidence = confidence

            # Extract and store the maximum pushup count
            if results and hasattr(results, "workout_count") and results.workout_count:
                current_count = sum(results.workout_count)
                if current_count > self.max_count:
                    self.max_count = current_count

                # Write to temporary file (thread-safe way to share data)
                self._write_temp_data()
            else:
                # Even if no workout count, still update confidence
                self._write_temp_data()

            # Get the processed image with annotations
            if results and hasattr(results, "plot_im"):
                annotated_img = results.plot_im
            else:
                # Fallback to original image if results not available
                annotated_img = img

            # Note: Only 3 keypoints (right arm) are detected and shown
            # For full body visualization, see the 'full-body-visualization' branch

            # Return the processed image to the browser
            return av.VideoFrame.from_ndarray(annotated_img, format="bgr24")

        except Exception as e:
            # On error, return original frame to prevent crashes
            print(f"Error processing frame: {e}")
            return frame

    def _extract_confidence(self):
        """
        Extract confidence score from gym detections.

        Returns:
            float: Confidence score (0.0 to 1.0)
        """
        confidence = 0.0
        try:
            # Method 1: Try to get from gym.boxes (populated by extract_tracks)
            if hasattr(self.gym, "boxes") and len(self.gym.boxes) > 0:
                # gym.boxes typically contains [x1, y1, x2, y2, conf, cls, ...] per box
                box_data = self.gym.boxes[0]
                if hasattr(box_data, "__len__") and len(box_data) >= 5:
                    # Confidence is usually the 5th element (index 4)
                    try:
                        confidence = float(box_data[4])
                    except (ValueError, TypeError, IndexError):
                        pass

            # Method 2: Try from tracks.boxes if available
            if (
                confidence == 0.0
                and hasattr(self.gym, "tracks")
                and self.gym.tracks is not None
            ):
                if (
                    hasattr(self.gym.tracks, "boxes")
                    and self.gym.tracks.boxes is not None
                ):
                    if (
                        hasattr(self.gym.tracks.boxes, "conf")
                        and len(self.gym.tracks.boxes.conf) > 0
                    ):
                        confidence = float(self.gym.tracks.boxes.conf[0])
                elif hasattr(self.gym.tracks, "conf") and len(self.gym.tracks.conf) > 0:
                    confidence = float(self.gym.tracks.conf[0])

            # Method 3: Try from r_s if available (final fallback)
            if (
                confidence == 0.0
                and hasattr(self.gym, "r_s")
                and self.gym.r_s is not None
            ):
                if hasattr(self.gym.r_s, "boxes") and self.gym.r_s.boxes is not None:
                    if (
                        hasattr(self.gym.r_s.boxes, "conf")
                        and len(self.gym.r_s.boxes.conf) > 0
                    ):
                        confidence = float(self.gym.r_s.boxes.conf[0])
        except Exception:
            # Silently fail and keep confidence at 0.0
            pass

        return confidence

    def _write_temp_data(self):
        """Write current count and confidence to temporary file."""
        try:
            with open(TEMP_COUNT_FILE, "w") as f:
                json.dump(
                    {"count": self.max_count, "confidence": self.current_confidence}, f
                )
        except Exception:
            pass
