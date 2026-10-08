"""
Custom CSS and Styling Helpers for Streamlit Dashboard.
Implements modern dark-mode aesthetics with glassmorphic cards and badges.
"""

import streamlit as st

def inject_custom_css():
    """Injects bespoke CSS for a dark sports analytics interface."""
    st.markdown(
        """
        <style>
        /* Base typography and background */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Container background adjustments */
        .stApp {
            background-color: #0b0f17;
        }

        /* Card container styling */
        .analytics-card {
            background: linear-gradient(135deg, rgba(22, 27, 34, 0.95), rgba(15, 23, 42, 0.85));
            border: 1px solid rgba(48, 54, 61, 0.8);
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
            margin-bottom: 20px;
        }

        /* Metric badge styling */
        .metric-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .badge-idn {
            background-color: rgba(230, 57, 70, 0.2);
            color: #ff6b6b;
            border: 1px solid rgba(230, 57, 70, 0.4);
        }

        .badge-tha {
            background-color: rgba(29, 140, 248, 0.2);
            color: #60a5fa;
            border: 1px solid rgba(29, 140, 248, 0.4);
        }

        .badge-gold {
            background-color: rgba(245, 158, 11, 0.2);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }

        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-weight: 800;
            color: #f0f6fc !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-weight: 600;
            color: #8b949e !important;
            font-size: 0.85rem !important;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        /* Hero banner */
        .hero-banner {
            background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 50%, #111827 100%);
            border: 1px solid #312e81;
            border-radius: 16px;
            padding: 32px 36px;
            margin-bottom: 28px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        }

        /* Custom tables */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
        }

        /* Section header badge */
        .section-tag {
            font-size: 0.8rem;
            font-weight: 700;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
