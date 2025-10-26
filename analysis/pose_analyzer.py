# analysis/pose_analyzer.py
import cv2
import numpy as np
import os
import json
from typing import Tuple, Optional
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def process_video_with_pose(input_path: str, output_path: str, landmarks_json: Optional[str]=None, 
                            draw_landmarks=True, model_complexity=1, min_detection_confidence=0.5,
                            min_tracking_confidence=0.5) -> Tuple[int, int]:
    """
    Process input video and write skeleton-overlaid result to output_path.
    Returns (frame_count, fps).
    Optionally writes per-frame landmarks to landmarks_json (list of dicts).
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input not found: {input_path}")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError("Cannot open video")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4 container
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    landmarks_list = [] if landmarks_json else None
    frame_count = 0

    with mp_pose.Pose(static_image_mode=False,
                      model_complexity=model_complexity,
                      enable_segmentation=False,
                      min_detection_confidence=min_detection_confidence,
                      min_tracking_confidence=min_tracking_confidence) as pose:

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1

            # MediaPipe expects RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                if draw_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                    )

                if landmarks_list is not None:
                    # Convert landmarks to serializable format + bounding box
                    lm = []
                    xs = []
                    ys = []
                    for l in results.pose_landmarks.landmark:
                        lm.append({'x': l.x, 'y': l.y, 'z': l.z, 'visibility': l.visibility})
                        xs.append(l.x)
                        ys.append(l.y)
                    # Bounding box approx
                    if xs and ys:
                        minx, maxx = min(xs), max(xs)
                        miny, maxy = min(ys), max(ys)
                        bbox = {'xmin': minx, 'xmax': maxx, 'ymin': miny, 'ymax': maxy}
                    else:
                        bbox = None
                    landmarks_list.append({'frame': frame_count, 'landmarks': lm, 'bbox': bbox, 'has_landmarks': True})
            else:
                if landmarks_list is not None:
                    landmarks_list.append({'frame': frame_count, 'landmarks': [], 'bbox': None, 'has_landmarks': False})

            out.write(frame)

    cap.release()
    out.release()

    if landmarks_json:
        with open(landmarks_json, 'w') as f:
            json.dump(landmarks_list, f)

    return frame_count, int(fps)
