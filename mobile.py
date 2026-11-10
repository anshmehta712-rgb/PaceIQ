"""PaceIQ mobile presentation rules.

All rendering changes are CSS only; the tracking, video-processing,
measurement and local AI routines remain unmodified.
"""

import streamlit as st


def apply_mobile_styles():
    st.markdown(
        """
<style>
/* Responsive navigation: show only the appropriate control. */
.st-key-mobile_navigation {
    display: none !important;
}

.st-key-desktop_navigation {
    display: block !important;
}

/* Media must never escape the content container. */
.stApp video,
.stApp canvas,
.stApp img,
.stApp svg {
    max-width: 100%;
}

.stApp [data-testid="stDataFrame"],
.stApp [data-testid="stVegaLiteChart"] {
    max-width: 100%;
}

/* Protect against large text forcing horizontal page scrolling. */
.pace-title,
.pace-section-title,
.pace-tile-title,
.pace-banner h1,
.pace-brand-name {
    overflow-wrap: anywhere;
}

/* Compact tablet experience without changing the desktop structure. */
@media (min-width: 769px) and (max-width: 1040px) {
    .block-container {
        max-width: 100% !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    .pace-title {
        font-size: clamp(2.5rem, 6vw, 4.7rem) !important;
    }

    .pace-viz {
        min-height: 360px !important;
    }

    .pace-viz img {
        height: 330px !important;
    }
}

/* PHONE: build a true single-column layout instead of squeezing columns. */
@media (max-width: 768px) {
    html,
    body,
    .stApp {
        overflow-x: clip !important;
    }

    .st-key-desktop_navigation {
        display: none !important;
    }

    .st-key-mobile_navigation {
        display: block !important;
        width: 100% !important;
        margin-bottom: 0.65rem;
    }

    .st-key-mobile_navigation [data-baseweb="select"] > div {
        min-height: 48px;
        border-radius: 12px !important;
        background: #122b34 !important;
        border: 1px solid rgba(138, 247, 178, .42) !important;
    }

    /* This is the main fix: force Streamlit's actual columns to stack. */
    .stApp [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: column !important;
        flex-wrap: nowrap !important;
        align-items: stretch !important;
        gap: 0.9rem !important;
        width: 100% !important;
        min-width: 0 !important;
    }

    .stApp [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    .stApp [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        flex: 0 0 auto !important;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        margin: 0 !important;
    }

    .stApp [data-testid="stVerticalBlock"],
    .stApp [data-testid="stElementContainer"],
    .stApp [data-testid="stMarkdownContainer"] {
        max-width: 100%;
        min-width: 0 !important;
    }

    .block-container,
    [data-testid="stMainBlockContainer"] {
        max-width: 100% !important;
        padding: 0.8rem 1rem 2rem !important;
    }

    h1, h2, h3 {
        overflow-wrap: anywhere;
    }

    .pace-brand {
        padding: 0 0 10px !important;
        gap: 8px !important;
    }

    .pace-brand-name {
        font-size: 22px !important;
        letter-spacing: -.04em !important;
    }

    .pace-brand-logo {
        width: 34px !important;
        height: 34px !important;
        margin-right: 7px !important;
        font-size: 19px !important;
    }

    .pace-brand-right {
        display: none !important;
    }

    .pace-hero-wrap {
        padding: 15px 0 12px !important;
    }

    .pace-eyebrow {
        font-size: 10px !important;
        letter-spacing: .11em !important;
        line-height: 1.5;
    }

    .pace-eyebrow:before {
        width: 18px !important;
    }

    .pace-title {
        font-size: clamp(2.25rem, 10.5vw, 3.65rem) !important;
        line-height: 1.04 !important;
        letter-spacing: -.055em !important;
        margin: 14px 0 18px !important;
        overflow-wrap: normal !important;
        word-break: normal !important;
    }

    .pace-lede {
        font-size: 15px !important;
        line-height: 1.55 !important;
        max-width: 100% !important;
        margin: 0 0 13px !important;
    }

    .pace-micro-row {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 9px 12px !important;
        margin: 13px 0 5px !important;
    }

    .pace-micro-row span {
        font-size: 10px !important;
    }

    .pace-viz {
        min-height: 0 !important;
        border-radius: 18px !important;
        padding-bottom: 32px;
        margin-top: 4px;
    }

    .pace-viz img {
        height: 270px !important;
        object-fit: contain !important;
        max-width: 100% !important;
    }

    .pace-viz-head {
        top: 15px !important;
        left: 15px !important;
        right: 15px !important;
        font-size: 9px !important;
        letter-spacing: .075em !important;
    }

    .pace-viz-head span:last-child,
    .pace-viz-foot span:last-child {
        display: none !important;
    }

    .pace-viz-foot {
        bottom: 12px !important;
        left: 15px !important;
        right: 15px !important;
        font-size: 9px !important;
        letter-spacing: .04em !important;
    }

    .pace-user-photo {
        max-width: min(68vw, 230px) !important;
        margin-top: 35px !important;
    }

    .pace-strip {
        display: flex !important;
        flex-direction: column !important;
        align-items: start !important;
        gap: 8px !important;
        padding: 13px 2px !important;
        font-size: 10px !important;
    }

    .pace-section-top {
        gap: 8px !important;
        padding: 18px 0 12px !important;
    }

    .pace-section-label {
        font-size: 10px !important;
        letter-spacing: .13em !important;
    }

    .pace-section-title {
        font-size: clamp(1.6rem, 7vw, 2.3rem) !important;
        line-height: 1.14 !important;
    }

    .pace-section-sub {
        font-size: 13px !important;
        line-height: 1.55 !important;
        max-width: 100% !important;
    }

    .pace-tile,
    .pace-story-card {
        min-height: 0 !important;
        height: auto !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin: 0 0 3px !important;
    }

    .pace-tile-title {
        font-size: 22px !important;
        margin: 12px 0 7px !important;
    }

    .pace-tile-body {
        font-size: 13px !important;
        line-height: 1.55 !important;
        max-width: 100% !important;
    }

    .pace-banner {
        padding: 22px 18px !important;
        border-radius: 17px !important;
        margin: 8px 0 16px !important;
    }

    .pace-banner h1 {
        font-size: clamp(2rem, 8.5vw, 2.75rem) !important;
        line-height: 1.08 !important;
    }

    .pace-banner p {
        font-size: 14px !important;
        line-height: 1.5 !important;
    }

    .pace-band {
        padding: 20px !important;
        border-radius: 16px !important;
    }

    .pace-band h3 {
        font-size: 24px !important;
        line-height: 1.2 !important;
    }

    .pace-story-quote {
        padding: 19px !important;
        font-size: 21px !important;
        line-height: 1.35 !important;
    }

    .pace-story-card h3 {
        font-size: 21px !important;
        margin: 12px 0 8px !important;
    }

    .pace-footer {
        flex-direction: column !important;
        gap: 6px !important;
        margin-top: 24px !important;
        padding: 15px 0 !important;
    }

    .pace-footer span {
        font-size: 10px !important;
    }

    /* Scrolling tabs are more usable than three squeezed labels. */
    .stTabs {
        max-width: 100%;
        min-width: 0;
    }

    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        width: 100% !important;
        max-width: 100% !important;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: thin;
        gap: 5px !important;
        padding: 6px !important;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 0 0 auto !important;
        min-width: max-content !important;
        white-space: nowrap !important;
        font-size: 12px !important;
        min-height: 44px !important;
        padding: 8px 11px !important;
    }

    [data-testid="stMetric"] {
        padding: 13px 16px !important;
        min-width: 0 !important;
        border-radius: 13px !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.55rem !important;
    }

    [data-testid="stFileUploader"] {
        max-width: 100%;
    }

    [data-testid="stFileUploader"] section {
        padding: 10px !important;
    }

    [data-testid="stSlider"] {
        max-width: 100%;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        min-height: 46px !important;
        line-height: 1.25 !important;
        white-space: normal !important;
        border-radius: 12px !important;
        touch-action: manipulation;
    }

    div.stButton,
    div.stDownloadButton {
        width: 100% !important;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        width: 100% !important;
    }

    .stApp [data-testid="stDataFrame"],
    .stApp [data-testid="stVegaLiteChart"] {
        max-width: 100% !important;
        overflow-x: auto !important;
    }
}

/* Extremely small phones. */
@media (max-width: 370px) {
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-left: .75rem !important;
        padding-right: .75rem !important;
    }

    .pace-title {
        font-size: 2.05rem !important;
    }

    .pace-viz img {
        height: 240px !important;
    }

    .pace-user-photo {
        max-width: 205px !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    div.stButton > button,
    div.stDownloadButton > button {
        transition: none !important;
        transform: none !important;
    }
}

/*
 * Responsive homepage grids are based on their actual container width.
 * They do not depend on Safari's viewport or Streamlit column internals.
 */
.pace-feature-grid,
.pace-process-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 270px), 1fr)) !important;
    gap: 18px !important;
    width: 100% !important;
    min-width: 0 !important;
    margin: 12px 0 24px !important;
    box-sizing: border-box !important;
}

.pace-feature-grid > .pace-tile {
    box-sizing: border-box !important;
    min-width: 0 !important;
    width: 100% !important;
    height: auto !important;
    min-height: 210px !important;
    overflow-wrap: normal !important;
    word-break: normal !important;
    padding: 24px !important;
}

.pace-feature-grid .pace-tile-title,
.pace-feature-grid .pace-tile-body {
    overflow-wrap: normal !important;
    word-break: normal !important;
    white-space: normal !important;
    max-width: 100% !important;
}

.pace-feature-grid .pace-tile-title {
    font-size: clamp(21px, 2.3vw, 26px) !important;
    margin: 20px 0 10px !important;
    line-height: 1.18 !important;
}

.pace-feature-grid .pace-tile-body {
    font-size: 14px !important;
    line-height: 1.6 !important;
}

.pace-process-step {
    min-width: 0;
    padding: 12px 4px 16px;
}

.pace-process-step h3 {
    font-size: 20px;
    line-height: 1.25;
    margin: 0 0 8px;
}

.pace-process-step p {
    font-size: 14px;
    line-height: 1.6;
    color: #a8bbc2;
    margin: 0;
}

@media (max-width: 768px) {
    .pace-feature-grid,
    .pace-process-grid {
        grid-template-columns: minmax(0, 1fr) !important;
        gap: 12px !important;
    }

    .pace-feature-grid > .pace-tile {
        min-height: 0 !important;
        padding: 22px !important;
    }

    .pace-feature-grid .pace-tile-title {
        font-size: 23px !important;
        margin: 14px 0 8px !important;
    }

    .pace-process-step {
        padding: 12px 4px !important;
    }
}


/* My Story chapter cards: auto-fit, never three squeezed phone columns. */
.pace-story-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 270px), 1fr)) !important;
    gap: 18px !important;
    width: 100% !important;
    min-width: 0 !important;
    margin: 16px 0 28px !important;
}

.pace-story-grid > .pace-story-card {
    box-sizing: border-box !important;
    width: 100% !important;
    min-width: 0 !important;
    min-height: 0 !important;
    height: auto !important;
    overflow-wrap: normal !important;
    word-break: normal !important;
    padding: 25px !important;
}

.pace-story-grid .pace-story-card h3,
.pace-story-grid .pace-story-card p {
    overflow-wrap: normal !important;
    word-break: normal !important;
    white-space: normal !important;
}

.pace-story-grid .pace-story-card h3 {
    font-size: 23px !important;
    line-height: 1.22 !important;
}

.pace-story-grid .pace-story-card p {
    font-size: 14px !important;
    line-height: 1.6 !important;
}

/* Scope the photo and opening story columns to a phone-friendly layout. */
@media (max-width: 768px) {
    .pace-story-grid {
        grid-template-columns: minmax(0, 1fr) !important;
        gap: 12px !important;
    }

    .pace-story-grid > .pace-story-card {
        padding: 21px !important;
    }

    .pace-story-grid .pace-story-card h3 {
        font-size: 22px !important;
    }

    .pace-story-grid .pace-story-card p {
        font-size: 14px !important;
    }

    .pace-story-quote {
        overflow-wrap: normal !important;
        word-break: normal !important;
    }
}


/* Story opening is an editorial sequence, not two squeezed columns. */
.st-key-story_intro,
.st-key-story_photo,
.st-key-story_intro_continued {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
}

.st-key-story_intro h2 {
    font-size: clamp(2rem, 4.4vw, 3.6rem) !important;
    line-height: 1.12 !important;
    letter-spacing: -0.045em !important;
    overflow-wrap: normal !important;
    word-break: normal !important;
    max-width: 850px;
    margin-top: 12px !important;
}

.st-key-story_intro p,
.st-key-story_intro_continued p {
    max-width: 780px;
    line-height: 1.75 !important;
    font-size: 16px !important;
}

.st-key-story_photo {
    max-width: 800px !important;
    margin: 18px 0 23px !important;
}

.st-key-story_photo img {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    height: auto !important;
    object-fit: contain !important;
    border-radius: 18px !important;
}

@media (max-width: 768px) {
    .st-key-story_intro h2 {
        font-size: clamp(1.9rem, 8.1vw, 2.6rem) !important;
        line-height: 1.13 !important;
        max-width: 100% !important;
    }

    .st-key-story_intro p,
    .st-key-story_intro_continued p {
        max-width: 100% !important;
        font-size: 15px !important;
        line-height: 1.7 !important;
    }

    .st-key-story_photo {
        width: 100% !important;
        max-width: 100% !important;
        margin: 16px 0 19px !important;
    }

    .st-key-story_photo img {
        border-radius: 14px !important;
    }
}

</style>
        """,
        unsafe_allow_html=True,
    )
