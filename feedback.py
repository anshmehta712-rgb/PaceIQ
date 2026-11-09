
import os
import tempfile

import cv2
import mediapipe as mp

from tracker import MODEL, draw_pose_and_angles


def analyse_movement(
    video_bytes,
    start_time,
    front_leg,
    bowling_arm,
    clip_seconds=5
):
    """
    Sample the bowling clip and record joint angles.
    """

    if not MODEL.exists():
        raise FileNotFoundError("MediaPipe model not found.")

    with tempfile.TemporaryDirectory() as folder:

        path = os.path.join(folder, "video.mp4")

        with open(path, "wb") as file:
            file.write(video_bytes)

        video = cv2.VideoCapture(path)

        try:
            if not video.isOpened():
                raise ValueError("Cannot open video.")

            fps = video.get(cv2.CAP_PROP_FPS)
            total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

            if fps <= 0 or total <= 0:
                raise ValueError("Invalid video.")

            first = max(0, int(start_time * fps))
            first = min(first, total - 1)

            last = min(
                total,
                first + max(1, int(clip_seconds * fps))
            )

            # Sample approximately five times per second
            step = max(1, round(fps / 5))

            options = mp.tasks.vision.PoseLandmarkerOptions(
                base_options=mp.tasks.BaseOptions(
                    model_asset_path=str(MODEL)
                ),
                running_mode=mp.tasks.vision.RunningMode.VIDEO,
                num_poses=1
            )

            records = []

            with mp.tasks.vision.PoseLandmarker.create_from_options(
                options
            ) as detector:

                for frame_number in range(first, last, step):

                    video.set(
                        cv2.CAP_PROP_POS_FRAMES,
                        frame_number
                    )

                    success, frame = video.read()

                    if not success:
                        continue

                    # Match the resolution used in tracking
                    height, width = frame.shape[:2]

                    new_width = 640
                    new_height = max(
                        2,
                        round(height * new_width / width / 2) * 2
                    )

                    frame = cv2.resize(
                        frame,
                        (new_width, new_height)
                    )

                    rgb = cv2.cvtColor(
                        frame,
                        cv2.COLOR_BGR2RGB
                    )

                    image = mp.Image(
                        image_format=mp.ImageFormat.SRGB,
                        data=rgb
                    )

                    timestamp = round(
                        frame_number * 1000 / fps
                    )

                    result = detector.detect_for_video(
                        image,
                        timestamp
                    )

                    row = {
                        "Time (s)": round(frame_number / fps, 3),
                        "Knee": None,
                        "Elbow": None,
                        "Trunk": None
                    }

                    if result.pose_landmarks:

                        _, measurements = draw_pose_and_angles(
                            frame,
                            result.pose_landmarks[0],
                            front_leg=front_leg,
                            bowling_arm=bowling_arm
                        )

                        row["Knee"] = measurements["knee"]
                        row["Elbow"] = measurements["elbow"]
                        row["Trunk"] = measurements["trunk"]

                    records.append(row)

            return records

        finally:
            video.release()


def generate_feedback(records):
    """
    Create cautious, explainable feedback from angles.
    """

    if not records:
        return {
            "summary": "No measurements available.",
            "strengths": [],
            "review": [],
            "suggestions": [],
            "ranges": {}
        }

    strengths = []
    review = []
    suggestions = []
    ranges = {}

    names = ["Knee", "Elbow", "Trunk"]

    for name in names:

        values = [
            row[name]
            for row in records
            if row[name] is not None
        ]

        if len(values) < 3:
            review.append(
                f"{name}: insufficient reliable measurements."
            )
            continue

        lowest = min(values)
        highest = max(values)
        movement_range = round(highest - lowest, 1)

        ranges[name] = movement_range

        strengths.append(
            f"{name} tracking captured {len(values)} "
            f"usable measurements."
        )

        # These thresholds flag movement for review.
        # They are not validated performance standards.
        if name == "Knee" and movement_range >= 20:

            review.append(
                f"Front-knee angle changed by "
                f"{movement_range:.1f}° during the clip."
            )

            suggestions.append(
                "Review knee movement around front-foot "
                "contact and ball release with your coach."
            )

        elif name == "Elbow" and movement_range >= 20:

            review.append(
                f"Bowling-elbow angle changed by "
                f"{movement_range:.1f}° during the clip."
            )

            suggestions.append(
                "Examine the bowling arm across successive "
                "frames. A 2D elbow angle cannot determine "
                "bowling-action legality."
            )

        elif name == "Trunk" and movement_range >= 15:

            review.append(
                f"Projected trunk angle changed by "
                f"{movement_range:.1f}° during the clip."
            )

            suggestions.append(
                "Review trunk movement from front-foot "
                "contact through ball release."
            )

    if not review:
        review.append(
            "No large angle changes were flagged by "
            "the prototype's screening thresholds."
        )

    if not suggestions:
        suggestions.append(
            "Compare multiple deliveries and check "
            "your technique with a qualified coach."
        )

    return {
        "summary": (
            "PaceIQ analysed joint-angle changes across "
            "the selected clip. These observations highlight "
            "movement patterns, not confirmed technique faults."
        ),
        "strengths": strengths,
        "review": review,
        "suggestions": suggestions,
        "ranges": ranges
    }
