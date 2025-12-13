"""
Reusable UI components for the Pushup Counter application.
Enhanced with UX best practices and accessibility improvements.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from contextlib import contextmanager


def render_header():
    """Render the application header with improved accessibility."""
    st.markdown(
        """
        <div class="header-container" role="banner">
            <h1>💪 Pushup Counter</h1>
            <p class="subtitle">AI-powered workout tracking with real-time form analysis</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_counter_display(current_count, is_streaming):
    """
    ALWAYS VISIBLE counter display - UX Best Practice: Visibility of System Status

    Args:
        current_count (int): Current pushup count
        is_streaming (bool): Whether workout is active
    """
    if is_streaming:
        status_text = "In Progress"
        status_color = "#10B981"
        size_class = "counter-streaming"
    else:
        status_text = "Ready to Start"
        status_color = "#6B7280"
        size_class = "counter-idle"

    st.markdown(
        f"""
        <div class="counter-main {size_class}" role="status" aria-live="polite" aria-atomic="true">
            <div class="counter-label">Current Count</div>
            <div class="counter-value" aria-label="{current_count} pushups">{current_count}</div>
            <div class="counter-status" style="color: {status_color};">
                <span class="status-indicator" style="background: {status_color};"></span>
                {status_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_badge(is_streaming):
    """
    Simplified status badge - less intrusive

    Args:
        is_streaming (bool): Whether the video stream is active
    """
    if is_streaming:
        st.markdown(
            """
            <div class="status-mini" role="status">
                <span class="status-dot live"></span>
                <span>LIVE</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="status-mini" role="status">
                <span class="status-dot idle"></span>
                <span>IDLE</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_session_stats(duration_str, rate, confidence):
    """
    Simplified session stats - only shown during workout (Progressive Disclosure)

    Args:
        duration_str (str): Formatted duration string (MM:SS)
        rate (float): Pushups per minute
        confidence (float): Confidence score (0.0 to 1.0)
    """
    from utils import get_confidence_status

    confidence_pct = confidence * 100
    conf_color, conf_status = get_confidence_status(confidence_pct)

    st.markdown(
        f"""
        <div class="session-stats-compact">
            <div class="stat-item">
                <div class="stat-icon">⏱️</div>
                <div class="stat-content">
                    <div class="stat-value">{duration_str}</div>
                    <div class="stat-label">Duration</div>
                </div>
            </div>
            <div class="stat-item">
                <div class="stat-icon">⚡</div>
                <div class="stat-content">
                    <div class="stat-value">{rate:.1f}</div>
                    <div class="stat-label">Reps/Min</div>
                </div>
            </div>
            <div class="stat-item">
                <div class="stat-icon">🎯</div>
                <div class="stat-content">
                    <div class="stat-value" style="color: {conf_color};">{confidence_pct:.0f}%</div>
                    <div class="stat-label">Confidence</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_loading_state(message="Loading..."):
    """
    Loading state with spinner - UX Best Practice: Provide Feedback

    Args:
        message (str): Loading message to display
    """
    st.markdown(
        f"""
        <div class="loading-state">
            <div class="spinner"></div>
            <div class="loading-text">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_video_placeholder():
    """Enhanced video placeholder with better visual hierarchy."""
    st.markdown(
        """
        <div class="video-placeholder">
            <div class="placeholder-icon">📹</div>
            <div class="placeholder-title">Camera Preview</div>
            <div class="placeholder-text">
                Click "Start Workout Session" above to begin tracking
            </div>
            <div class="placeholder-tips">
                <div class="tip-item">✓ Position yourself sideways to camera</div>
                <div class="tip-item">✓ Ensure good lighting</div>
                <div class="tip-item">✓ Keep right arm visible</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_statistics(df, personal_best):
    """
    Cleaner statistics display with focus on key metrics

    Args:
        df (pd.DataFrame): DataFrame containing pushup history
        personal_best (int): Personal best pushup count
    """
    total_pushups = df["Count"].sum()
    avg_pushups = df["Count"].mean()
    total_sessions = len(df)

    st.markdown(
        f"""
        <div class="stats-grid">
            <div class="stat-card stat-card-primary">
                <div class="stat-card-icon">🏆</div>
                <div class="stat-card-value">{personal_best}</div>
                <div class="stat-card-label">Personal Best</div>
            </div>
            <div class="stat-card stat-card-secondary">
                <div class="stat-card-icon">📊</div>
                <div class="stat-card-value">{total_pushups}</div>
                <div class="stat-card-label">Total Pushups</div>
            </div>
            <div class="stat-card stat-card-tertiary">
                <div class="stat-card-icon">📈</div>
                <div class="stat-card-value">{avg_pushups:.0f}</div>
                <div class="stat-card-label">Average</div>
            </div>
            <div class="stat-card stat-card-quaternary">
                <div class="stat-card-icon">🎯</div>
                <div class="stat-card-value">{total_sessions}</div>
                <div class="stat-card-label">Sessions</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_session_history(recent_sessions, max_pushups):
    """
    Improved session history with better visual design

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
            col_main, col_count = st.columns([3, 1])

            with col_main:
                st.markdown(
                    f"<div class='session-date'>{date} at {time_str}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div class='session-duration'>Duration: {duration}</div>",
                    unsafe_allow_html=True,
                )

            with col_count:
                if is_pb:
                    st.markdown(
                        f"""
                        <div class='session-count pb'>
                            <span class='count-value'>{count}</span>
                            <span class='count-badge'>🏆 PB</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div class='session-count'>
                            <span class='count-value'>{count}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.progress(progress_pct, text="")


def render_new_pb_message(final_count, duration_str):
    """
    Celebration modal for new personal best with confetti animation
    Creates a centered overlay modal that focuses attention on the achievement

    Args:
        final_count (int): Final pushup count
        duration_str (str): Formatted duration string
    """
    st.markdown(
        f"""
        <div class="celebration-modal-overlay" role="dialog" aria-labelledby="pb-title" aria-modal="true">
            <div class="celebration-modal">
                <div class="celebration-confetti-bg">
                    <span class="confetti">🎉</span>
                    <span class="confetti">🎊</span>
                    <span class="confetti">✨</span>
                    <span class="confetti">🌟</span>
                    <span class="confetti">💫</span>
                    <span class="confetti">⭐</span>
                </div>
                <div class="celebration-icon">🎉</div>
                <div id="pb-title" class="celebration-title">New Personal Best!</div>
                <div class="celebration-count">{final_count} pushups</div>
                <div class="celebration-duration">Completed in {duration_str}</div>
                <div class="celebration-message">Amazing work! Keep it up! 💪</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_enhanced_empty_state():
    """
    Enhanced empty state with clear CTA and onboarding
    UX Best Practice: Guide users with clear next steps
    """
    st.markdown(
        '<div class="empty-state-enhanced">'
        '<div class="empty-icon">💪</div>'
        '<div class="empty-title">Ready to Start Your Fitness Journey?</div>'
        '<div class="empty-subtitle">Track your pushups with AI-powered precision</div>'
        '<div class="setup-checklist">'
        '<div class="checklist-title">Quick Setup Guide:</div>'
        '<div class="checklist-item"><span class="check">✓</span><span>Position yourself sideways to the camera</span></div>'
        '<div class="checklist-item"><span class="check">✓</span><span>Ensure good lighting for accurate tracking</span></div>'
        '<div class="checklist-item"><span class="check">✓</span><span>Keep your right arm visible throughout</span></div>'
        '<div class="checklist-item"><span class="check">✓</span><span>Maintain proper form for best results</span></div>'
        "</div>"
        '<div class="empty-cta">'
        '<div class="cta-arrow">👆</div>'
        '<div class="cta-text">Click "Start Workout Session" above to begin!</div>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


@contextmanager
def render_collapsible_section(title, is_expanded=True):
    """
    Collapsible section wrapper for better content organization

    Args:
        title (str): Section title
        is_expanded (bool): Whether section is expanded by default
    """
    with st.expander(title, expanded=is_expanded):
        yield
