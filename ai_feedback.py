
import json
import math
import os
import re
import logging

from groq import Groq
from ollama import chat


MODEL = "qwen3:4b"
GROQ_MODEL = "llama-3.3-70b-versatile"
logger = logging.getLogger(__name__)

HEADINGS = {
    "overall_assessment": "Overall Assessment",
    "potential_strengths": "Potential Strengths",
    "areas_to_investigate": "Areas to Investigate",
    "recommended_drills": "Recommended Drills",
    "next_steps": "Next Steps",
}


def valid_number(value):
    try:
        number = float(value)
        if math.isfinite(number):
            return number
    except (TypeError, ValueError):
        pass

    return None


def format_list(content):
    """
    Put numbered points on separate lines
    for proper Streamlit Markdown formatting.
    """

    content = content.strip()

    # Convert inline numbered points into separate lines
    content = re.sub(
        r"\s+(?=\d+\.\s)",
        "\n",
        content
    )

    # Remove unnecessary leading whitespace
    lines = content.splitlines()
    formatted = []

    for line in lines:
        line = line.strip()

        if line:
            formatted.append(line)

    # Blank lines ensure Markdown renders numbered lists
    return "\n\n".join(formatted)


def generate_ai_feedback(
    records,
    front_leg,
    bowling_arm,
    bowler_notes="",
    bowling_speed=None,
    api_key=None,
    phase_times=None,
):
    """
    Generate cricket bowling feedback using hosted Groq AI,
    local Ollama, or a transparent rule-based fallback.
    """

    if not records:
        raise ValueError(
            "No analysed bowling measurements available."
        )

    # ------------------------------------------
    # 1. READ VIDEO MEASUREMENTS
    # ------------------------------------------

    measurements = []

    for row in records:
        time = valid_number(row.get("Time (s)"))

        if time is None:
            continue

        measurements.append({
            "time": time,
            "knee": valid_number(row.get("Knee")),
            "elbow": valid_number(row.get("Elbow")),
            "trunk": valid_number(row.get("Trunk")),
        })

    if not measurements:
        raise ValueError(
            "No valid timestamped measurements found."
        )

    measurements.sort(
        key=lambda row: row["time"]
    )

    # ------------------------------------------
    # 2. CALCULATE STATISTICS
    # ------------------------------------------

    statistics = {}

    for joint in ("knee", "elbow", "trunk"):
        values = [
            row[joint]
            for row in measurements
            if row[joint] is not None
        ]

        if values:
            statistics[joint] = {
                "minimum": round(min(values), 1),
                "maximum": round(max(values), 1),
                "average": round(
                    sum(values) / len(values), 1
                ),
                "samples": len(values),
            }
        else:
            statistics[joint] = {
                "samples": 0
            }

    # ------------------------------------------
    # 3. MATCH SELECTED BOWLING PHASES
    # ------------------------------------------

    phase_data = {}

    for name, selected_time in (
        phase_times or {}
    ).items():

        selected_time = valid_number(
            selected_time
        )

        if selected_time is None:
            continue

        nearest = min(
            measurements,
            key=lambda row: abs(
                row["time"] - selected_time
            )
        )

        difference = abs(
            nearest["time"] - selected_time
        )

        if difference <= 0.15:
            phase_data[name] = {
                "selected_time": round(
                    selected_time, 2
                ),
                "measured_time": round(
                    nearest["time"], 2
                ),
                "knee": nearest["knee"],
                "elbow": nearest["elbow"],
                "trunk": nearest["trunk"],
            }

        else:
            phase_data[name] = {
                "selected_time": round(
                    selected_time, 2
                ),
                "status": (
                    "No nearby measurement available"
                ),
            }

    # ------------------------------------------
    # 4. PREPARE MEASUREMENT DATA FOR AI
    # ------------------------------------------

    step = max(
        1,
        math.ceil(len(measurements) / 35)
    )

    sample = measurements[::step]

    if sample[-1] != measurements[-1]:
        sample.append(
            measurements[-1]
        )

    data = {
        "front_leg": front_leg,
        "bowling_arm": bowling_arm,
        "bowler_notes": bowler_notes,
        "measured_speed_kmh": bowling_speed,
        "statistics_from_all_frames": statistics,
        "selected_phases": phase_data,
        "sampled_video_measurements": sample,
        "total_measurement_rows": len(measurements),
    }

    # ------------------------------------------
    # 5. AI INSTRUCTIONS
    # ------------------------------------------

    instructions = """
You are PaceIQ, an AI-assisted cricket
fast-bowling analysis assistant.

Generate a professional, beginner-friendly
technique report using the supplied
video-derived measurements.

Return a JSON object with EXACTLY five keys:

overall_assessment
potential_strengths
areas_to_investigate
recommended_drills
next_steps

Each value must be a nonempty string.

REPORT REQUIREMENTS:

overall_assessment:
Write 2-3 concise sentences about the
measured bowling movement.

potential_strengths:
Provide 1-2 evidence-supported observations.
Do not claim good technique without evidence.

areas_to_investigate:
Provide exactly 3 numbered points.
Each point must describe a specific movement
or measurement worth reviewing.

recommended_drills:
Provide exactly 3 numbered points.
Each drill should be beginner-friendly
and have a clear purpose.

next_steps:
Provide exactly 2 numbered points.
Focus on improving measurement quality
and comparing repeated deliveries.

IMPORTANT RULES:

- Reference actual measured angles and times.
- Never invent measurements.
- Never invent visual observations.
- Do not infer arm extension from trunk lean.
- Do not claim that angles prove strong leg drive.
- Do not infer efficient energy transfer.
- Do not infer bowling speed from joint angles.
- Do not recommend maintaining a fixed trunk angle.
- Do not diagnose injuries.
- Do not assess bowling-action legality.
- Selected bowling phases are manually identified.
- Measurements are estimated 2D projections.
- If the evidence is insufficient, recommend
  a specific visual check instead of guessing.
- Do not show internal reasoning.
- Avoid unnecessary technical language.
- Keep the entire report below 350 words.

Return only the requested JSON object.
"""

    # ------------------------------------------
    # 6. GENERATE CLOUD OR LOCAL AI RESPONSE
    # ------------------------------------------

    # Only numerical measurements, phase timestamps and optional
    # bowler notes are sent to the model; the video stays in PaceIQ.
    messages = [
        {"role": "system", "content": instructions},
        {
            "role": "user",
            "content": json.dumps(data, allow_nan=False),
        },
    ]

    def parse_report(content):
        parsed = json.loads((content or "").strip())
        if not isinstance(parsed, dict):
            raise ValueError("AI response is not a JSON object.")
        if not any(
            isinstance(parsed.get(key), str) and parsed[key].strip()
            for key in HEADINGS
        ):
            raise ValueError("AI response has no usable report sections.")
        return parsed

    report = {}
    ai_source = None

    # Root-level Streamlit secrets are also exposed as environment
    # variables. Never store the API key in the GitHub repository.
    groq_key = api_key or os.getenv("GROQ_API_KEY")

    if groq_key:
        try:
            client = Groq(
                api_key=groq_key,
                timeout=25.0,
                max_retries=1,
            )
            response = client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", GROQ_MODEL),
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=1600,
            )
            report = parse_report(
                response.choices[0].message.content
            )
            ai_source = "Groq"

        except Exception as error:
            # Keep the report functional if the cloud API is
            # unavailable, rate-limited or misconfigured.
            logger.warning(
                "Groq coaching unavailable (%s); using rule-based feedback.",
                type(error).__name__,
            )

    else:
        # Local development can still use the installed Ollama model.
        try:
            response = chat(
                model=MODEL,
                messages=messages,
                format="json",
                think=False,
                options={
                    "temperature": 0.1,
                    "num_predict": 1800,
                },
            )
            report = parse_report(response.message.content)
            ai_source = "Ollama"

        except Exception as error:
            logger.info(
                "Local Ollama unavailable (%s); using rule-based feedback.",
                type(error).__name__,
            )

    # ------------------------------------------
    # 7. FALLBACK CONTENT
    # ------------------------------------------

    def measurement_summary(name, values):
        if values["samples"] == 0:
            return (
                f"{name} measurements were unavailable."
            )

        return (
            f"{name} ranged from "
            f"{values['minimum']:.1f}° to "
            f"{values['maximum']:.1f}° "
            f"across {values['samples']} samples."
        )

    fallback = {
        "overall_assessment": (
            measurement_summary(
                "Front knee",
                statistics["knee"]
            )
            + " "
            + measurement_summary(
                "Bowling elbow",
                statistics["elbow"]
            )
            + " "
            + measurement_summary(
                "Trunk lean",
                statistics["trunk"]
            )
        ),

        "potential_strengths": (
            f"PaceIQ captured {len(measurements)} "
            "timestamped measurements. "
            "These allow movement patterns to be "
            "compared across the analysed delivery."
        ),

        "areas_to_investigate": (
            "1. Compare front-knee movement at "
            "front-foot contact and ball release. "
            "Check whether the measured angle changes.\n"
            "2. Review bowling-elbow movement across "
            "successive frames for consistency.\n"
            "3. Compare trunk lean at the selected "
            "phases and confirm the positions visually."
        ),

        "recommended_drills": (
            "1. Delivery-stride walkthroughs: "
            "practise the movement slowly and review "
            "front-foot placement.\n"
            "2. Side-on video review: record three "
            "deliveries from the same camera position "
            "to compare consistency.\n"
            "3. Controlled shadow bowling: rehearse "
            "the bowling sequence without a ball "
            "and review the movement on video."
        ),

        "next_steps": (
            "1. Verify the BFC, FFC and ball-release "
            "timestamps using the video selector.\n"
            "2. Record additional deliveries from "
            "a consistent camera angle to compare "
            "the measured patterns."
        ),
    }

    # ------------------------------------------
    # 8. BUILD FORMATTED REPORT
    # ------------------------------------------

    output = [
        (
            f"# PaceIQ — AI Technique Report ({ai_source})"
            if ai_source
            else "# PaceIQ — Technique Report (Rule-Based)"
        )
    ]

    list_sections = {
        "areas_to_investigate",
        "recommended_drills",
        "next_steps",
    }

    for key, title in HEADINGS.items():

        content = report.get(key)

        if isinstance(content, list):
            content = "\n".join(
                f"{index}. {item}"
                for index, item in enumerate(
                    content, start=1
                )
            )

        if (
            not isinstance(content, str)
            or not content.strip()
        ):
            content = fallback[key]

        content = content.strip()

        if key in list_sections:
            content = format_list(content)

        output.append(
            f"### {title}\n\n{content}"
        )

    return "\n\n".join(output)
