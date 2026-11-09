
"""PaceIQ visual design — premium dark sports interface."""

import base64
from pathlib import Path
from html import escape

import streamlit as st


def apply_design():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #071018;
    --surface: #101E29;
    --surface2: #142531;
    --line: rgba(178, 219, 219, .16);
    --text: #F4F8F7;
    --muted: #92A5AE;
    --mint: #8AF7B2;
    --lime: #D4FC79;
}

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', 'Inter', sans-serif;
}

.stApp {
    color: var(--text);
    background:
      radial-gradient(
        ellipse at 80% 4%,
        rgba(33,119,108,.21) 0,
        transparent 34%
      ),
      radial-gradient(
        ellipse at 3% 55%,
        rgba(29,75,91,.19) 0,
        transparent 40%
      ),
      linear-gradient(
        135deg,
        #071018 0%,
        #08141d 55%,
        #071018 100%
      );
}

[data-testid="stHeader"] {
    background: rgba(7,16,24,.84) !important;
    backdrop-filter: blur(18px);
    border-bottom: 1px solid rgba(178,219,219,.09);
}

[data-testid="stToolbar"] {
    opacity: .55;
}

.block-container {
    max-width: 1320px;
    padding-top: 1.7rem;
    padding-bottom: 3.5rem;
}

[data-testid="stSidebar"] {
    background: #0b1822;
}

.stApp p,
.stApp label {
    color: #D5E0DF;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -.035em !important;
    color: var(--text) !important;
}

h2 {
    font-weight: 700 !important;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

hr {
    border-color: rgba(178,219,219,.13) !important;
}

/* ==========================================
   NAVIGATION
========================================== */

[data-testid="stNavigation"] {
    font-weight: 700;
}

[data-testid="stNavigation"] a,
[data-testid="stNavigation"] button {
    border-radius: 12px !important;
}

/* ==========================================
   BUTTONS — HIGH CONTRAST
========================================== */

/* Secondary buttons */

div.stButton > button,
div.stDownloadButton > button {
    background: rgba(18,36,48,.95);
    color: #EEF9F6 !important;
    border: 1px solid rgba(166,226,216,.25);
    border-radius: 12px;
    font-weight: 700;
    min-height: 45px;

    transition:
        transform .18s ease,
        border-color .18s ease,
        background .18s ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    border-color: #8AF7B2;
    color: #8AF7B2 !important;
    transform: translateY(-1px);
}

/* PRIMARY BUTTON FIX */
/* Dark emerald background + pure white text */

div.stButton > button[kind="primary"],
div.stButton > button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(
        120deg,
        #0E6E54 0%,
        #075A48 100%
    ) !important;

    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;

    border: 1px solid #77D9AF !important;
    border-radius: 14px !important;

    min-height: 54px;
    font-weight: 800 !important;

    box-shadow:
        0 8px 28px rgba(0,160,110,.18);

    transition:
        transform .2s ease,
        box-shadow .2s ease,
        background .2s ease;
}

/* Make Streamlit's nested text white too */

div.stButton > button[kind="primary"] *,
div.stButton > button[data-testid="stBaseButton-primary"] *,
button[data-testid="stBaseButton-primary"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
    text-shadow: none !important;
}

/* Hover */

div.stButton > button[kind="primary"]:hover,
div.stButton > button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(
        120deg,
        #15795D,
        #0A624B
    ) !important;

    border-color: #A7FFD2 !important;
    color: #FFFFFF !important;

    transform: translateY(-2px);

    box-shadow:
        0 12px 35px rgba(0,170,110,.25);
}

/* Focus accessibility */

div.stButton > button[kind="primary"]:focus-visible,
button[data-testid="stBaseButton-primary"]:focus-visible {
    outline: 3px solid #C6FFDF !important;
    outline-offset: 3px !important;
}

/* ==========================================
   STREAMLIT COMPONENTS
========================================== */

