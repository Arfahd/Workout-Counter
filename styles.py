"""
CSS styles for the Pushup Counter application.
Contains all the custom styling for the Streamlit interface.
"""

import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app."""

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

    # Linear.app inspired CSS
    st.markdown(
        """
        <style>
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif;
        }
        
        /* Main container with VIBRANT animated gradient mesh */
        body {
            margin: 0;
            padding: 0;
        }
        
        .stApp, [data-testid="stAppViewContainer"], .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 20%, #f093fb 40%, #4facfe 60%, #43e97b 80%, #667eea 100%) !important;
            background-size: 400% 400% !important;
            animation: gradient-mesh 15s ease infinite !important;
            min-height: 100vh;
        }
        
        /* Add floating gradient orbs overlay */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.4) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(240, 147, 251, 0.4) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(79, 172, 254, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 60% 60%, rgba(67, 233, 123, 0.3) 0%, transparent 50%);
            animation: float-bubbles 20s ease infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes gradient-mesh {
            0% { background-position: 0% 50%; }
            25% { background-position: 50% 100%; }
            50% { background-position: 100% 50%; }
            75% { background-position: 50% 0%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes float-bubbles {
            0%, 100% { 
                transform: translate(0, 0) scale(1);
                opacity: 0.4;
            }
            33% { 
                transform: translate(50px, -50px) scale(1.2);
                opacity: 0.6;
            }
            66% { 
                transform: translate(-30px, 30px) scale(0.8);
                opacity: 0.5;
            }
        }
        
        /* Ensure content is above the animated background */
        .block-container {
            position: relative;
            z-index: 1;
        }
        
        /* Remove Streamlit default padding */
        .block-container {
            padding: 3rem 2rem 2rem 2rem !important;
            max-width: 1280px !important;
            margin-top: 0 !important;
        }
        
        /* Header styles with gradient */
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-bottom: none;
            padding: 2.5rem 0 1.5rem 0;
            margin: 0 -2rem 2rem -2rem;
            margin-top: -3rem;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        }
        
        h1 {
            font-size: 1.875rem !important;
            font-weight: 600 !important;
            color: white !important;
            letter-spacing: -0.025em !important;
            margin: 0 !important;
            padding: 0 2rem !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        .subtitle {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.9);
            margin-top: 0.25rem;
            font-weight: 400;
        }
        
        /* Card styles with glassmorphism */
        .status-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .status-card:hover {
            background: rgba(255, 255, 255, 0.25);
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }
        
        .status-card-active {
            background: rgba(16, 185, 129, 0.2);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 2px solid rgba(16, 185, 129, 0.5);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
            animation: pulse-glow 2s ease infinite;
        }
        
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3); }
            50% { box-shadow: 0 8px 40px rgba(16, 185, 129, 0.5); }
        }
        
        .status-card-active::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #10B981, #34D399, #10B981);
            background-size: 200% 100%;
            animation: shimmer-line 2s linear infinite;
        }
        
        @keyframes shimmer-line {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        
        /* Status badge */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            font-weight: 600;
            padding: 0.375rem 1rem;
            border-radius: 9999px;
            margin-bottom: 0.75rem;
            letter-spacing: 0.05em;
        }
        
        .status-active {
            background: linear-gradient(135deg, #0ba360 0%, #3cba92 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(11, 163, 96, 0.5), 0 0 30px rgba(16, 185, 129, 0.3);
        }
        
        .status-inactive {
            background: linear-gradient(135deg, #6B7280 0%, #9CA3AF 100%);
            color: white;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
            box-shadow: 0 2px 10px rgba(107, 114, 128, 0.3);
        }
        
        /* Enhanced status indicator dots */
        .status-dot {
            display: inline-block;
            border-radius: 50%;
            position: relative;
        }
        
        /* IDLE dot - white with glow */
        .status-inactive .status-dot {
            width: 12px;
            height: 12px;
            background: white;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.8), 
                        0 0 20px rgba(255, 255, 255, 0.4),
                        inset 0 0 5px rgba(156, 163, 175, 0.5);
            animation: idle-pulse 3s ease-in-out infinite;
        }
        
        @keyframes idle-pulse {
            0%, 100% { 
                opacity: 0.8;
                transform: scale(1);
            }
            50% { 
                opacity: 1;
                transform: scale(1.1);
            }
        }
        
        /* LIVE dot - bright green with strong animated glow */
        .status-active .status-dot {
            width: 14px;
            height: 14px;
            background: #10B981;
            box-shadow: 0 0 15px rgba(16, 185, 129, 1), 
                        0 0 30px rgba(16, 185, 129, 0.6),
                        0 0 45px rgba(16, 185, 129, 0.3),
                        inset 0 0 5px rgba(255, 255, 255, 0.5);
            animation: live-glow 1.5s ease-in-out infinite;
        }
        
        @keyframes live-glow {
            0%, 100% { 
                box-shadow: 0 0 15px rgba(16, 185, 129, 1), 
                            0 0 30px rgba(16, 185, 129, 0.6),
                            0 0 45px rgba(16, 185, 129, 0.3),
                            inset 0 0 5px rgba(255, 255, 255, 0.5);
                transform: scale(1);
            }
            50% { 
                box-shadow: 0 0 20px rgba(16, 185, 129, 1), 
                            0 0 40px rgba(16, 185, 129, 0.8),
                            0 0 60px rgba(16, 185, 129, 0.5),
                            inset 0 0 8px rgba(255, 255, 255, 0.7);
                transform: scale(1.15);
            }
        }
        
        /* Typography with better contrast */
        .card-title {
            font-size: 1rem;
            font-weight: 600;
            color: white;
            margin-bottom: 0.25rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .card-description {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.9);
            line-height: 1.5;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }
        
        /* Metric cards with gradients */
        .metric-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border: none;
            border-radius: 0.5rem;
            padding: 1rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
        }
        
        .metric-card:nth-child(2) {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        }
        
        .metric-card:nth-child(3) {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            box-shadow: 0 4px 15px rgba(67, 233, 123, 0.3);
        }
        
        .metric-label {
            font-size: 0.75rem;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.9);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: white;
            letter-spacing: -0.025em;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        /* Buttons with gradient */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 0.375rem !important;
            padding: 0.5rem 1rem !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        /* Primary button with gradient */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%) !important;
            box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6) !important;
        }
        
        /* Secondary button with subtle gradient */
        .stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%) !important;
            color: #111827 !important;
            border: 1px solid #E5E7EB !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #e3e3e3 0%, #d4d4d4 100%) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Video container with gradient */
        .video-container {
            background: rgba(17, 24, 39, 0.8);
            backdrop-filter: blur(20px);
            border: 2px solid rgba(139, 92, 246, 0.5);
            border-radius: 1rem;
            padding: 1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 0 40px rgba(139, 92, 246, 0.3);
            position: relative;
        }
        
        .video-container::before {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 1rem;
            padding: 2px;
            background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0.6;
            animation: rotate-border 3s linear infinite;
        }
        
        @keyframes rotate-border {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
        
        .video-placeholder {
            background: rgba(249, 250, 251, 0.1);
            backdrop-filter: blur(10px);
            border: 2px dashed rgba(255, 255, 255, 0.3);
            border-radius: 1rem;
            padding: 3rem;
            text-align: center;
        }
        
        /* Table styles */
        .dataframe {
            font-size: 0.875rem !important;
            background: white !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 0.5rem !important;
        }
        
        .dataframe thead {
            background: #F9FAFB !important;
        }
        
        .dataframe th {
            font-weight: 500 !important;
            color: #6B7280 !important;
            text-transform: uppercase !important;
            font-size: 0.75rem !important;
            letter-spacing: 0.05em !important;
        }
        
        .dataframe td {
            color: #111827 !important;
            border-color: #F3F4F6 !important;
        }
        
        /* Info/Alert boxes */
        .stAlert {
            background: white !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 0.5rem !important;
            color: #374151 !important;
            font-size: 0.875rem !important;
        }
        
        .stInfo {
            background: #EFF6FF !important;
            border: 1px solid #DBEAFE !important;
            border-left: 3px solid #3B82F6 !important;
        }
        
        .stSuccess {
            background: #F0FDF4 !important;
            border: 1px solid #BBF7D0 !important;
            border-left: 3px solid #10B981 !important;
        }
        
        .stWarning {
            background: #FFFBEB !important;
            border: 1px solid #FEF3C7 !important;
            border-left: 3px solid #F59E0B !important;
            color: #92400E !important;
        }
        
        .stWarning > div {
            color: #92400E !important;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: white !important;
            border-right: 1px solid #E5E7EB !important;
        }
        
        /* Divider */
        hr {
            border: none !important;
            border-top: 1px solid #E5E7EB !important;
            margin: 1.5rem 0 !important;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Section headers with glow */
        h3 {
            font-size: 0.875rem !important;
            font-weight: 600 !important;
            color: white !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            margin-bottom: 1rem !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3), 0 0 20px rgba(255, 255, 255, 0.2);
        }
        
        /* Empty state with glassmorphism */
        .empty-state {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 1rem;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .empty-state-icon {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .empty-state-text {
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.875rem;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }
        
        .empty-state-text strong {
            color: white;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        /* Metric grid */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
            margin-bottom: 1rem;
        }
        
        /* Real-time counter display */
        .counter-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 1rem;
            padding: 2rem;
            text-align: center;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .counter-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: rotate(45deg);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .counter-label {
            font-size: 0.875rem;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.9);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.5rem;
        }
        
        .counter-value {
            font-size: 4.5rem;
            font-weight: 700;
            color: white;
            letter-spacing: -0.05em;
            line-height: 1;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            animation: pulse-counter 0.3s ease;
        }
        
        @keyframes pulse-counter {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .counter-sublabel {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 0.5rem;
            font-weight: 400;
        }
        
        /* Timer display with gradient */
        .timer-display {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            border: none;
            border-radius: 0.5rem;
            padding: 1rem;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(250, 112, 154, 0.3);
        }
        
        .timer-display:nth-of-type(2) {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            box-shadow: 0 4px 15px rgba(168, 237, 234, 0.3);
        }
        
        .timer-value {
            font-size: 2rem;
            font-weight: 600;
            color: white;
            font-variant-numeric: tabular-nums;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        .timer-label {
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.9);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.25rem;
        }
        
        /* Colorful progress bars */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
            background-size: 200% 100% !important;
            animation: progress-flow 2s linear infinite !important;
        }
        
        @keyframes progress-flow {
            0% { background-position: 0% 50%; }
            100% { background-position: 200% 50%; }
        }
        
        /* Confidence indicator animations */
        @keyframes confidence-pulse {
            0%, 100% { 
                opacity: 1;
                transform: scale(1);
            }
            50% { 
                opacity: 0.8;
                transform: scale(1.05);
            }
        }
        
        .confidence-excellent {
            animation: confidence-pulse 2s ease-in-out infinite;
        }
        
        /* Progress circle */
        .progress-circle {
            position: relative;
            width: 120px;
            height: 120px;
            margin: 0 auto 1rem;
        }
        
        .progress-circle svg {
            transform: rotate(-90deg);
        }
        
        .progress-circle-bg {
            fill: none;
            stroke: #E5E7EB;
            stroke-width: 8;
        }
        
        .progress-circle-progress {
            fill: none;
            stroke: url(#gradient);
            stroke-width: 8;
            stroke-linecap: round;
            transition: stroke-dashoffset 0.5s ease;
        }
        
        .progress-circle-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.5rem;
            font-weight: 600;
            color: #111827;
        }
        
        /* Celebration animation */
        @keyframes celebrate {
            0%, 100% { transform: scale(1) rotate(0deg); }
            25% { transform: scale(1.2) rotate(-5deg); }
            75% { transform: scale(1.2) rotate(5deg); }
        }
        
        .celebrating {
            animation: celebrate 0.5s ease;
        }
        
        /* Glassmorphism effect */
        .glass-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        /* Apply glassmorphism to Streamlit containers */
        div[data-testid="stVerticalBlock"] > div[data-testid="column"] > div {
            background: transparent;
        }
        
        /* Container borders with glassmorphism */
        div[data-testid="stVerticalBlock"] > div[style*="border"] {
            background: rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 1rem !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
        }
        
        /* Streamlit container styling */
        .element-container {
            background: transparent !important;
        }
        
        /* WebRTC video styling - CENTERED AND LARGER */
        video {
            border-radius: 0.75rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            display: block;
            margin: 0 auto;
            max-width: 100%;
            width: 100% !important;
        }
        
        /* WebRTC container */
        .streamlit-webrtc {
            border-radius: 1rem;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        /* Alert/Warning boxes on gradient background */
        .stAlert, .stWarning, .stInfo, .stSuccess {
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 0.75rem !important;
            color: white !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
        }
        
        .stAlert p, .stWarning p, .stInfo p, .stSuccess p {
            color: rgba(255, 255, 255, 0.95) !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Smooth transitions */
        * {
            transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
        }
        
        /* Enhanced hover effects */
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .status-card:hover {
            border-color: #D1D5DB;
        }
        
        /* Skeleton loading */
        .skeleton {
            background: linear-gradient(90deg, #F3F4F6 25%, #E5E7EB 50%, #F3F4F6 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* Personal best badge with animation */
        .pb-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            background: linear-gradient(135deg, #FFD700, #FFA500, #FF6347);
            background-size: 200% 200%;
            animation: gradient-shift 3s ease infinite;
            color: white;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: 0 2px 10px rgba(255, 215, 0, 0.5);
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        }
        
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Stats overlay on video */
        .video-overlay {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            color: white;
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            font-size: 0.875rem;
            font-weight: 500;
            z-index: 10;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .metric-grid {
                grid-template-columns: 1fr;
            }
            
            .counter-value {
                font-size: 3rem;
            }
            
            .block-container {
                padding: 2rem 1rem !important;
            }
            
            .header-container {
                padding: 2rem 0 1rem 0;
            }
        }
        
        /* Success animation */
        @keyframes success-pop {
            0% { transform: scale(0.8); opacity: 0; }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .success-message {
            animation: success-pop 0.5s ease;
        }
        
        /* Chart container with glassmorphism */
        .chart-container {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 1rem;
            padding: 1rem;
            margin-top: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        /* Download button styling */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 0.5rem !important;
            font-weight: 500 !important;
            box-shadow: 0 4px 15px rgba(67, 233, 123, 0.4) !important;
            transition: all 0.2s ease !important;
        }
        
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #38f9d7 0%, #43e97b 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(67, 233, 123, 0.6) !important;
        }
        
        /* Fix text readability - remove default highlights but preserve custom backgrounds */
        .stMarkdown > div:not(.counter-container):not(.timer-display):not(.metric-card):not(.status-card):not(.status-card-active) p,
        .stMarkdown > div:not(.counter-container):not(.timer-display):not(.metric-card):not(.status-card):not(.status-card-active) span:not(.counter-value):not(.counter-label):not(.counter-sublabel):not(.status-dot) {
            background: transparent !important;
        }
        
        /* Fix caption readability on colorful background */
        .stCaptionContainer p {
            color: rgba(255, 255, 255, 0.85) !important;
            background: transparent !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Remove any text selection highlights */
        ::selection {
            background: rgba(255, 255, 255, 0.3);
            color: white;
        }
        
        /* Fix bold text in session cards */
        [data-testid="stVerticalBlock"] strong {
            color: white !important;
            background: transparent !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Preserve counter container gradient */
        .counter-container,
        .counter-container * {
            background: inherit !important;
        }
        
        .counter-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        /* Session container glassmorphism */
        [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-radius: 1rem !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
