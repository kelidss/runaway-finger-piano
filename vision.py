import os
import urllib.request
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
from config import Config

class ModelDownloader:
    @staticmethod
    def ensure_model_exists():
        if os.path.exists(Config.MODEL_PATH) and os.path.getsize(Config.MODEL_PATH) > 10_000:
            return
        print("📥 Baixando modelo MediaPipe Hand Landmarker (~8 MB)...")
        try:
            urllib.request.urlretrieve(Config.MODEL_URL, Config.MODEL_PATH)
            print("✅ Modelo baixado com sucesso!")
        except Exception as e:
            print(f"❌ Falha ao baixar modelo: {e}")
            raise SystemExit(1)

class HandTracker:
    def __init__(self):
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=Config.MODEL_PATH),
            running_mode=RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.6,
            min_hand_presence_confidence=0.6,
            min_tracking_confidence=0.5,
        )
        self.detector = HandLandmarker.create_from_options(options)
        self.frame_ts = 0

    def process_frame(self, frame: np.ndarray):
        self.frame_ts += 33
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return self.detector.detect_for_video(mp_image, self.frame_ts)

    @staticmethod
    def is_finger_pressed(landmarks, finger_idx: int, handedness: str) -> bool:
        tip = landmarks[Config.FINGER_TIPS[finger_idx]]
        pip = landmarks[Config.FINGER_PIPS[finger_idx]]
        if finger_idx == 0:
            return tip.x < pip.x if handedness == "Right" else tip.x > pip.x
        return tip.y > pip.y - 0.02

    def close(self):
        self.detector.close()