[data-testid="stFileUploader"] section {
    background: rgba(15,31,41,.92);
    border: 1px dashed rgba(138,247,178,.38);
    border-radius: 16px;
}

[data-testid="stFileUploader"] button {
    color: var(--text);
}

[data-testid="stMetric"] {
    background: linear-gradient(
        160deg,
        rgba(22,44,55,.95),
        rgba(12,28,38,.95)
    );

    border: 1px solid var(--line);
    padding: 18px 20px;
    border-radius: 17px;
}

[data-testid="stMetricValue"] {
    color: var(--lime);
    font-family: 'Space Grotesk', sans-serif;
}

[data-testid="stMetricLabel"] {
    color: #AFBFBE;
}

[data-testid="stAlert"] {
    border-radius: 14px;
}

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

[data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(12,27,37,.85);
    padding: 8px;
    border: 1px solid var(--line);
    border-radius: 16px;
}

[data-baseweb="tab"] {
    border-radius: 10px !important;
    color: #AFC1C1 !important;
    font-weight: 700 !important;
}

[aria-selected="true"][data-baseweb="tab"] {
    color: #B9FFCB !important;
    background: rgba(100,233,150,.11) !important;
}

[data-testid="stImage"] img,
[data-testid="stVideo"] video {
    border-radius: 15px;
}

/* ==========================================
   BRAND
========================================== */

.pace-brand {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 6px 0 21px;
}

.pace-brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 25px;
    letter-spacing: -.065em;
    color: #F7FFFB;
}

.pace-brand-name span {
    color: var(--lime);
}

.pace-brand-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    width: 38px;
    height: 38px;
    margin-right: 12px;

    background: linear-gradient(
        135deg,
        var(--mint),
        var(--lime)
    );

    color: #061811 !important;
    font-weight: 800;
    font-size: 21px;
    border-radius: 12px;

    transform: skewX(-8deg);
}

.pace-brand-right {
    color: #91B2AF;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .17em;
    text-transform: uppercase;
}

/* ==========================================
   HERO SECTION
========================================== */

.pace-hero-wrap {
    padding: 42px 0 32px;
}

.pace-eyebrow {
    display: inline-flex;
    gap: 10px;
    align-items: center;

    color: var(--mint);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .23em;
    text-transform: uppercase;
}

.pace-eyebrow:before {
    content: '';
    width: 27px;
    height: 2px;
    display: inline-block;
    background: var(--mint);
    border-radius: 2px;
}

.pace-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    letter-spacing: -.075em;

    font-size: clamp(51px, 5.6vw, 91px);
    line-height: .99;

    color: #F7FBFA;
    margin: 21px 0 23px;
}

.pace-title .outline {
    color: transparent;
    -webkit-text-stroke:
        1px rgba(206,255,222,.67);
}

.pace-title .accent {
    color: var(--lime);
}

.pace-lede {
    max-width: 570px;
    color: #A8BAC1;

    font-size: 17px;
    line-height: 1.72;
    margin: 0 0 27px;
}

.pace-micro-row {
    display: flex;
    flex-wrap: wrap;

    gap: 16px 22px;
    margin: 28px 0 8px;
}

.pace-micro-row span {
    color: #A8BBC0;
    font-size: 12px;
    font-weight: 700;
}

.pace-micro-row strong {
    color: #98F4B6;
    margin-right: 7px;
}

/* ==========================================
   MOTION VISUAL
========================================== */

.pace-viz {
    position: relative;

    background:
        radial-gradient(
            circle at 53% 44%,
            rgba(42,144,114,.22),
            transparent 47%
        ),
        linear-gradient(
            148deg,
            #172934,
            #0B1B25 76%
        );

    border: 1px solid rgba(150,240,192,.18);

    box-shadow:
        0 28px 90px rgba(0,0,0,.18),
        inset 0 0 60px rgba(25,114,101,.05);

    border-radius: 28px;
    overflow: hidden;
    min-height: 470px;
}

