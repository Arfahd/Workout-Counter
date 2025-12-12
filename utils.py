"""
Utility functions for the Pushup Counter application.
"""

import os
import json
from config import TEMP_COUNT_FILE


def read_temp_count():
    """
    Read the count and confidence from temporary file.

    Returns:
        tuple: (count, confidence) where count is int and confidence is float
    """
    try:
        if os.path.exists(TEMP_COUNT_FILE):
            with open(TEMP_COUNT_FILE, "r") as f:
                data = json.load(f)
                return data.get("count", 0), data.get("confidence", 0.0)
    except Exception:
        pass
    return 0, 0.0


def clear_temp_count():
    """Clear the temporary count file."""
    try:
        if os.path.exists(TEMP_COUNT_FILE):
            os.remove(TEMP_COUNT_FILE)
    except Exception:
        pass


def get_confidence_status(confidence_pct):
    """
    Get confidence status and color based on confidence percentage.

    Args:
        confidence_pct (float): Confidence percentage (0-100)

    Returns:
        tuple: (color, status_text)
    """
    from config import CONFIDENCE_THRESHOLDS, CONFIDENCE_COLORS

    if confidence_pct >= CONFIDENCE_THRESHOLDS["excellent"]:
        return CONFIDENCE_COLORS["excellent"], "Excellent"
    elif confidence_pct >= CONFIDENCE_THRESHOLDS["good"]:
        return CONFIDENCE_COLORS["good"], "Good"
    elif confidence_pct > CONFIDENCE_THRESHOLDS["poor"]:
        return CONFIDENCE_COLORS["poor"], "Poor"
    else:
        return CONFIDENCE_COLORS["none"], "No Detection"


def format_duration(seconds):
    """
    Format duration in seconds to MM:SS format.

    Args:
        seconds (int): Duration in seconds

    Returns:
        str: Formatted duration string (MM:SS)
    """
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def format_duration_verbose(seconds):
    """
    Format duration in seconds to verbose format (Xm Ys).

    Args:
        seconds (int): Duration in seconds

    Returns:
        str: Formatted duration string (e.g., "5m 30s")
    """
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}m {secs}s"


def calculate_rate(count, elapsed_seconds):
    """
    Calculate pushup rate per minute.

    Args:
        count (int): Number of pushups
        elapsed_seconds (int): Elapsed time in seconds

    Returns:
        float: Pushups per minute
    """
    if elapsed_seconds == 0:
        return 0.0
    elapsed_minutes = max(elapsed_seconds / 60, 0.1)
    return count / elapsed_minutes
