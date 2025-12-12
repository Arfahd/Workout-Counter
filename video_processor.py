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

            # Draw all keypoints on top (while keeping angle calculation from right arm)
            annotated_img = self._draw_all_keypoints(annotated_img)

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

    def _draw_all_keypoints(self, img):
        """
        Draw all 17 COCO keypoints on the image.

        This displays the full body skeleton while AIGym continues to use
        only the right arm keypoints [6, 8, 10] for angle calculation.

        Args:
            img: Image to draw keypoints on

        Returns:
            np.ndarray: Image with all keypoints drawn
        """
        if not hasattr(self.gym, "tracks") or self.gym.tracks is None:
            return img

        if (
            not hasattr(self.gym.tracks, "keypoints")
            or self.gym.tracks.keypoints is None
        ):
            return img

        kpt_data = self.gym.tracks.keypoints.data
        conf_thresh = 0.5  # Confidence threshold for displaying keypoints

        # COCO skeleton connections (pairs of keypoint indices to connect with lines)
        skeleton = [
            [0, 1],
            [0, 2],
            [1, 3],
            [2, 4],  # Head
            [5, 6],
            [5, 7],
            [7, 9],
            [6, 8],
            [8, 10],  # Arms
            [5, 11],
            [6, 12],
            [11, 12],  # Torso
            [11, 13],
            [13, 15],
            [12, 14],
            [14, 16],  # Legs
        ]

        for k in kpt_data:
            # Draw skeleton lines
            for pt1_idx, pt2_idx in skeleton:
                if k[pt1_idx][2] >= conf_thresh and k[pt2_idx][2] >= conf_thresh:
                    pt1 = (int(k[pt1_idx][0]), int(k[pt1_idx][1]))
                    pt2 = (int(k[pt2_idx][0]), int(k[pt2_idx][1]))
                    cv2.line(img, pt1, pt2, (0, 255, 0), 2, lineType=cv2.LINE_AA)

            # Draw keypoint circles
            for i, kpt in enumerate(k):
                if kpt[2] >= conf_thresh:  # Check confidence
                    x, y = int(kpt[0]), int(kpt[1])
                    # Use different colors for different body parts
                    if i in [6, 8, 10]:  # Right arm (used for calculation) - Red
                        color = (0, 0, 255)
                        radius = 5  # Slightly larger for emphasis
                    elif i < 5:  # Head - Yellow
                        color = (0, 255, 255)
                        radius = 4
                    else:  # Other parts - Green
                        color = (0, 255, 0)
                        radius = 4
                    cv2.circle(img, (x, y), radius, color, -1, lineType=cv2.LINE_AA)

        return img