.pace-viz::before {
    content: '';
    position: absolute;
    inset: 0;

    background-image:
        linear-gradient(
            rgba(139,224,200,.055) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(139,224,200,.055) 1px,
            transparent 1px
        );

    background-size: 30px 30px;
    pointer-events: none;
}

.pace-viz-head {
    position: absolute;
    top: 24px;
    left: 26px;
    right: 26px;

    display: flex;
    justify-content: space-between;

    z-index: 2;
    color: #A7D1C5;

    letter-spacing: .14em;
    font-size: 10px;
    font-weight: 800;
}

.pace-viz-ping {
    display: inline-block;

    width: 8px;
    height: 8px;
    margin-right: 7px;

    border-radius: 50%;
    background: #88F3A9;

    box-shadow: 0 0 17px #88F3A9;
}

.pace-viz img {
    display: block;
    width: 100%;
    height: 435px;
    object-fit: contain;
    position: relative;
    z-index: 1;
}

.pace-viz-foot {
    position: absolute;
    bottom: 21px;
    left: 25px;
    right: 25px;

    display: flex;
    justify-content: space-between;

    z-index: 2;

    color: #A4C8C2;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .11em;
}

/* ==========================================
   FEATURE CARDS
========================================== */

.pace-section-top {
    padding: 26px 0 18px;
    display: flex;
    flex-wrap: wrap;
    align-items: end;
    justify-content: space-between;
    gap: 12px;
}

.pace-section-label {
    font-size: 11px;
    font-weight: 800;
    color: var(--mint);
    letter-spacing: .2em;
    text-transform: uppercase;
    margin-bottom: 9px;
}

.pace-section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(28px,3vw,41px);
    line-height: 1.12;
    letter-spacing: -.05em;
    font-weight: 700;
    color: #F2FAF7;
}

.pace-section-sub {
    color: #97ADB5;
    max-width: 400px;
    font-size: 14px;
    line-height: 1.6;
}

.pace-tile {
    min-height: 215px;
    height: 100%;
    padding: 27px;

    background: linear-gradient(
        155deg,
        rgba(22,46,56,.9),
        rgba(12,27,38,.96)
    );

    border: 1px solid var(--line);
    border-radius: 19px;
    overflow: hidden;
    position: relative;
}

.pace-tile:after {
    content: '';
    width: 135px;
    height: 135px;
    position: absolute;

    right: -70px;
    top: -75px;

    border-radius: 50%;
    border: 1px solid rgba(159,248,186,.16);

    box-shadow:
        0 0 0 25px rgba(159,248,186,.025);
}

.pace-tile-no {
    color: var(--mint);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .15em;
}

.pace-tile-title {
    color: #F1F8F6;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -.04em;
    margin: 29px 0 9px;
}

.pace-tile-body {
    color: #9FB1B8;
    font-size: 14px;
    line-height: 1.6;
    max-width: 280px;
}

.pace-strip {
    padding: 19px 22px;
    margin: 18px 0 5px;

    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 14px;

    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);

    color: #B4C8C7;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .08em;
}

.pace-strip b {
    color: var(--lime);
}

.pace-band {
    background: linear-gradient(
        112deg,
        #B1FBB1,
        #DAFE7D
    );

    color: #0D241D;
    padding: 28px 31px;
    border-radius: 19px;
    margin: 25px 0 5px;
}

.pace-band h3 {
    color: #0E261E !important;
    font-size: 30px;
    margin: 0 0 8px;
}

.pace-band p {
    color: #234739 !important;
    margin: 0;
}

/* ==========================================
   OTHER PAGES
========================================== */

.pace-banner {
    background: linear-gradient(
        110deg,
        rgba(24,54,59,.86),
        rgba(11,29,39,.9)
    );

    border: 1px solid var(--line);
    border-radius: 21px;

    padding: 28px 32px;
    margin: 12px 0 24px;
}

.pace-banner h1 {
    font-size: clamp(34px,4.1vw,55px);
    margin: 10px 0;
}

.pace-banner p {
    color: #A5BDC1;
    max-width: 800px;
}

