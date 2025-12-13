"""
CSS styles for the Pushup Counter application.
Enhanced with UX best practices, accessibility, and performance optimizations.
"""

import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app with UX improvements."""

    # Hide sidebar completely
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Modern, accessible CSS with design system tokens
    st.markdown(
        """
        <style>
        /* ============================================
           DESIGN SYSTEM TOKENS
           ============================================ */
        :root {
            /* Colors - Simplified palette */
            --color-primary: #667eea;
            --color-primary-dark: #5568d3;
            --color-success: #10B981;
            --color-warning: #F59E0B;
            --color-error: #EF4444;
            --color-neutral: #6B7280;
            --color-neutral-light: #9CA3AF;
            
            /* Spacing - 8px base unit */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;
            --space-3xl: 4rem;
            
            /* Typography */
            --font-size-xs: 0.75rem;
            --font-size-sm: 0.875rem;
            --font-size-md: 1rem;
            --font-size-lg: 1.125rem;
            --font-size-xl: 1.25rem;
            --font-size-2xl: 1.5rem;
            --font-size-3xl: 1.875rem;
            --font-size-4xl: 2.25rem;
            --font-size-5xl: 3rem;
            --font-size-6xl: 4rem;
            
            /* Shadows */
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
            --shadow-xl: 0 20px 25px rgba(0,0,0,0.1);
            
            /* Border radius */
            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 1rem;
            --radius-xl: 1.5rem;
            --radius-full: 9999px;
            
            /* Transitions */
            --transition-fast: 150ms ease;
            --transition-base: 200ms ease;
            --transition-slow: 300ms ease;
        }
        
        /* ============================================
           GLOBAL STYLES
           ============================================ */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        /* Main background - Subtle gradient (less animation for performance) */
        .stApp, [data-testid="stAppViewContainer"], .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%) !important;
            background-size: 200% 200% !important;
            animation: subtle-gradient 20s ease infinite !important;
            min-height: 100vh;
        }
        
        @keyframes subtle-gradient {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        /* Reduce motion for accessibility */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        
        .block-container {
            position: relative;
            z-index: 1;
            padding: var(--space-2xl) var(--space-xl) var(--space-xl) var(--space-xl) !important;
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        
        /* ============================================
           HEADER
           ============================================ */
        .header-container {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            padding: var(--space-2xl) 0 var(--space-lg) 0;
            margin: calc(var(--space-2xl) * -1) calc(var(--space-xl) * -1) var(--space-xl);
            border-radius: 0 0 var(--space-lg) var(--space-lg);
            box-shadow: var(--shadow-xl);
            text-align: center;
        }
        
        .header-container h1 {
            font-size: var(--font-size-3xl) !important;
            font-weight: 700 !important;
            color: white !important;
            margin: 0 !important;
            letter-spacing: -0.025em !important;
        }
        
        .subtitle {
            font-size: var(--font-size-md);
            color: rgba(255, 255, 255, 0.9);
            margin-top: var(--space-sm);
            font-weight: 400;
        }
        
        /* ============================================
           COUNTER DISPLAY (ALWAYS VISIBLE)
           ============================================ */
        .counter-main {
            background: rgba(255, 255, 255, 0.95);
            border-radius: var(--radius-xl);
            padding: var(--space-2xl);
            text-align: center;
            margin-bottom: var(--space-xl);
            box-shadow: var(--shadow-xl);
            transition: all var(--transition-base);
        }
        
        .counter-main.counter-streaming {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            color: white;
            transform: scale(1.02);
        }
        
        .counter-main.counter-idle {
            background: rgba(255, 255, 255, 0.9);
        }
        
        .counter-label {
            font-size: var(--font-size-sm);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            opacity: 0.8;
            margin-bottom: var(--space-sm);
        }
        
        .counter-streaming .counter-label {
            color: rgba(255, 255, 255, 0.9);
        }
        
        .counter-idle .counter-label {
            color: var(--color-neutral);
        }
        
        .counter-value {
            font-size: var(--font-size-6xl);
            font-weight: 800;
            line-height: 1;
            margin: var(--space-md) 0;
            letter-spacing: -0.05em;
        }
        
        .counter-streaming .counter-value {
            color: white;
            animation: pulse-glow 2s ease-in-out infinite;
        }
        
        .counter-idle .counter-value {
            color: var(--color-neutral);
        }
        
        @keyframes pulse-glow {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.9; }
        }
        
        .counter-status {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--space-sm);
            font-size: var(--font-size-sm);
            font-weight: 600;
            margin-top: var(--space-md);
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: var(--radius-full);
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.8; }
        }
        
        /* ============================================
           STATUS BADGE (MINI)
           ============================================ */
        .status-mini {
            display: inline-flex;
            align-items: center;
            gap: var(--space-sm);
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: var(--radius-full);
            padding: var(--space-sm) var(--space-md);
            font-size: var(--font-size-sm);
            font-weight: 600;
            color: white;
            margin-bottom: var(--space-lg);
            width: fit-content;
            margin-left: auto;
            margin-right: auto;
        }
        
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: var(--radius-full);
        }
        
        .status-dot.live {
            background: var(--color-success);
            box-shadow: 0 0 10px var(--color-success);
            animation: blink 1.5s ease-in-out infinite;
        }
        
        .status-dot.idle {
            background: var(--color-neutral-light);
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* ============================================
           CONTROL BAR (FULL WIDTH)
           ============================================ */
        .control-bar {
            margin-bottom: var(--space-xl);
        }
        
        /* Buttons - Improved touch targets */
        .stButton > button {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: var(--space-md) var(--space-xl) !important;
            font-size: var(--font-size-md) !important;
            font-weight: 600 !important;
            min-height: 56px !important;
            transition: all var(--transition-base) !important;
            box-shadow: var(--shadow-md) !important;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-lg) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        .stButton > button:focus-visible {
            outline: 3px solid rgba(102, 126, 234, 0.5) !important;
            outline-offset: 2px !important;
        }
        
        /* Primary button */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--color-success) 0%, #059669 100%) !important;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6) !important;
        }
        
        /* Secondary button */
        .stButton > button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.9) !important;
            color: var(--color-neutral) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: rgba(255, 255, 255, 1) !important;
        }
        
        /* ============================================
           SESSION STATS (COMPACT)
           ============================================ */
        .session-stats-compact {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--space-md);
            margin-bottom: var(--space-xl);
        }
        
        .stat-item {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            display: flex;
            align-items: center;
            gap: var(--space-md);
        }
        
        .stat-icon {
            font-size: var(--font-size-2xl);
        }
        
        .stat-value {
            font-size: var(--font-size-2xl);
            font-weight: 700;
            color: white;
            line-height: 1;
        }
        
        .stat-label {
            font-size: var(--font-size-xs);
            color: rgba(255, 255, 255, 0.8);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: var(--space-xs);
        }
        
        /* ============================================
           LOADING STATE
           ============================================ */
        .loading-state {
            text-align: center;
            padding: var(--space-3xl);
        }
        
        .spinner {
            width: 48px;
            height: 48px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top-color: white;
            border-radius: var(--radius-full);
            animation: spin 1s linear infinite;
            margin: 0 auto var(--space-lg);
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .loading-text {
            color: white;
            font-size: var(--font-size-md);
            font-weight: 500;
        }
        
        /* ============================================
           VIDEO PLACEHOLDER
           ============================================ */
        .video-placeholder {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 2px dashed rgba(255, 255, 255, 0.3);
            border-radius: var(--radius-xl);
            padding: var(--space-3xl);
            text-align: center;
        }
        
        .placeholder-icon {
            font-size: 4rem;
            margin-bottom: var(--space-lg);
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .placeholder-title {
            font-size: var(--font-size-xl);
            font-weight: 600;
            color: white;
            margin-bottom: var(--space-sm);
        }
        
        .placeholder-text {
            font-size: var(--font-size-md);
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: var(--space-xl);
        }
        
        .placeholder-tips {
            background: rgba(255, 255, 255, 0.1);
            border-radius: var(--radius-md);
            padding: var(--space-lg);
            max-width: 400px;
            margin: 0 auto;
        }
        
        .tip-item {
            font-size: var(--font-size-sm);
            color: rgba(255, 255, 255, 0.9);
            text-align: left;
            margin-bottom: var(--space-sm);
        }
        
        .tip-item:last-child {
            margin-bottom: 0;
        }
        
        /* ============================================
           STATISTICS GRID
           ============================================ */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: var(--space-md);
            margin-bottom: var(--space-xl);
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            text-align: center;
            box-shadow: var(--shadow-md);
            transition: all var(--transition-base);
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .stat-card-primary {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: white;
        }
        
        .stat-card-secondary {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            color: white;
        }
        
        .stat-card-tertiary {
            background: linear-gradient(135deg, var(--color-success) 0%, #059669 100%);
            color: white;
        }
        
        .stat-card-quaternary {
            background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
            color: white;
        }
        
        .stat-card-icon {
            font-size: var(--font-size-2xl);
            margin-bottom: var(--space-sm);
        }
        
        .stat-card-value {
            font-size: var(--font-size-3xl);
            font-weight: 700;
            line-height: 1;
            margin-bottom: var(--space-xs);
        }
        
        .stat-card-label {
            font-size: var(--font-size-xs);
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* ============================================
           ENHANCED EMPTY STATE
           ============================================ */
        .empty-state-enhanced {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: var(--radius-xl);
            padding: var(--space-3xl);
            text-align: center;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .empty-icon {
            font-size: 5rem;
            margin-bottom: var(--space-lg);
            animation: float 3s ease-in-out infinite;
        }
        
        .empty-title {
            font-size: var(--font-size-2xl);
            font-weight: 700;
            color: white;
            margin-bottom: var(--space-sm);
        }
        
        .empty-subtitle {
            font-size: var(--font-size-md);
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: var(--space-xl);
        }
        
        .setup-checklist {
            background: rgba(255, 255, 255, 0.1);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            margin-bottom: var(--space-xl);
            text-align: left;
        }
        
        .checklist-title {
            font-size: var(--font-size-sm);
            font-weight: 600;
            color: white;
            margin-bottom: var(--space-md);
            text-align: center;
        }
        
        .checklist-item {
            display: flex;
            align-items: center;
            gap: var(--space-md);
            font-size: var(--font-size-sm);
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: var(--space-sm);
        }
        
        .checklist-item:last-child {
            margin-bottom: 0;
        }
        
        .check {
            color: var(--color-success);
            font-weight: 700;
        }
        
        .empty-cta {
            padding-top: var(--space-lg);
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .cta-arrow {
            font-size: var(--font-size-2xl);
            margin-bottom: var(--space-sm);
            animation: bounce 2s ease-in-out infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .cta-text {
            font-size: var(--font-size-md);
            font-weight: 600;
            color: white;
        }
        
        /* ============================================
           CELEBRATION MODAL (NEW PERSONAL BEST)
           ============================================ */
        
        /* Modal Overlay - Full screen with backdrop */
        .celebration-modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            animation: fadeIn 0.4s ease;
            padding: var(--space-xl);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Modal Card - Centered celebration */
        .celebration-modal {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6347 100%);
            border-radius: var(--radius-xl);
            padding: var(--space-3xl);
            text-align: center;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 25px 80px rgba(255, 215, 0, 0.8),
                        0 0 0 1px rgba(255, 255, 255, 0.2);
            animation: celebration-pop 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            overflow: hidden;
        }
        
        @keyframes celebration-pop {
            0% { transform: scale(0.5) rotate(-5deg); opacity: 0; }
            50% { transform: scale(1.05) rotate(2deg); }
            100% { transform: scale(1) rotate(0deg); opacity: 1; }
        }
        
        /* Confetti Background Animation */
        .celebration-confetti-bg {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            pointer-events: none;
            overflow: hidden;
        }
        
        .confetti {
            position: absolute;
            font-size: 2rem;
            animation: confetti-fall 3s linear infinite;
            opacity: 0.8;
        }
        
        .confetti:nth-child(1) { left: 10%; animation-delay: 0s; }
        .confetti:nth-child(2) { left: 25%; animation-delay: 0.3s; }
        .confetti:nth-child(3) { left: 40%; animation-delay: 0.6s; }
        .confetti:nth-child(4) { left: 60%; animation-delay: 0.9s; }
        .confetti:nth-child(5) { left: 75%; animation-delay: 1.2s; }
        .confetti:nth-child(6) { left: 90%; animation-delay: 1.5s; }
        
        @keyframes confetti-fall {
            0% { 
                top: -10%; 
                transform: translateY(0) rotate(0deg);
                opacity: 1;
            }
            100% { 
                top: 110%; 
                transform: translateY(0) rotate(360deg);
                opacity: 0;
            }
        }
        
        /* Icon - Bouncing trophy/party */
        .celebration-icon {
            font-size: 5rem;
            margin-bottom: var(--space-lg);
            animation: celebrate-bounce 0.8s ease infinite;
            position: relative;
            z-index: 1;
        }
        
        @keyframes celebrate-bounce {
            0%, 100% { transform: scale(1) rotate(0deg); }
            25% { transform: scale(1.2) rotate(-10deg); }
            50% { transform: scale(1.1) rotate(0deg); }
            75% { transform: scale(1.2) rotate(10deg); }
        }
        
        /* Title */
        .celebration-title {
            font-size: var(--font-size-3xl);
            font-weight: 800;
            color: white;
            margin-bottom: var(--space-md);
            text-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            letter-spacing: -0.02em;
            position: relative;
            z-index: 1;
        }
        
        /* Count - Big number */
        .celebration-count {
            font-size: 5rem;
            font-weight: 900;
            color: white;
            margin-bottom: var(--space-sm);
            text-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
            line-height: 1;
            animation: pulse-glow 2s ease-in-out infinite;
            position: relative;
            z-index: 1;
        }
        
        /* Duration */
        .celebration-duration {
            font-size: var(--font-size-lg);
            color: rgba(255, 255, 255, 0.95);
            margin-bottom: var(--space-lg);
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            position: relative;
            z-index: 1;
        }
        
        /* Message */
        .celebration-message {
            font-size: var(--font-size-md);
            color: rgba(255, 255, 255, 0.9);
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            position: relative;
            z-index: 1;
        }
        
        /* ============================================
           SESSION HISTORY
           ============================================ */
        .session-date {
            font-size: var(--font-size-sm);
            font-weight: 600;
            color: white;
            margin-bottom: var(--space-xs);
        }
        
        .session-duration {
            font-size: var(--font-size-xs);
            color: rgba(255, 255, 255, 0.8);
        }
        
        .session-count {
            text-align: right;
        }
        
        .count-value {
            font-size: var(--font-size-2xl);
            font-weight: 700;
            color: white;
        }
        
        .count-badge {
            display: block;
            font-size: var(--font-size-xs);
            margin-top: var(--space-xs);
        }
        
        .session-count.pb .count-value {
            color: #FFD700;
        }
        
        /* ============================================
           CONTAINERS & BORDERS
           ============================================ */
        div[data-testid="stVerticalBlock"] > div[style*="border"] {
            background: rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow-md) !important;
        }
        
        /* ============================================
           VIDEO STYLING
           ============================================ */
        video {
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-xl);
            width: 100% !important;
            max-width: 100%;
        }
        
        /* ============================================
           ALERTS & NOTIFICATIONS
           ============================================ */
        .stAlert, .stWarning, .stInfo, .stSuccess {
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: var(--radius-md) !important;
            color: white !important;
            box-shadow: var(--shadow-md) !important;
        }
        
        .stAlert p, .stWarning p, .stInfo p, .stSuccess p {
            color: white !important;
        }
        
        /* ============================================
           PROGRESS BARS
           ============================================ */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-success) 100%) !important;
        }
        
        /* ============================================
           DOWNLOAD BUTTON
           ============================================ */
        .stDownloadButton > button {
            background: linear-gradient(135deg, var(--color-success) 0%, #059669 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-md) !important;
            padding: var(--space-md) var(--space-xl) !important;
            font-size: var(--font-size-md) !important;
            font-weight: 600 !important;
            min-height: 56px !important;
            transition: all var(--transition-base) !important;
            box-shadow: var(--shadow-md) !important;
            cursor: pointer !important;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-lg) !important;
        }
        
        /* ============================================
           EXPANDER (COLLAPSIBLE SECTIONS)
           ============================================ */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: var(--radius-md) !important;
            color: white !important;
            font-weight: 600 !important;
        }
        
        .streamlit-expanderHeader:hover {
            background: rgba(255, 255, 255, 0.15) !important;
        }
        
        /* ============================================
           HIDE STREAMLIT BRANDING
           ============================================ */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
        header {visibility: hidden;}
        
        /* ============================================
           RESPONSIVE DESIGN - MOBILE FIRST
           ============================================ */
        @media (max-width: 768px) {
            .block-container {
                padding: var(--space-lg) var(--space-md) !important;
            }
            
            .counter-value {
                font-size: var(--font-size-5xl);
            }
            
            .session-stats-compact {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .stat-item {
                flex-direction: column;
                text-align: center;
            }
            
            .header-container h1 {
                font-size: var(--font-size-2xl) !important;
            }
            
            /* Celebration modal mobile adjustments */
            .celebration-modal {
                padding: var(--space-xl);
                max-width: 90%;
            }
            
            .celebration-icon {
                font-size: 4rem;
            }
            
            .celebration-title {
                font-size: var(--font-size-2xl);
            }
            
            .celebration-count {
                font-size: 4rem;
            }
        }
        
        /* ============================================
           ACCESSIBILITY
           ============================================ */
        /* Focus visible states for keyboard navigation */
        *:focus-visible {
            outline: 3px solid rgba(102, 126, 234, 0.5);
            outline-offset: 2px;
        }
        
        /* Skip to content link for screen readers */
        .skip-to-content {
            position: absolute;
            left: -9999px;
            z-index: 999;
            padding: var(--space-md);
            background: white;
            color: var(--color-primary);
            text-decoration: none;
        }
        
        .skip-to-content:focus {
            left: 50%;
            transform: translateX(-50%);
        }
        
        /* ============================================
           SMOOTH TRANSITIONS
           ============================================ */
        * {
            transition: background-color var(--transition-base), 
                        border-color var(--transition-base), 
                        color var(--transition-base),
                        transform var(--transition-base);
        }
        
        /* Disable transitions for reduced motion */
        @media (prefers-reduced-motion: reduce) {
            * {
                transition: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
