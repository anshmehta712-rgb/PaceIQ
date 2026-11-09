
import os
import tempfile
import cv2


def get_preview_frame(video_bytes, seconds):
    """Return an RGB preview frame and its exact video timestamp."""

    with tempfile.TemporaryDirectory() as folder:
        video_path = os.path.join(folder, "video.mp4")

        with open(video_path, "wb") as file:
            file.write(video_bytes)

        capture = cv2.VideoCapture(video_path)

        try:
            if not capture.isOpened():
                raise ValueError("Could not open uploaded video")

            fps = capture.get(cv2.CAP_PROP_FPS)
            count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

            if fps <= 0 or count <= 0:
                raise ValueError(
                    "Video frame rate or frame count is invalid"
                )

            index = max(
                0,
                min(round(seconds * fps), count - 1)
            )

            capture.set(cv2.CAP_PROP_POS_FRAMES, index)
            success, frame = capture.read()

            if not success:
                raise ValueError(
                    "Could not extract the selected frame"
                )

            height, width = frame.shape[:2]

            if width > 800:
                frame = cv2.resize(
                    frame,
                    (800, max(1, round(height * 800 / width)))
                )

            return (
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                index / fps
            )

        finally:
            capture.release()



def get_phase_measurements(records, selected_time, tolerance=0.15):
    """
    Find measured knee, elbow and trunk angles
    nearest to a selected bowling phase.
    """

    if not records:
        return None

    valid_records = [
        row for row in records
        if row.get("Time (s)") is not None
    ]

    if not valid_records:
        return None

    nearest = min(
        valid_records,
        key=lambda row: abs(
            float(row["Time (s)"]) - selected_time
        )
    )

    measured_time = float(nearest["Time (s)"])

    if abs(measured_time - selected_time) > tolerance:
        return None

    return {
        "Time": measured_time,
        "Knee": nearest.get("Knee"),
        "Elbow": nearest.get("Elbow"),
        "Trunk": nearest.get("Trunk"),
    }