.pace-empty {
    border: 1px dashed rgba(139,247,178,.35);
    border-radius: 20px;

    background: rgba(14,35,43,.56);
    text-align: center;

    padding: 58px 24px;
    margin: 15px 0;
}

.pace-empty .number {
    color: var(--mint);
    font-size: 46px;
    font-family: 'Space Grotesk';
    font-weight: 700;
}

.pace-empty h3 {
    margin: 7px 0 6px;
}

.pace-empty p {
    color: #9EB4BC;
    max-width: 570px;
    margin: 0 auto;
}

/* ==========================================
   MY STORY
========================================== */

.pace-story-quote {
    background: linear-gradient(
        120deg,
        rgba(21,62,57,.7),
        rgba(14,35,42,.85)
    );

    border-left: 3px solid var(--lime);
    border-radius: 0 20px 20px 0;

    padding: 29px 34px;

    font-family: 'Space Grotesk';
    color: #EAF8E7;

    font-size: clamp(22px,2.8vw,34px);
    letter-spacing: -.04em;
    line-height: 1.35;
}

.pace-story-card {
    border: 1px solid var(--line);
    border-radius: 19px;

    background: rgba(17,38,48,.73);
    padding: 27px;
    min-height: 220px;
}

.pace-story-card .num {
    color: var(--mint);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .16em;
}

.pace-story-card h3 {
    font-size: 25px;
    margin: 19px 0 8px;
}

.pace-story-card p {
    color: #9FB4B9;
    font-size: 14px;
    line-height: 1.7;
}

.pace-footer {
    border-top: 1px solid var(--line);
    margin-top: 49px;
    padding: 19px 0;

    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;

    color: #718E96;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .11em;
}

/* ==========================================
   YOUR ORIGINAL PHOTO
========================================== */

.pace-user-photo {
    position: relative;
    width: min(100%, 266px);

    margin: 12px auto 0;
    border-radius: 14px;
    overflow: hidden;

    border: 1px solid rgba(168,240,197,.25);

    box-shadow:
        0 8px 45px rgba(0,0,0,.34);
}

.pace-user-photo img {
    width: 100% !important;
    height: auto !important;
    display: block;

    object-fit: contain !important;
}

.pace-user-photo svg {
    position: absolute;

    width: 100%;
    height: 100%;

    left: 0;
    top: 0;

    pointer-events: none;
}

/* ==========================================
   RESPONSIVE DESIGN
========================================== */

@media (max-width: 800px) {

    .block-container {
        padding: 1rem 1.1rem 2rem;
    }

    .pace-title {
        font-size: clamp(49px,11vw,72px);
    }

    .pace-hero-wrap {
        padding: 20px 0 14px;
    }

    .pace-viz {
        min-height: 330px;
    }

    .pace-viz img {
        height: 320px;
    }

    .pace-brand-right {
        display: none;
    }

    .pace-tile {
        min-height: 165px;
    }

}

</style>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# BRAND
# ==================================================

