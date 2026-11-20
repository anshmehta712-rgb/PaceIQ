"""Conservative prototype screening, not clinical or performance standards."""
import math

# Observed participant mean ranges, NOT universal ideal ranges.
# Wickington & Linthorne (2017), Sports 5(1), 18.
# https://doi.org/10.3390/sports5010018
REFERENCE = {
    "BFC": ("Back Knee", 141, 176),
    "FFC": ("Knee", 148, 179),
    "Release": ("Knee", 125, 178),
}
# Provisional app-level quality screen for the loaded leg at a selected phase.
# Extreme but genuine measurements may also be excluded; review the video.
MIN_LOADED_KNEE = 90

def validate_phase(row, phase):
    """Keep valid observations; annotate missing and suspect measurements."""
    result = dict(row)
    target = REFERENCE.get(phase)
    for joint, upper in (("Knee", 180), ("Back Knee", 180),
                         ("Elbow", 180), ("Trunk", 90)):
        reason_key = joint + " quality"
        reason = result.get(reason_key)
        try:
            value = float(result.get(joint))
        except (ValueError, TypeError):
            value = float("nan")
        if not math.isfinite(value) or not 0 <= value <= upper:
            result[joint] = None
            result[reason_key] = reason or "Unavailable: missing or invalid landmarks"
        elif target and joint == target[0] and value < MIN_LOADED_KNEE:
            result[joint] = None
            result[reason_key] = "Unavailable: extreme projected knee angle; check selected frame"
        else:
            result[joint] = value
            if target and joint == target[0]:
                result[reason_key] = (
                    "Within study reference" if target[1] <= value <= target[2]
                    else "Outside study reference; review"
                )
            else:
                result[reason_key] = "Measured; no validated phase reference"
    return result

def reference_text(phase):
    ref = REFERENCE.get(phase)
    if not ref:
        return "Not established"
    joint, low, high = ref
    label = "Front knee" if joint == "Knee" else "Back knee"
    return f"{label}: {low}–{high}° (observed study means)"
