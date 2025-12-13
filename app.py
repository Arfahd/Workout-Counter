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
    render_session_stats,
    render_status_badge,
    render_video_placeholder,
    render_statistics,
    render_session_history,
    render_new_pb_message,
    render_enhanced_empty_state,
    render_collapsible_section,
    render_loading_state,
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
if "camera_initializing" not in st.session_state:
    st.session_state.camera_initializing = False
if "show_history" not in st.session_state:
    st.session_state.show_history = True

# Get current workout data
if st.session_state.is_streaming:
    current_count, confidence = read_temp_count()

    if st.session_state.session_start:
        duration = datetime.now() - st.session_state.session_start
        duration_str = format_duration(duration.seconds)
        rate = calculate_rate(current_count, duration.seconds)
    else:
        duration_str = "00:00"
        rate = 0
        confidence = 0
else:
    current_count = 0
    confidence = 0
    duration_str = "00:00"
    rate = 0

# ALWAYS SHOW COUNTER - UX Best Practice: Visibility of System Status
render_counter_display(current_count, st.session_state.is_streaming)

# Status badge
render_status_badge(st.session_state.is_streaming)

# CONTROL BAR - Full width above video (UX Best Practice: Fitts's Law)
st.markdown('<div class="control-bar">', unsafe_allow_html=True)

if not st.session_state.is_streaming:
    # Single large primary button when idle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "▶️  Start Workout Session",
            use_container_width=True,
            type="primary",
            key="start_btn",
        ):
            clear_temp_count()
            st.session_state.session_start = None
            st.session_state.is_streaming = True
            st.session_state.camera_initializing = True
            st.rerun()
else:
    # Two buttons side by side when streaming
    col_stop, col_cancel = st.columns(2)

    with col_stop:
        if st.button(
            "⏹  Stop & Save", use_container_width=True, type="primary", key="stop_btn"
        ):
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
            st.session_state.camera_initializing = False

            # Enhanced success message with vibrant colors
            if is_new_pb and final_count > 0:
                render_new_pb_message(final_count, duration_str)
            else:
                st.success(
                    f"✅ Session saved: **{final_count} pushups** in {duration_str}"
                )
            time.sleep(2)
            st.rerun()

    with col_cancel:
        if st.button(
            "❌  Cancel Session",
            use_container_width=True,
            type="secondary",
            key="cancel_btn",
        ):
            clear_temp_count()
            st.session_state.is_streaming = False
            st.session_state.camera_initializing = False
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# SESSION STATS - Only show when streaming (Progressive Disclosure)
if st.session_state.is_streaming:
    render_session_stats(duration_str, rate, confidence)

# VIDEO FEED - Centered, larger (75% width)
st.markdown("---")
col_left, col_video, col_right = st.columns([1, 3, 1])

with col_video:
    if st.session_state.is_streaming:
        # Show loading state initially
        if st.session_state.camera_initializing:
            render_loading_state("Initializing camera...")

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
            # Camera is now active, turn off initializing state
            if st.session_state.camera_initializing:
                st.session_state.camera_initializing = False

            # Start the timer only when webcam is actually streaming
            if st.session_state.session_start is None:
                st.session_state.session_start = datetime.now()

            time.sleep(1)  # Refresh every 1 second
            st.rerun()
    else:
        render_video_placeholder()

# STATISTICS & HISTORY - Collapsible sections
st.markdown("---")

if st.session_state.pushup_history:
    # Statistics
    df = pd.DataFrame(st.session_state.pushup_history)
    max_pushups = df["Count"].max()

    # Update personal best
    if max_pushups > st.session_state.personal_best:
        st.session_state.personal_best = max_pushups

    # Display metrics
    render_statistics(df, st.session_state.personal_best)

    # History section - Collapsible
    with render_collapsible_section(
        "📊 Workout History", st.session_state.show_history
    ):
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
                label="📥 Export to CSV",
                data=csv,
                file_name=f"pushup_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with col_clear:
            if st.button(
                "🗑️ Clear All History", use_container_width=True, type="secondary"
            ):
                st.session_state.pushup_history = []
                st.session_state.personal_best = 0
                st.rerun()
else:
    render_enhanced_empty_state()

# Keyboard shortcuts info (Accessibility)
st.markdown("---")
with st.expander("⌨️ Keyboard Shortcuts"):
    st.markdown("""
    - **Space**: Start/Stop workout
    - **Esc**: Cancel workout
    - **H**: Toggle history
    - **?**: Show this help
    """)

# Footer with accessibility info
st.markdown(
    """
    <div style="text-align: center; padding: 2rem 0; color: rgba(255,255,255,0.6); font-size: 0.75rem;">
        Made with ❤️ using AI-powered pose detection<br>
        <a href="#" style="color: rgba(255,255,255,0.8); text-decoration: none;">Accessibility Statement</a> • 
        <a href="#" style="color: rgba(255,255,255,0.8); text-decoration: none;">Privacy Policy</a>
    </div>
    """,
    unsafe_allow_html=True,
)
