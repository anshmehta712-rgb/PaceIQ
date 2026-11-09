
import hashlib
from pathlib import Path

import pandas as pd
import streamlit as st

from tracker import process_video, video_information
from feedback import analyse_movement
from phase_tools import get_preview_frame, get_phase_measurements
from ai_feedback import generate_ai_feedback

from design import (
    apply_design,
    brand,
    banner,
    section_title,
    tile,
    empty_state,
    story_card,
    pose_visual,
    footer,
)


# ============================================================
# PACEIQ — APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PaceIQ | Fast Bowling Intelligence",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_design()

PHASE_NAMES = {
    "BFC": "Back-Foot Contact",
    "FFC": "Front-Foot Contact",
    "Release": "Ball Release",
}

PAGES = [
    "Home",
    "Motion Lab",
    "My Story",
]

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def navigate(page):
    st.session_state["current_page"] = page
    st.rerun()


def switch_to_analysis():
    navigate("Motion Lab")


@st.cache_data(show_spinner=False, max_entries=64)
def preview_frame_cached(video_bytes, frame_index, fps):
    return get_preview_frame(
        video_bytes,
        frame_index / fps,
    )


def display_angle(value):
    if value is None:
        return "Unavailable"

    try:
        value = float(value)

        if pd.isna(value):
            return "Unavailable"

        return f"{value:.1f}°"

    except (TypeError, ValueError):
        return "Unavailable"


def measure_video(video_bytes, start_time, front_leg, bowling_arm):
    records = analyse_movement(
        video_bytes,
        start_time,
        front_leg.lower(),
        bowling_arm.lower(),
    )

    if not records:
        raise ValueError(
            "No movement measurements were detected."
        )

    return records


def reset_video_state(video_id):
    if st.session_state.get("video_id") == video_id:
        return

    keys = [
        "tracked_video",
        "tracking_stats",
        "analysis_settings",
        "movement_records",
        "measurement_settings",
        "ai_result",
        "ai_input_settings",
        "saved_phases",
    ]

    for key in keys:
        st.session_state.pop(key, None)

    st.session_state["video_id"] = video_id


def phase_signature(saved_phases):
    return tuple(
        sorted(
            (
                name,
                round(item["time"], 3),
            )
            for name, item in saved_phases.items()
        )
    )


# ============================================================
# GLOBAL NAVIGATION
# ============================================================

brand()

navigation = st.columns([1, 1, 1, 3], gap="small")

for index, page in enumerate(PAGES):
    with navigation[index]:
        if st.button(
            page,
            key=f"nav_{index}",
            type=(
                "primary"
                if st.session_state["current_page"] == page
                else "secondary"
            ),
            width="stretch",
        ):
            navigate(page)

st.divider()


# ============================================================
# PAGE 1 — HOME DASHBOARD
# ============================================================

