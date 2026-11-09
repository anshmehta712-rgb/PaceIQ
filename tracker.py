
import os
import math
import tempfile
from pathlib import Path

import cv2
import mediapipe as mp
import imageio_ffmpeg


# MEDIAPIPE MODEL
MODEL = (
    Path(__file__).parent
    / "models"
    / "pose_landmarker_lite.task"
)


# BODY CONNECTIONS
CONNECTIONS = [
    (11, 12),
    (11, 13),
    (13, 15),
    (12, 14),
    (14, 16),
    (11, 23),
    (12, 24),
    (23, 24),
    (23, 25),
    (25, 27),
    (24, 26),
    (26, 28)
]


# BODY LANDMARK NUMBERS
LEFT = {
    "shoulder": 11,
    "elbow": 13,
    "wrist": 15,
    "hip": 23,
    "knee": 25,
    "ankle": 27
}

RIGHT = {
    "shoulder": 12,
    "elbow": 14,
    "wrist": 16,
    "hip": 24,
    "knee": 26,
    "ankle": 28
}


# COLOURS (OpenCV uses BGR)
YELLOW = (0, 215, 255)
GREEN = (80, 220, 80)
CYAN = (255, 220, 60)
PINK = (200, 90, 255)
WHITE = (255, 255, 255)


# FUNCTION 1: VIDEO INFORMATION
def video_information(video_bytes):

    with tempfile.TemporaryDirectory() as folder:

        path = os.path.join(folder, "input.mp4")

        with open(path, "wb") as file:
            file.write(video_bytes)

        video = cv2.VideoCapture(path)

        try:
            if not video.isOpened():
                raise ValueError("Cannot open uploaded video.")

            frames = int(
                video.get(cv2.CAP_PROP_FRAME_COUNT)
            )

            fps = video.get(cv2.CAP_PROP_FPS)

            if frames <= 0 or fps <= 0:
                raise ValueError("Invalid video information.")

            duration = frames / fps

            return frames, fps, duration

        finally:
            video.release()


# FUNCTION 2: CALCULATE JOINT ANGLE
def calculate_angle(a, b, c):

    # Calculate the angle at point B
    vector1 = (
        a[0] - b[0],
        a[1] - b[1]
    )

    vector2 = (
        c[0] - b[0],
        c[1] - b[1]
    )

    length1 = math.hypot(*vector1)
    length2 = math.hypot(*vector2)

    if length1 == 0 or length2 == 0:
        return None

    dot_product = (
        vector1[0] * vector2[0]
        + vector1[1] * vector2[1]
    )

    cosine = dot_product / (length1 * length2)

    cosine = max(-1, min(1, cosine))

    angle = math.degrees(math.acos(cosine))

    return round(angle, 1)


# FUNCTION 3: TRUNK LEAN
def calculate_trunk_lean(shoulder, hip):

    dx = shoulder[0] - hip[0]
    dy = shoulder[1] - hip[1]

    if dx == 0 and dy == 0:
        return None

    angle = math.degrees(
        math.atan2(abs(dx), abs(dy))
    )

    return round(angle, 1)


# FUNCTION 4: MIDPOINT
def midpoint(a, b):

    x = (a[0] + b[0]) // 2
    y = (a[1] + b[1]) // 2

    return (x, y)


# FUNCTION 5: CONVERT BODY LANDMARKS
def collect_points(landmarks, width, height):

    points = {}

    for index in range(11, 29):

        joint = landmarks[index]

        # Ignore joints that are not clearly visible
        if joint.visibility < 0.5:
            continue

        if not (
            0 <= joint.x <= 1
            and 0 <= joint.y <= 1
        ):
            continue

        x = int(joint.x * width)
        y = int(joint.y * height)

        points[index] = (x, y)

    return points


# FUNCTION 6: DRAW TEXT
def draw_text(frame, text, x, y, color=WHITE):

    cv2.putText(
        frame,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        color,
        1,
        cv2.LINE_AA
    )