def brand():
    st.markdown(
        '<div class="pace-brand">'
        '<div class="pace-brand-name">'
        '<span class="pace-brand-logo">P</span>'
        'PACE<span>IQ</span>'
        '</div>'
        '<div class="pace-brand-right">'
        'FAST BOWLING &nbsp; / &nbsp; REIMAGINED'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# BANNER
# ==================================================

def banner(kicker, title, description):
    st.markdown(
        '<div class="pace-banner">'
        f'<div class="pace-section-label">{escape(kicker)}</div>'
        f'<h1>{escape(title)}</h1>'
        f'<p>{escape(description)}</p>'
        '</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# SECTION TITLE
# ==================================================

def section_title(kicker, title, description=""):
    st.markdown(
        '<div class="pace-section-top">'
        '<div>'
        f'<div class="pace-section-label">{escape(kicker)}</div>'
        f'<div class="pace-section-title">{escape(title)}</div>'
        '</div>'
        f'<div class="pace-section-sub">'
        f'{escape(description)}'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# FEATURE TILE
# ==================================================

def tile(number, title, description):
    st.markdown(
        '<div class="pace-tile">'
        f'<div class="pace-tile-no">{escape(number)}</div>'
        f'<div class="pace-tile-title">{escape(title)}</div>'
        f'<div class="pace-tile-body">{escape(description)}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# EMPTY STATE
# ==================================================

def empty_state(title, description):
    st.markdown(
        '<div class="pace-empty">'
        '<div class="number">◎</div>'
        f'<h3>{escape(title)}</h3>'
        f'<p>{escape(description)}</p>'
        '</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# STORY CARD
# ==================================================

def story_card(number, title, description):
    st.markdown(
        '<div class="pace-story-card">'
        f'<div class="num">CHAPTER {escape(number)}</div>'
        f'<h3>{escape(title)}</h3>'
        f'<p>{escape(description)}</p>'
        '</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# ORIGINAL BOWLING PHOTO + POSE GUIDE
# ==================================================

def pose_visual():
    """
    Display the original bowling photograph unchanged.

    The SVG skeleton is an illustrative overlay.
    It is not a real tracking measurement.
    """

    photo = (
        Path(__file__).resolve().parent
        / "bowling_photo.png"
    )

    if not photo.exists():
        st.info(
            "Place bowling_photo.png next to design.py "
            "to display your original bowling photograph."
        )
        return

    raw = base64.b64encode(
        photo.read_bytes()
    ).decode("ascii")

    st.markdown(
        '<div class="pace-viz">'

        '<div class="pace-viz-head">'
        '<span>'
        '<i class="pace-viz-ping"></i>'
        'BOWLING ACTION / YOUR FOOTAGE'
        '</span>'
        '<span>01 / MOTION</span>'
        '</div>'

        '<div class="pace-user-photo">'

        f'<img src="data:image/png;base64,{raw}" '
        'alt="Original bowling photograph">'

        '<svg viewBox="0 0 332 554" '
        'preserveAspectRatio="none" '
        'aria-hidden="true">'

        '<g fill="none" '
        'stroke="#A8FFD4" '
        'stroke-width="3.2" '
        'stroke-linecap="round" '
        'stroke-linejoin="round" '
        'opacity=".83">'

        '<path d="M209 50 L203 105 L231 154 '
        'L219 257 L258 357 L282 449"/>'

        '<path d="M231 154 L169 122 L145 124"/>'

        '<path d="M219 257 L154 332 L89 441"/>'

        '</g>'

        '<g fill="#0A3027" '
        'stroke="#CEFFE3" '
        'stroke-width="2.8">'

        '<circle cx="209" cy="50" r="5"/>'
        '<circle cx="203" cy="105" r="5"/>'
        '<circle cx="231" cy="154" r="5"/>'
        '<circle cx="169" cy="122" r="5"/>'
        '<circle cx="145" cy="124" r="5"/>'
        '<circle cx="219" cy="257" r="5"/>'
        '<circle cx="258" cy="357" r="5"/>'
        '<circle cx="282" cy="449" r="5"/>'
        '<circle cx="154" cy="332" r="5"/>'
        '<circle cx="89" cy="441" r="5"/>'

        '</g>'
        '</svg>'

        '</div>'
'<div class="pace-viz-foot">'
'<span>PACEIQ / MOTION ANALYSIS</span>'
'<span>FAST BOWLING INTELLIGENCE</span>'
'</div>'

        '</div>',
        unsafe_allow_html=True,
    )


# ==================================================
# FOOTER
# ==================================================

def footer():
    st.markdown(
        '<div class="pace-footer">'
        '<span>'
        'PACEIQ &nbsp; / &nbsp; '
        'DESIGNED FOR THE BOWLER'
        '</span>'
        '<span>'
        'IB MYP PERSONAL PROJECT '
        '&nbsp; • &nbsp; LOCAL AI'
        '</span>'
        '</div>',
        unsafe_allow_html=True,
    )