def home():

    left, right = st.columns(
        [1.12, 1],
        gap="large",
        vertical_alignment="center",
    )

    with left:

        st.markdown(
            '<div class="pace-hero-wrap">'
            '<div class="pace-eyebrow">'
            'THE NEXT GENERATION OF BOWLING ANALYSIS'
            '</div>'
            '<div class="pace-title">'
            'Every Action.<br>'
            '<span class="accent">Every Angle.</span><br>'
            '<span class="outline">Every Detail.</span>'
            '</div>'
            '<div class="pace-lede">'
            'Understand your fast-bowling action through '
            'computer vision, biomechanical measurements '
            'and local AI-assisted coaching.'
            '</div>'
            '<div class="pace-micro-row">'
            '<span><strong>01</strong> MOTION TRACKING</span>'
            '<span><strong>02</strong> PHASE ANALYSIS</span>'
            '<span><strong>03</strong> AI COACHING</span>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Launch Motion Lab ↗",
            type="primary",
            key="home_launch",
            width="stretch",
        ):
            switch_to_analysis()

        st.caption(
            "Analyse your action using a standard MP4 video."
        )

    with right:

        pose_visual()

    st.markdown(
        '<div class="pace-strip">'
        '<span><b>PACEIQ</b> / BUILT FOR FAST BOWLERS</span>'
        '<span>COMPUTER VISION + LOCAL AI</span>'
        '<span>IB MYP PERSONAL PROJECT</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    section_title(
        "THE PLATFORM",
        "One action. Deeper understanding.",
        "Explore your bowling movement through three "
        "connected analysis tools.",
    )

    feature_columns = st.columns(3, gap="medium")

    with feature_columns[0]:
        tile(
            "01 / TRACK",
            "Motion Tracking",
            "Upload a bowling video and visualise "
            "estimated body landmarks and joint movement.",
        )

    with feature_columns[1]:
        tile(
            "02 / MEASURE",
            "Biomechanics Lab",
            "Examine estimated knee, elbow and trunk "
            "angles across important delivery phases.",
        )

    with feature_columns[2]:
        tile(
            "03 / UNDERSTAND",
            "AI Bowling Coach",
            "Receive structured observations and "
            "suggested training questions using local AI.",
        )

    st.markdown(
        '<div class="pace-band">'
        '<h3>Train with purpose.</h3>'
        '<p>'
        'PaceIQ helps fast bowlers observe their action '
        'and make better-informed decisions about training.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    section_title(
        "THE PROCESS",
        "From footage to feedback.",
        "A simple workflow designed around the "
        "fast-bowling delivery.",
    )

    process_columns = st.columns(3, gap="medium")

    with process_columns[0]:
        st.markdown("### 01 — Upload")
        st.write(
            "Record your bowling action and upload "
            "the video into PaceIQ."
        )

    with process_columns[1]:
        st.markdown("### 02 — Analyse")
        st.write(
            "Identify bowling phases and measure "
            "estimated joint angles."
        )

    with process_columns[2]:
        st.markdown("### 03 — Reflect")
        st.write(
            "Review the measurements and receive "
            "AI-assisted coaching observations."
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Start Your Analysis ↗",
            type="primary",
            key="home_start",
            width="stretch",
        ):
            switch_to_analysis()

    with col2:
        if st.button(
            "Discover My Story",
            key="home_story",
            width="stretch",
        ):
            navigate("My Story")


# ============================================================
# PAGE 2 — MOTION LAB
# ============================================================

