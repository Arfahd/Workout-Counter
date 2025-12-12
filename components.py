"""
Reusable UI components for the Pushup Counter application.
"""

import streamlit as st
import pandas as pd
from datetime import datetime


def render_header():
    """Render the application header."""
    st.markdown(
        """
        <div class="header-container">
            <h1>Pushup Counter</h1>
            <p class="subtitle" style="padding: 0 2rem;">AI-powered workout tracking with real-time form analysis</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_counter_display(current_count, confidence):
    """
    Render the real-time counter display with confidence indicator.

    Args:
        current_count (int): Current pushup count
        confidence (float): Confidence score (0.0 to 1.0)
    """
    from utils import get_confidence_status

    confidence_pct = confidence * 100
    conf_color, conf_status = get_confidence_status(confidence_pct)

    st.markdown(
        f"""
        <div class="counter-container">
            <div class="counter-label">Current Count</div>
            <div class="counter-value">{current_count}</div>
            <div class="counter-sublabel">pushups completed</div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                <div style="font-size: 0.75rem; color: rgba(255,255,255,0.8); margin-bottom: 0.25rem;">Detection Confidence</div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="font-size: 1.25rem; font-weight: 600; color: {conf_color};">{confidence_pct:.0f}%</div>
                    <div style="font-size: 0.75rem; color: rgba(255,255,255,0.7); background: rgba(255,255,255,0.1); padding: 0.125rem 0.5rem; border-radius: 0.25rem;">{conf_status}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_session_timers(duration_str, rate, confidence):
    """
    Render session timers and statistics.

    Args:
        duration_str (str): Formatted duration string (MM:SS)
        rate (float): Pushups per minute
        confidence (float): Confidence score (0.0 to 1.0)
    """
    from utils import get_confidence_status

    confidence_pct = confidence * 100
    conf_color, _ = get_confidence_status(confidence_pct)

    col_timer, col_rate, col_conf = st.columns(3)

    with col_timer:
        st.markdown(
            f"""
            <div class="timer-display">
                <div class="timer-value">{duration_str}</div>
                <div class="timer-label">Session Time</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_rate:
        st.markdown(
            f"""
            <div class="timer-display">
                <div class="timer-value">{rate:.1f}</div>
                <div class="timer-label">Reps/Min</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_conf:
        st.markdown(
            f"""
            <div class="timer-display" style="background: linear-gradient(135deg, {conf_color}22 0%, {conf_color}44 100%); border: 2px solid {conf_color}66;">
                <div class="timer-value" style="color: {conf_color};">{confidence_pct:.0f}%</div>
                <div class="timer-label">Confidence</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_status_card(is_streaming):
    """
    Render the session status card.

    Args:
        is_streaming (bool): Whether the video stream is active
    """
    if is_streaming:
        st.markdown(
            """
            <div class="status-card-active">
                <span class="status-badge status-active">
                    <span class="status-dot"></span>
                    LIVE
                </span>
                <div class="card-title">Recording Session</div>
                <div class="card-description">Pushup counter is active on the video feed. Complete your set and save when done.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="status-card">
                <span class="status-badge status-inactive">
                    <span class="status-dot"></span>
                    IDLE
                </span>
                <div class="card-title">Ready to Start</div>
                <div class="card-description">Position yourself in the camera view and start your workout session.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_video_placeholder():
    """Render the video placeholder when not streaming."""
    st.markdown(
        """
        <div class="video-placeholder">
            <div class="empty-state-icon">📹</div>
            <div class="empty-state-text">
                <strong>Camera Preview</strong><br>
                Start a session to begin tracking
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_statistics(df, personal_best):
    """
    Render statistics metrics grid.

    Args:
        df (pd.DataFrame): DataFrame containing pushup history
        personal_best (int): Personal best pushup count
    """
    total_pushups = df["Count"].sum()
    avg_pushups = df["Count"].mean()
    total_sessions = len(df)

    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Total</div>
                <div class="metric-value" style="color: #3B82F6;">{total_pushups}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Average</div>
                <div class="metric-value" style="color: #10B981;">{avg_pushups:.0f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Sessions</div>
                <div class="metric-value" style="color: #8B5CF6;">{total_sessions}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_personal_best(personal_best):
    """
    Render the personal best display.

    Args:
        personal_best (int): Personal best pushup count
    """
    if personal_best > 0:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6347 100%); background-size: 200% 200%; animation: gradient-shift 3s ease infinite; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1rem; text-align: center; box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);">
                <div style="display: inline-flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 2rem; animation: celebrate 1s ease infinite;">🏆</span>
                    <div>
                        <div style="font-size: 0.75rem; font-weight: 500; color: rgba(255, 255, 255, 0.95); text-transform: uppercase; letter-spacing: 0.05em; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);">Personal Best</div>
                        <div style="font-size: 1.75rem; font-weight: 700; color: white; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);">{personal_best} pushups</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_session_history(recent_sessions, max_pushups):
    """
    Render recent session history.

    Args:
        recent_sessions (list): List of session dictionaries
        max_pushups (int): Maximum pushup count in history (for progress bars)
    """
    for session in recent_sessions:
        count = session["Count"]
        date = session["Date"]
        time_str = session["Time"]
        duration = session["Duration"]

        is_pb = count == max_pushups
        progress_pct = (count / max_pushups) if max_pushups > 0 else 0

        with st.container(border=True):
            col_main, col_badge = st.columns([4, 1])

            with col_main:
                if is_pb:
                    st.markdown(
                        f"<span style='font-size: 1.1rem; font-weight: 600; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.3);'>{count} pushups</span> "
                        f"<span style='background: linear-gradient(135deg, #FFD700, #FFA500); color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.3); box-shadow: 0 2px 8px rgba(255,215,0,0.4);'>🏆 PB</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<span style='font-size: 1.1rem; font-weight: 600; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.3);'>{count} pushups</span>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"<span style='font-size: 0.875rem; color: rgba(255,255,255,0.85); text-shadow: 0 1px 2px rgba(0,0,0,0.2);'>{date} at {time_str} • {duration}</span>",
                    unsafe_allow_html=True,
                )

            st.progress(progress_pct, text="")


def render_new_pb_message(final_count, duration_str):
    """
    Render new personal best celebration message.

    Args:
        final_count (int): Final pushup count
        duration_str (str): Formatted duration string
    """
    st.markdown(
        f"""
        <div class="success-message" style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6347 100%); background-size: 200% 200%; animation: gradient-shift 3s ease infinite; border: none; border-radius: 1rem; padding: 2rem; margin-bottom: 1rem; text-align: center; box-shadow: 0 10px 40px rgba(255, 215, 0, 0.5);">
            <div style="font-size: 3.5rem; margin-bottom: 0.5rem; animation: celebrate 1s ease infinite;">🎉</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: white; margin-bottom: 0.5rem; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);">New Personal Best!</div>
            <div style="font-size: 1rem; color: white; text-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);">
                <strong style="font-size: 1.25rem;">{final_count} pushups</strong> in {duration_str}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state():
    """Render the empty state when no history exists."""
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-state-icon">💪</div>
            <div class="empty-state-text">
                <strong>Ready to start your fitness journey?</strong><br>
                Begin your first session to track your progress<br>
                <span style="font-size: 0.75rem; color: #9CA3AF;">Your workout statistics will appear here</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tips():
    """Render tips for best results."""
    st.markdown("### 💡 Tips for Best Results")
    st.markdown(
        """
        <div style="background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 1rem; padding: 1.5rem; font-size: 0.875rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
            <ul style="margin: 0; padding-left: 1.25rem; color: rgba(255, 255, 255, 0.95); line-height: 1.75; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);">
                <li style="margin-bottom: 0.5rem;">✨ Ensure good lighting for accurate tracking</li>
                <li style="margin-bottom: 0.5rem;">📹 Position yourself fully visible in frame</li>
                <li style="margin-bottom: 0.5rem;">💪 Maintain proper form throughout your set</li>
                <li>👁️ Keep your right arm visible to the camera</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
