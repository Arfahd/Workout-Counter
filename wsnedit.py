"""
Pushup Counter - Main Application
AI-powered workout tracking with real-time form analysis
"""

import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_webrtc import webrtc_streamer

# Import custom modules
from config import PAGE_CONFIG, RTC_CONFIG, VIDEO_CONFIG
from styles import apply_custom_styles
from components import (
    render_header,
    render_counter_display,
    render_session_timers,
    render_status_card,
    render_video_placeholder,
    render_statistics,
    render_personal_best,
    render_session_history,
    render_new_pb_message,
    render_empty_state,
    render_tips,
)
from utils import (
    read_temp_count,
    clear_temp_count,
    format_duration,
    format_duration_verbose,
    calculate_rate,
)
from video_processor import GymProcessor


# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Apply custom styles
apply_custom_styles()

# Render header
render_header()

# Initialize session state
if "is_streaming" not in st.session_state:
    st.session_state.is_streaming = False
if "session_start" not in st.session_state:
    st.session_state.session_start = None
if "pushup_history" not in st.session_state:
    st.session_state.pushup_history = []
if "current_count" not in st.session_state:
    st.session_state.current_count = 0
if "personal_best" not in st.session_state:
    st.session_state.personal_best = 0


# Main content area - Top section: Counter and timers
if st.session_state.is_streaming:
    # Read current count and confidence from temp file
    current_count, confidence = read_temp_count()

    # Calculate session duration
    if st.session_state.session_start:
        duration = datetime.now() - st.session_state.session_start
        duration_str = format_duration(duration.seconds)
        rate = calculate_rate(current_count, duration.seconds)
    else:
        duration_str = "00:00"
        rate = 0

    # Display counter with gradient background and confidence indicator
    render_counter_display(current_count, confidence)

    # Timer display and confidence progress bar
    render_session_timers(duration_str, rate, confidence)

# Session status
render_status_card(st.session_state.is_streaming)

# Middle section: Centered webcam (70% width centered)
col_spacer1, col_camera, col_spacer2 = st.columns([1, 3, 1])

with col_camera:
    # Camera section
    st.markdown("### Camera Feed")

    # Controls
    if not st.session_state.is_streaming:
        if st.button("▶️ Start Session", use_container_width=True):
            clear_temp_count()
            st.session_state.session_start = None  # Don't start timer yet
            st.session_state.is_streaming = True
            st.rerun()
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("⏹ Stop & Save", use_container_width=True, type="primary"):
                final_count, _ = read_temp_count()

                if st.session_state.session_start:
                    duration = datetime.now() - st.session_state.session_start
                    duration_str = format_duration_verbose(duration.seconds)
                else:
                    duration_str = "0m 0s"

                st.session_state.pushup_history.append(
                    {
                        "Date": st.session_state.session_start.strftime("%b %d, %Y")
                        if st.session_state.session_start
                        else datetime.now().strftime("%b %d, %Y"),
                        "Time": st.session_state.session_start.strftime("%I:%M %p")
                        if st.session_state.session_start
                        else datetime.now().strftime("%I:%M %p"),
                        "Count": final_count,
                        "Duration": duration_str,
                    }
                )

                # Keep only last N sessions to prevent memory issues
                max_history = VIDEO_CONFIG.get("max_history", 100)
                if len(st.session_state.pushup_history) > max_history:
                    st.session_state.pushup_history = st.session_state.pushup_history[
                        -max_history:
                    ]

                # Check if it's a new personal best
                is_new_pb = final_count > st.session_state.personal_best

                clear_temp_count()
                st.session_state.is_streaming = False

                # Enhanced success message with vibrant colors
                if is_new_pb and final_count > 0:
                    render_new_pb_message(final_count, duration_str)
                else:
                    st.success(
                        f"✅ Session saved: **{final_count} pushups** in {duration_str}"
                    )
                time.sleep(2)
                st.rerun()

        with col_b:
            if st.button("❌ Cancel", use_container_width=True, type="secondary"):
                clear_temp_count()
                st.session_state.is_streaming = False
                st.rerun()

    # Video stream
    if st.session_state.is_streaming:
        ctx = webrtc_streamer(
            key="pushup-gym",
            video_processor_factory=GymProcessor,
            media_stream_constraints={"video": True, "audio": False},
            rtc_configuration=RTC_CONFIG,
        )

        if ctx and not ctx.state.playing:
            st.warning(
                "📹 Camera access required. Please allow camera permissions and refresh if needed."
            )

        # Safe auto-refresh: Only refresh if the WebRTC is properly playing
        if ctx and ctx.state.playing:
            # Start the timer only when webcam is actually streaming
            if st.session_state.session_start is None:
                st.session_state.session_start = datetime.now()

            time.sleep(1)  # Refresh every 1 second
            st.rerun()
    else:
        render_video_placeholder()

    # Bottom section: Statistics & History
st.markdown("### Statistics & History")

if st.session_state.pushup_history:
    # Statistics
    df = pd.DataFrame(st.session_state.pushup_history)
    max_pushups = df["Count"].max()

    # Update personal best
    if max_pushups > st.session_state.personal_best:
        st.session_state.personal_best = max_pushups

    # Display metrics
    render_statistics(df, st.session_state.personal_best)

    # Personal best display
    render_personal_best(st.session_state.personal_best)

    # History table
    st.markdown("### Recent Sessions")

    # Get last 10 sessions in reverse order
    recent_sessions = st.session_state.pushup_history[-10:][::-1]
    render_session_history(recent_sessions, max_pushups)

    # Actions
    st.markdown("")
    col_export, col_clear = st.columns(2)

    with col_export:
        # Export to CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Export CSV",
            data=csv,
            file_name=f"pushup_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col_clear:
        if st.button("🗑️ Clear History", use_container_width=True, type="secondary"):
            st.session_state.pushup_history = []
            st.session_state.personal_best = 0
            st.rerun()
else:
    render_empty_state()
    render_tips()