def motion_lab():

    banner(
        "PACEIQ / ANALYSIS WORKSPACE",
        "Motion Lab.",
        "Track your bowling action, identify delivery "
        "phases and examine estimated biomechanical data.",
    )

    video = st.file_uploader(
        "Upload a bowling video (MP4)",
        type=["mp4"],
        key="bowling_upload",
    )

    if video is None:

        empty_state(
            "Your analysis starts here.",
            "Upload an MP4 recording of your bowling "
            "action to begin motion tracking.",
        )

        return

    video_bytes = video.getvalue()

    video_id = hashlib.sha256(
        video_bytes
    ).hexdigest()

    reset_video_state(video_id)

    try:
        frames, fps, duration = video_information(
            video_bytes
        )

        if fps <= 0 or frames <= 0:
            raise ValueError(
                "Invalid video frame rate or frame count."
            )

    except Exception as error:
        st.error(f"Could not read video: {error}")
        return

    st.success("Video loaded successfully.")

    metric_columns = st.columns(3)

    metric_columns[0].metric(
        "Video Frames",
        frames,
    )

    metric_columns[1].metric(
        "Frame Rate",
        f"{fps:.1f} FPS",
    )

    metric_columns[2].metric(
        "Duration",
        f"{duration:.2f} s",
    )

    st.video(video_bytes)

    phase_tab, tracking_tab, coaching_tab = st.tabs(
        [
            "01 / Bowling Phases",
            "02 / Tracking & Measurements",
            "03 / AI Coach",
        ]
    )

    saved_phases = st.session_state.setdefault(
        "saved_phases",
        {},
    )

    # ========================================================
    # TAB 1 — BOWLING PHASE SELECTION
    # ========================================================

    with phase_tab:

        section_title(
            "DELIVERY PHASES",
            "Find the important moments.",
            "Move frame by frame and manually save "
            "back-foot contact, front-foot contact "
            "and ball release.",
        )

        frame_index = st.slider(
            "Select video frame",
            min_value=0,
            max_value=frames - 1,
            value=min(int(37 * fps), frames - 1),
            step=1,
            key=f"phase_frame_{video_id}",
        )

        try:

            preview, actual_time = preview_frame_cached(
                video_bytes,
                frame_index,
                fps,
            )

            preview_left, preview_right = st.columns(
                [1.45, 1],
                gap="large",
            )

            with preview_left:

                st.image(
                    preview,
                    caption=(
                        f"Frame {frame_index + 1} / {frames}"
                        f" | {actual_time:.3f} seconds"
                    ),
                    width="stretch",
                )

            with preview_right:

                st.markdown("### Select the phase")

                selected_phase = st.radio(
                    "Bowling phase",
                    list(PHASE_NAMES.keys()),
                    format_func=lambda name: (
                        f"{name} — {PHASE_NAMES[name]}"
                    ),
                    key=f"phase_choice_{video_id}",
                )

                st.write(
                    "Check the frame carefully before "
                    "saving its timestamp."
                )

                if st.button(
                    "Save Selected Phase",
                    type="primary",
                    key="save_phase",
                    width="stretch",
                ):

                    saved_phases[selected_phase] = {
                        "time": actual_time,
                        "frame": preview.copy(),
                    }

                    st.success(
                        f"{PHASE_NAMES[selected_phase]} saved "
                        f"at {actual_time:.3f}s."
                    )

        except Exception as error:
            st.error(f"Frame preview failed: {error}")

        st.divider()

        section_title(
            "YOUR SELECTIONS",
            "Saved delivery phases.",
            "These manually selected frames are used "
            "for phase-specific measurements.",
        )

        columns = st.columns(3, gap="medium")

        for index, phase in enumerate(PHASE_NAMES):

            with columns[index]:

                st.markdown(
                    f"**{PHASE_NAMES[phase]}**"
                )

                if phase not in saved_phases:
                    st.info("Not selected yet.")
                    continue

                item = saved_phases[phase]

                st.image(
                    item["frame"],
                    width="stretch",
                )

                st.caption(
                    f"Timestamp: {item['time']:.3f}s"
                )

                if st.button(
                    f"Remove {phase}",
                    key=f"remove_{phase}",
                    width="stretch",
                ):
                    del saved_phases[phase]
                    st.rerun()

    # ========================================================
    # ANALYSIS SETTINGS
    # ========================================================

    with tracking_tab:

        section_title(
            "TRACKING ENGINE",
            "Analyse your bowling action.",
            "Select the five-second section containing "
            "your delivery.",
        )

        max_start = max(
            0.0,
            round(duration - 0.1, 1),
        )

        start_time = st.slider(
            "Start of bowling action (seconds)",
            min_value=0.0,
            max_value=max_start,
            value=0.0,
            step=0.1,
            key=f"start_time_{video_id}",
        )

        st.caption(
            f"Selected section: {start_time:.1f}s "
            f"to {min(duration, start_time + 5):.1f}s"
        )

        settings_columns = st.columns(2)

        front_leg = settings_columns[0].selectbox(
            "Front leg",
            ["Right", "Left"],
            key=f"front_leg_{video_id}",
        )

        bowling_arm = settings_columns[1].selectbox(
            "Bowling arm",
            ["Right", "Left"],
            index=1,
            key=f"bowling_arm_{video_id}",
        )

        settings = (
            video_id,
            round(start_time, 1),
            front_leg,
            bowling_arm,
        )

        if st.button(
            "Analyse Bowling Action",
            type="primary",
            key="analyse_action",
            width="stretch",
        ):

            for key in [
                "tracked_video",
                "tracking_stats",
                "analysis_settings",
                "movement_records",
                "measurement_settings",
                "ai_result",
                "ai_input_settings",
            ]:
                st.session_state.pop(key, None)

            try:

                with st.spinner(
                    "Processing bowling footage..."
                ):

                    output, processed, detected = process_video(
                        video_bytes,
                        start_time,
                        front_leg=front_leg.lower(),
                        bowling_arm=bowling_arm.lower(),
                    )

                st.session_state["tracked_video"] = output

                st.session_state["tracking_stats"] = (
                    processed,
                    detected,
                )

                st.session_state["analysis_settings"] = settings

                st.success("Video tracking complete.")

            except Exception as error:
                st.exception(error)

        saved_video = st.session_state.get(
            "tracked_video"
        )

        analysis_current = (
            saved_video is not None
            and st.session_state.get("analysis_settings")
            == settings
        )

        if saved_video is not None and not analysis_current:
            st.warning(
                "Your settings have changed. "
                "Run the analysis again."
            )

        if analysis_current:

            st.divider()

            section_title(
                "POSE TRACKING",
                "Original vs tracked footage.",
                "Review the estimated skeletal landmarks "
                "and angle overlays.",
            )

            st.video(
                saved_video,
                format="video/mp4",
            )

            processed, detected = (
                st.session_state["tracking_stats"]
            )

            metric_left, metric_right = st.columns(2)

            metric_left.metric(
                "Frames Analysed",
                processed,
            )

            metric_right.metric(
                "Frames With Pose Detection",
                detected,
            )

            st.download_button(
                "Download Tracked Video",
                data=saved_video,
                file_name="PaceIQ_Tracked.mp4",
                mime="video/mp4",
            )

            st.divider()

            section_title(
                "BIOMECHANICS",
                "Joint angle measurements.",
                "Measure estimated front knee, "
                "bowling elbow and trunk angles.",
            )

            if st.button(
                "Measure Joint Angles",
                type="primary",
                key="measure_angles",
            ):

                try:

                    with st.spinner(
                        "Measuring joint movement..."
                    ):

                        records = measure_video(
                            video_bytes,
                            start_time,
                            front_leg,
                            bowling_arm,
                        )

                    st.session_state[
                        "movement_records"
                    ] = records

                    st.session_state[
                        "measurement_settings"
                    ] = settings

                    st.success(
                        "Joint measurements complete."
                    )

                except Exception as error:
                    st.error(
                        f"Measurement failed: {error}"
                    )

            records = st.session_state.get(
                "movement_records"
            )

            if (
                st.session_state.get(
                    "measurement_settings"
                ) != settings
            ):
                records = None

            if records:

                df = pd.DataFrame(records)

                st.markdown("### Angle trends")

                st.line_chart(
                    df.set_index("Time (s)")[
                        ["Knee", "Elbow", "Trunk"]
                    ]
                )

                st.download_button(
                    "Download Angle Data (CSV)",
                    data=df.to_csv(index=False),
                    file_name="PaceIQ_Angles.csv",
                    mime="text/csv",
                )

                st.divider()

                section_title(
                    "PHASE COMPARISON",
                    "Three moments. Three measurements.",
                    "Measurements are matched to the "
                    "nearest available sample.",
                )

                phase_rows = []
                phase_columns = st.columns(3)

                for index, phase in enumerate(PHASE_NAMES):

                    with phase_columns[index]:

                        st.markdown(
                            f"### {PHASE_NAMES[phase]}"
                        )

                        if phase not in saved_phases:
                            st.info("Phase not selected.")
                            continue

                        item = saved_phases[phase]

                        st.image(
                            item["frame"],
                            width="stretch",
                        )

                        selected_time = item["time"]

                        measurement = get_phase_measurements(
                            records,
                            selected_time,
                        )

                        st.caption(
                            f"Selected: {selected_time:.3f}s"
                        )

                        if measurement is None:

                            st.warning(
                                "No nearby measurement available."
                            )

                            phase_rows.append({
                                "Phase": PHASE_NAMES[phase],
                                "Selected Time": selected_time,
                                "Measured Time": None,
                                "Knee": None,
                                "Elbow": None,
                                "Trunk": None,
                            })

                            continue

                        st.caption(
                            "Measured: "
                            f"{measurement['Time']:.3f}s"
                        )

                        st.metric(
                            "Front Knee",
                            display_angle(
                                measurement["Knee"]
                            ),
                        )

                        st.metric(
                            "Bowling Elbow",
                            display_angle(
                                measurement["Elbow"]
                            ),
                        )

                        st.metric(
                            "Trunk",
                            display_angle(
                                measurement["Trunk"]
                            ),
                        )

                        phase_rows.append({
                            "Phase": PHASE_NAMES[phase],
                            "Selected Time": selected_time,
                            "Measured Time": measurement["Time"],
                            "Knee": measurement["Knee"],
                            "Elbow": measurement["Elbow"],
                            "Trunk": measurement["Trunk"],
                        })

                if phase_rows:

                    phase_df = pd.DataFrame(
                        phase_rows
                    )

                    st.dataframe(
                        phase_df,
                        width="stretch",
                        hide_index=True,
                    )

                    st.download_button(
                        "Download Phase Comparison",
                        data=phase_df.to_csv(index=False),
                        file_name="PaceIQ_Phases.csv",
                        mime="text/csv",
                    )

                st.caption(
                    "Angles are estimated from 2D video. "
                    "Measurements are matched within "
                    "0.15 seconds of the selected phase."
                )

    # ========================================================
    # TAB 3 — LOCAL AI COACH
    # ========================================================

    with coaching_tab:

        section_title(
            "PACEIQ INTELLIGENCE",
            "Your AI bowling coach.",
            "Get evidence-based observations from "
            "the estimated movement data.",
        )

        current_settings = (
            video_id,
            round(
                st.session_state.get(
                    f"start_time_{video_id}",
                    0.0,
                ),
                1,
            ),
            st.session_state.get(
                f"front_leg_{video_id}",
                "Right",
            ),
            st.session_state.get(
                f"bowling_arm_{video_id}",
                "Left",
            ),
        )

        tracked_current = (
            st.session_state.get("tracked_video")
            is not None
            and st.session_state.get("analysis_settings")
            == current_settings
        )

        if not tracked_current:

            empty_state(
                "Analyse your action first.",
                "Go to Tracking & Measurements and "
                "complete video tracking before "
                "generating AI feedback.",
            )

        else:

            start_time = current_settings[1]
            front_leg = current_settings[2]
            bowling_arm = current_settings[3]

            bowler_notes = st.text_area(
                "What are you working on? (optional)",
                placeholder=(
                    "Example: I want to understand "
                    "my front-leg position at release."
                ),
                key="bowler_notes",
            )

            speed = st.number_input(
                "Measured bowling speed (km/h) — optional",
                min_value=0.0,
                max_value=180.0,
                value=0.0,
                step=1.0,
                key="bowling_speed",
            )

            input_settings = (
                current_settings,
                bowler_notes,
                speed,
                phase_signature(saved_phases),
            )

            if st.button(
                "Generate AI Coaching Feedback",
                type="primary",
                key="generate_coaching",
                width="stretch",
            ):

                st.session_state.pop(
                    "ai_result",
                    None,
                )

                try:

                    records = st.session_state.get(
                        "movement_records"
                    )

                    if (
                        st.session_state.get(
                            "measurement_settings"
                        ) != current_settings
                    ):
                        records = None

                    if not records:

                        with st.spinner(
                            "Measuring bowling movement..."
                        ):

                            records = measure_video(
                                video_bytes,
                                start_time,
                                front_leg,
                                bowling_arm,
                            )

                        st.session_state[
                            "movement_records"
                        ] = records

                        st.session_state[
                            "measurement_settings"
                        ] = current_settings

                    with st.spinner(
                        "PaceIQ AI is preparing your report..."
                    ):

                        feedback = generate_ai_feedback(
                            records=records,
                            front_leg=front_leg,
                            bowling_arm=bowling_arm,
                            bowler_notes=bowler_notes,
                            bowling_speed=(
                                speed if speed > 0 else None
                            ),
                            phase_times={
                                name: item["time"]
                                for name, item
                                in saved_phases.items()
                            },
                        )

                    st.session_state["ai_result"] = feedback

                    st.session_state[
                        "ai_input_settings"
                    ] = input_settings

                    st.success(
                        "AI coaching report generated."
                    )

                except Exception as error:
                    st.error(
                        f"AI coaching failed: {error}"
                    )

            feedback = st.session_state.get(
                "ai_result"
            )

            if feedback:

                if (
                    st.session_state.get(
                        "ai_input_settings"
                    ) != input_settings
                ):

                    st.info(
                        "Your inputs changed. Generate "
                        "a new report to update the feedback."
                    )

                else:

                    st.divider()

                    section_title(
                        "YOUR REPORT",
                        "Personalized coaching observations.",
                        "Based on the measured joint angles "
                        "and your selected bowling phases.",
                    )

                    st.markdown(feedback)

            st.caption(
                "AI feedback is based on estimated 2D "
                "pose measurements, not direct video "
                "understanding. It cannot establish "
                "bowling-action legality, injury risk "
                "or the cause of low pace."
            )