# FUNCTION 7: DRAW SKELETON AND ANGLES
def draw_pose_and_angles(
    frame,
    landmarks,
    front_leg="right",
    bowling_arm="left"
):

    height, width = frame.shape[:2]

    marked = frame.copy()

    points = collect_points(
        landmarks,
        width,
        height
    )

    # SMALLER, CLEANER SKELETON
    for start, end in CONNECTIONS:

        if start in points and end in points:

            cv2.line(
                marked,
                points[start],
                points[end],
                YELLOW,
                1,
                cv2.LINE_AA
            )

    for point in points.values():

        cv2.circle(
            marked,
            point,
            2,
            YELLOW,
            -1,
            cv2.LINE_AA
        )

    # SELECT BODY SIDES
    leg = (
        RIGHT
        if front_leg.lower() == "right"
        else LEFT
    )

    arm = (
        RIGHT
        if bowling_arm.lower() == "right"
        else LEFT
    )

    knee_angle = None
    elbow_angle = None
    trunk_angle = None

    # FRONT KNEE
    hip = leg["hip"]
    knee = leg["knee"]
    ankle = leg["ankle"]

    if all(
        i in points
        for i in [hip, knee, ankle]
    ):

        knee_angle = calculate_angle(
            points[hip],
            points[knee],
            points[ankle]
        )

        cv2.circle(
            marked,
            points[knee],
            4,
            GREEN,
            -1
        )

    # BOWLING ELBOW
    shoulder = arm["shoulder"]
    elbow = arm["elbow"]
    wrist = arm["wrist"]

    if all(
        i in points
        for i in [shoulder, elbow, wrist]
    ):

        elbow_angle = calculate_angle(
            points[shoulder],
            points[elbow],
            points[wrist]
        )

        cv2.circle(
            marked,
            points[elbow],
            4,
            CYAN,
            -1
        )

    # TRUNK LEAN
    if all(
        i in points
        for i in [11, 12, 23, 24]
    ):

        shoulder_middle = midpoint(
            points[11],
            points[12]
        )

        hip_middle = midpoint(
            points[23],
            points[24]
        )

        trunk_angle = calculate_trunk_lean(
            shoulder_middle,
            hip_middle
        )

        cv2.line(
            marked,
            hip_middle,
            shoulder_middle,
            PINK,
            2,
            cv2.LINE_AA
        )

    # FORMAT ANGLE VALUES
    def display_angle(angle):

        if angle is None:
            return "N/A"

        return f"{angle:.1f} deg"

    # DRAW A SMALL RESULTS PANEL
    panel_height = 88

    overlay = marked.copy()

    cv2.rectangle(
        overlay,
        (8, height - panel_height - 8),
        (230, height - 8),
        (12, 18, 28),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.85,
        marked,
        0.15,
        0,
        marked
    )

    draw_text(
        marked,
        f"Knee:  {display_angle(knee_angle)}",
        18,
        height - 68,
        GREEN
    )

    draw_text(
        marked,
        f"Elbow: {display_angle(elbow_angle)}",
        18,
        height - 44,
        CYAN
    )

    draw_text(
        marked,
        f"Trunk: {display_angle(trunk_angle)}",
        18,
        height - 20,
        PINK
    )

    measurements = {
        "knee": knee_angle,
        "elbow": elbow_angle,
        "trunk": trunk_angle
    }

    return marked, measurements


