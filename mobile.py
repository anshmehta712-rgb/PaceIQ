"""Responsive layout overrides for PaceIQ.

This module changes presentation only. It does not affect
video processing, pose tracking or AI analysis.
"""

import streamlit as st


def apply_mobile_styles():
    st.markdown(
        """
<style>
/* Desktop gets the original three-button navigation. */
.st-key-mobile_navigation {
    display: none !important;
}

.st-key-desktop_navigation {
    display: block !important;
}

/* Keep embedded media and layout columns within the viewport. */
.stApp img,
.stApp video,
.stApp canvas {
    max-width: 100%;
}

[data-testid="stHorizontalBlock"] > div,
[data-testid="stVerticalBlock"] {
    min-width: 0;
}

.pace-title,
.pace-section-title,
.pace-tile-title,
.pace-brand-name {
    overflow-wrap: break-word;
}

/* Tablet spacing */
@media (min-width: 701px) and (max-width: 950px) {
    .block-container {
        padding-left: 1.4rem !important;
        padding-right: 1.4rem !important;
    }

    .pace-title {
        font-size: clamp(2.8rem, 5.5vw, 4.8rem) !important;
    }

    .pace-viz {
        min-height: 360px !important;
    }

    .pace-viz img {
        height: 335px !important;
    }
}

/* Phones and narrower devices */
@media (max-width: 700px) {
    .st-key-desktop_navigation {
        display: none !important;
    }

    .st-key-mobile_navigation {
        display: block !important;
        width: 100% !important;
        margin: 0.15rem 0 0.75rem;
    }

    .st-key-mobile_navigation [data-baseweb="select"] > div {
        background: #112632 !important;
        border: 1px solid rgba(138, 247, 178, 0.35) !important;
        border-radius: 12px !important;
        min-height: 48px;
    }

    .block-container {
        max-width: 100% !important;
        padding: 0.8rem 0.9rem 2rem !important;
    }

    .pace-brand {
        gap: 8px !important;
        padding: 3px 0 8px !important;
    }

    .pace-brand-name {
        font-size: 22px !important;
        letter-spacing: -0.045em !important;
    }

    .pace-brand-logo {
        width: 32px !important;
        height: 32px !important;
        font-size: 18px !important;
        margin-right: 7px !important;
    }

    .pace-brand-right {
        display: none !important;
    }

    .pace-hero-wrap {
        padding: 15px 0 14px !important;
    }

    .pace-eyebrow {
        font-size: 9px !important;
        letter-spacing: 0.13em !important;
    }

    .pace-eyebrow:before {
        width: 18px !important;
    }

    .pace-title {
        font-size: clamp(2.35rem, 10.3vw, 3.7rem) !important;
        line-height: 1.04 !important;
        letter-spacing: -0.062em !important;
        margin: 15px 0 17px !important;
    }

    .pace-lede {
        max-width: 100% !important;
        font-size: 0.95rem !important;
        line-height: 1.58 !important;
        margin: 0 0 16px !important;
    }

    .pace-micro-row {
        gap: 9px 15px !important;
        margin: 15px 0 6px !important;
    }

    .pace-micro-row span {
        font-size: 10px !important;
        letter-spacing: 0.025em;
    }

    .pace-viz {
        min-height: 300px !important;
        border-radius: 18px !important;
        margin-top: 7px;
    }

    .pace-viz img {
        height: 280px !important;
        max-width: 100%;
        object-fit: contain;
    }

    .pace-viz-head {
        top: 14px !important;
        left: 15px !important;
        right: 15px !important;
        font-size: 9px !important;
        letter-spacing: 0.06em !important;
    }

    .pace-viz-head span:last-child {
        display: none;
    }

    .pace-viz-foot {
        left: 14px !important;
        right: 14px !important;
        bottom: 12px !important;
        font-size: 9px !important;
        letter-spacing: 0.05em !important;
    }

    .pace-viz-foot span:last-child {
        display: none;
    }

    .pace-user-photo {
        max-width: min(70vw, 240px) !important;
    }

    .pace-strip {
        display: flex !important;
        flex-direction: column !important;
        gap: 7px !important;
        padding: 12px 2px !important;
        font-size: 10px !important;
    }

    .pace-section-top {
        padding: 17px 0 10px !important;
        gap: 8px !important;
    }

    .pace-section-title {
        font-size: clamp(1.55rem, 7vw, 2.2rem) !important;
        line-height: 1.17 !important;
    }

    .pace-section-sub {
        font-size: 13px !important;
        line-height: 1.52 !important;
    }

    .pace-tile {
        min-height: 0 !important;
        padding: 20px !important;
        border-radius: 16px !important;
        margin-bottom: 0 !important;
    }

    .pace-tile-title {
        margin: 14px 0 6px !important;
        font-size: 21px !important;
    }

    .pace-tile-body {
        max-width: 100% !important;
        font-size: 13px !important;
    }

    .pace-band {
        padding: 22px 18px !important;
        border-radius: 16px !important;
    }

    .pace-band h3 {
        font-size: 24px !important;
        line-height: 1.17 !important;
    }

    .pace-banner {
        padding: 23px 18px !important;
        border-radius: 16px !important;
        margin: 10px 0 18px !important;
    }

    .pace-banner h1 {
        font-size: clamp(1.9rem, 8vw, 2.7rem) !important;
        line-height: 1.11 !important;
    }

    .pace-banner p {
        font-size: 14px !important;
        line-height: 1.55 !important;
    }

    .pace-story-quote {
        padding: 19px 18px !important;
        font-size: 20px !important;
        line-height: 1.35 !important;
    }

    .pace-story-card {
        min-height: 0 !important;
        padding: 19px !important;
    }

    .pace-story-card h3 {
        font-size: 21px !important;
        margin: 11px 0 7px !important;
    }

    .pace-footer {
        margin-top: 26px !important;
        gap: 7px !important;
    }

    .pace-footer span {
        font-size: 9px !important;
    }

    /* Keep the three Motion Lab tabs accessible by horizontal swipe. */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
        overflow-x: auto !important;
        max-width: 100%;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: thin;
        padding: 6px !important;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 0 0 auto !important;
        white-space: nowrap !important;
        min-height: 44px !important;
        padding: 9px 12px !important;
        font-size: 12px !important;
    }

    [data-testid="stMetric"] {
        padding: 12px 14px !important;
        border-radius: 13px !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        min-height: 44px !important;
        white-space: normal !important;
        line-height: 1.25 !important;
    }

    [data-testid="stDataFrame"],
    [data-testid="stVegaLiteChart"] {
        max-width: 100% !important;
    }
}

/* Small phones, including a 320px viewport. */
@media (max-width: 380px) {
    .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }

    .pace-title {
        font-size: clamp(2.12rem, 10vw, 2.5rem) !important;
    }

    .pace-viz {
        min-height: 270px !important;
    }

    .pace-viz img {
        height: 250px !important;
    }

    .pace-section-title {
        font-size: 1.65rem !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    div.stButton > button,
    div.stDownloadButton > button {
        transition: none !important;
        transform: none !important;
    }
}
</style>
        """,
        unsafe_allow_html=True,
    )