# ============================================================
# PAGE 3 — MY STORY
# ============================================================

def story():

    banner(
        "BEHIND PACEIQ / THE PERSONAL PROJECT",
        "The Bowler Behind the Code.",
        "How my journey as a fast bowler inspired "
        "me to build PaceIQ.",
    )

    left, right = st.columns(
        [1.05, 1],
        gap="large",
        vertical_alignment="center",
    )

    with left:

        st.markdown(
            '<div class="pace-eyebrow">'
            'FROM THE CREASE TO THE CODE'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            "## Before PaceIQ, there was just "
            "me and a cricket ball."
        )

        st.write(
            "Fast bowling has always fascinated me. "
            "There is something special about the "
            "rhythm of the run-up, the jump into "
            "the delivery stride, and the moment "
            "the ball leaves your hand."
        )

        st.write(
            "As I developed as a fast bowler, "
            "I wanted to understand more than "
            "whether a delivery was fast or accurate. "
            "I wanted to know what my body was "
            "actually doing."
        )

        st.write(
            "But I did not always have consistent "
            "access to a coach who could analyse "
            "every part of my action. I could "
            "record myself bowling and replay "
            "the footage, yet I often struggled "
            "to understand exactly what I was seeing."
        )

        st.markdown(
            '<div class="pace-story-quote">'
            '“I could watch my bowling action. '
            'I wanted to understand it.”'
            '</div>',
            unsafe_allow_html=True,
        )

    with right:

        photo_path = (
            Path(__file__).resolve().parent
            / "story_photo.png"
        )

        if photo_path.is_file():

            st.image(
                str(photo_path),
                width="stretch",
            )

            st.caption(
                "A moment from my own bowling journey. "
                "Original photograph, without edits."
            )

        else:

            st.info(
                "Save your original bowling photo as "
                "story_photo.png inside the PaceIQ folder."
            )

    st.divider()

    # --------------------------------------------------------
    # CHAPTER 1 — THE PROBLEM
    # --------------------------------------------------------

    section_title(
        "CHAPTER 01 / THE CHALLENGE",
        "The problem I experienced.",
        "My motivation came from a real challenge "
        "in my own training.",
    )

    st.write(
        "I began noticing how difficult it was "
        "to evaluate my bowling action without "
        "detailed technical feedback."
    )

    st.write(
        "Was my front knee bending too much? "
        "What happened to my bowling arm at release? "
        "How did my body position change between "
        "back-foot contact and front-foot contact?"
    )

    st.write(
        "These were questions I could not always "
        "answer by watching an ordinary recording. "
        "I realised that I needed a way to turn "
        "what I could see into something I could "
        "measure and investigate."
    )

    # --------------------------------------------------------
    # CHAPTER 2 — THE IDEA
    # --------------------------------------------------------

    section_title(
        "CHAPTER 02 / THE IDEA",
        "Turning frustration into innovation.",
        "The starting point of PaceIQ.",
    )

    st.write(
        "When I began planning my IB MYP Personal "
        "Project, I wanted to create something "
        "connected to a challenge I had experienced "
        "personally."
    )

    st.write(
        "I decided to combine two of my interests: "
        "cricket and technology. I imagined a "
        "platform where a fast bowler could upload "
        "a video, identify important delivery "
        "moments, examine estimated body angles "
        "and receive useful observations."
    )

    st.markdown(
        "**That idea became PaceIQ — "
        "Fast Bowling Intelligence.**"
    )

    # --------------------------------------------------------
    # THE JOURNEY
    # --------------------------------------------------------

    section_title(
        "THE JOURNEY",
        "From bowler to builder.",
        "Three stages that shaped the project.",
    )

    chapter_columns = st.columns(
        3,
        gap="medium",
    )

    with chapter_columns[0]:

        story_card(
            "01",
            "The Frustration",
            "I wanted to improve my technique, "
            "but I did not always have access "
            "to detailed coaching feedback.",
        )

    with chapter_columns[1]:

        story_card(
            "02",
            "The Experiment",
            "I explored computer vision and "
            "pose estimation to understand "
            "whether video could reveal useful "
            "movement measurements.",
        )

    with chapter_columns[2]:

        story_card(
            "03",
            "The Creation",
            "I developed PaceIQ to combine "
            "video tracking, bowling-phase "
            "analysis and local AI coaching.",
        )

    st.divider()

    # --------------------------------------------------------
    # CHAPTER 3 — DEVELOPMENT
    # --------------------------------------------------------

    section_title(
        "CHAPTER 03 / DEVELOPMENT",
        "Building PaceIQ.",
        "Learning programming, biomechanics "
        "and problem-solving along the way.",
    )

    st.write(
        "Developing PaceIQ pushed me beyond "
        "simply learning how to write code. "
        "I had to understand how different "
        "technologies could work together "
        "to solve a practical problem."
    )

    st.markdown(
        """
**Python and Streamlit** — Building the
application and interactive interface.

**OpenCV** — Reading and processing
bowling footage.

**MediaPipe** — Detecting body landmarks
and estimating joint positions.

**Biomechanical measurements** — Calculating
approximate knee, elbow and trunk angles.

**Local AI** — Producing structured coaching
observations from movement measurements.
"""
    )

    st.write(
        "The development process involved "
        "technical errors, debugging, "
        "testing different approaches and "
        "learning from unsuccessful attempts."
    )

    st.write(
        "One important lesson was that "
        "technology has limitations. "
        "Camera angles, landmark visibility "
        "and video quality can influence "
        "the accuracy of measurements."
    )

    st.write(
        "PaceIQ is therefore designed to "
        "support self-analysis, not replace "
        "an experienced cricket coach."
    )

    # --------------------------------------------------------
    # CHAPTER 4 — PURPOSE
    # --------------------------------------------------------

    section_title(
        "CHAPTER 04 / THE PURPOSE",
        "More than an application.",
        "Why building PaceIQ matters to me.",
    )

    st.write(
        "PaceIQ represents the connection "
        "between my experience as an athlete "
        "and my interest in technology."
    )

    st.write(
        "What began as a personal question "
        "became a project that could help "
        "other young fast bowlers who face "
        "similar challenges."
    )

    st.markdown(
        '<div class="pace-band">'
        '<h3>Every young fast bowler deserves '
        'a place to start.</h3>'
        '<p>'
        'My vision is to make basic bowling '
        'movement analysis more accessible, '
        'helping young cricketers observe '
        'their technique, ask better questions '
        'and approach training with purpose.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "### From the crease to the code."
    )

    st.write(
        "I started this journey as a fast bowler "
        "trying to understand my own action. "
        "Through PaceIQ, I learned to approach "
        "problems not only as an athlete, "
        "but also as a developer and innovator."
    )

    st.markdown(
        "**PaceIQ is not just the product "
        "I built. It is a reflection of "
        "why I built it.**"
    )

    if st.button(
        "Explore PaceIQ Motion Lab ↗",
        type="primary",
        key="story_launch",
        width="stretch",
    ):
        switch_to_analysis()


# ============================================================
# PAGE ROUTER
# ============================================================

current_page = st.session_state["current_page"]

if current_page == "Home":
    home()

elif current_page == "Motion Lab":
    motion_lab()

elif current_page == "My Story":
    story()

footer()