# FUNCTION 8: PROCESS THE COMPLETE CLIP
def process_video(
    video_bytes,
    start_time,
    clip_seconds=5,
    front_leg="right",
    bowling_arm="left"
):

    if not MODEL.exists():
        raise FileNotFoundError(
            "MediaPipe model missing. "
            "Check models/pose_landmarker_lite.task"
        )

    with tempfile.TemporaryDirectory() as folder:

        input_path = os.path.join(
            folder,
            "input.mp4"
        )

        output_path = os.path.join(
            folder,
            "PaceIQ_Tracked.mp4"
        )

        with open(input_path, "wb") as file:
            file.write(video_bytes)

        video = cv2.VideoCapture(input_path)

        if not video.isOpened():
            raise ValueError("Cannot open video.")

        writer = None

        try:
            fps = video.get(cv2.CAP_PROP_FPS)

            total_frames = int(
                video.get(cv2.CAP_PROP_FRAME_COUNT)
            )

            width = int(
                video.get(cv2.CAP_PROP_FRAME_WIDTH)
            )

            height = int(
                video.get(cv2.CAP_PROP_FRAME_HEIGHT)
            )

            if (
                fps <= 0
                or total_frames <= 0
                or width <= 0
                or height <= 0
            ):
                raise ValueError(
                    "Invalid video information."
                )

            # RESIZE VIDEO
            new_width = 640

            new_height = max(
                2,
                round(
                    height * new_width / width / 2
                ) * 2
            )

            # SELECT VIDEO SECTION
            first_frame = min(
                total_frames - 1,
                max(0, int(start_time * fps))
            )

            frame_count = min(
                max(1, int(clip_seconds * fps)),
                total_frames - first_frame
            )

            # MEDIAPIPE SETTINGS
            options = (
                mp.tasks.vision.PoseLandmarkerOptions(
                    base_options=mp.tasks.BaseOptions(
                        model_asset_path=str(MODEL)
                    ),
                    running_mode=(
                        mp.tasks.vision.RunningMode.VIDEO
                    ),
                    num_poses=1
                )
            )

            # CREATE MP4 VIDEO WRITER
            writer = imageio_ffmpeg.write_frames(
                output_path,
                size=(
                    new_width * 2,
                    new_height
                ),
                fps=fps,
                codec="libx264",
                pix_fmt_in="rgb24",
                pix_fmt_out="yuv420p",
                quality=6,
                output_params=[
                    "-movflags",
                    "+faststart"
                ]
            )

            writer.send(None)

            video.set(
                cv2.CAP_PROP_POS_FRAMES,
                first_frame
            )

            processed = 0
            detected = 0

            # PROCESS EACH FRAME
            with mp.tasks.vision.PoseLandmarker.create_from_options(
                options
            ) as detector:

                for i in range(frame_count):

                    success, frame = video.read()

                    if not success:
                        break

                    frame = cv2.resize(
                        frame,
                        (new_width, new_height)
                    )

                    original = frame.copy()
                    annotated = frame.copy()

                    # CONVERT TO RGB
                    rgb = cv2.cvtColor(
                        frame,
                        cv2.COLOR_BGR2RGB
                    )

                    image = mp.Image(
                        image_format=mp.ImageFormat.SRGB,
                        data=rgb
                    )

                    timestamp = round(
                        (first_frame + i) * 1000 / fps
                    )

                    # DETECT BODY
                    result = detector.detect_for_video(
                        image,
                        timestamp
                    )

                    if result.pose_landmarks:

                        annotated, measurements = (
                            draw_pose_and_angles(
                                annotated,
                                result.pose_landmarks[0],
                                front_leg=front_leg,
                                bowling_arm=bowling_arm
                            )
                        )

                        detected += 1

                    # COMBINE ORIGINAL AND TRACKED
                    combined = cv2.hconcat([
                        original,
                        annotated
                    ])

                    # VIDEO LABELS
                    cv2.putText(
                        combined,
                        "ORIGINAL",
                        (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        WHITE,
                        2,
                        cv2.LINE_AA
                    )

                    cv2.putText(
                        combined,
                        "TRACKING + ANGLES",
                        (new_width + 15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        YELLOW,
                        2,
                        cv2.LINE_AA
                    )

                    # CONVERT FOR VIDEO ENCODER
                    output = cv2.cvtColor(
                        combined,
                        cv2.COLOR_BGR2RGB
                    )

                    writer.send(
                        output.tobytes()
                    )

                    processed += 1

            writer.close()
            writer = None

            if processed == 0:
                raise ValueError(
                    "No video frames were processed."
                )

            # READ COMPLETED VIDEO
            with open(output_path, "rb") as file:
                finished_video = file.read()

            return (
                finished_video,
                processed,
                detected
            )

        finally:
            video.release()

            if writer is not None:
                writer.close()
