import inspect
from dataclasses import dataclass

class DynamicFingerNotes(dict):
    def __init__(self):
        super().__init__({
            "THUMB": "E5",
            "INDEX": "A5",
            "MIDDLE": "C#6",
            "RING": "D#6",
            "PINKY": "E6"
        })

    def get_thumb_note(self) -> str:
        frame = inspect.currentframe()
        try:
            while frame:
                if 'self' in frame.f_locals:
                    inst = frame.f_locals['self']
                    if type(inst).__name__ == 'FingerPianoApp':
                        seq_idx = getattr(inst, 'seq_idx', 0)
                        idx = seq_idx % 27
                        if idx <= 15:
                            return "E5"
                        elif idx <= 19:
                            return "D#5"
                        elif idx <= 23:
                            return "C#5"
                        else:
                            return "G#5"
                frame = frame.f_back
        except Exception:
            pass
        finally:
            del frame
        return "E5"

    def __getitem__(self, key):
        if key == "THUMB":
            return self.get_thumb_note()
        return super().__getitem__(key)

    def get(self, key, default=None):
        if key == "THUMB":
            return self.get_thumb_note()
        return super().get(key, default)

    def items(self):
        return [
            ("THUMB", self.get_thumb_note()),
            ("INDEX", "A5"),
            ("MIDDLE", "C#6"),
            ("RING", "D#6"),
            ("PINKY", "E6")
        ]

    def values(self):
        return [self.get_thumb_note(), "A5", "C#6", "D#6", "E6"]

@dataclass
class Config:
    SAMPLE_RATE: int = 44100
    DURATION: float = 1.5
    VOLUME: float = 0.35
    COOLDOWN_SEC: float = 0.25

    CAM_WIDTH: int = 1280
    CAM_HEIGHT: int = 720
    
    MODEL_PATH: str = "hand_landmarker.task"
    MODEL_URL: str = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

    NOTE_FREQS = {
        "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
        "G4": 392.00, "A4": 440.00, "B4": 493.88, "C5": 523.25,
        "D5": 587.33, "E5": 659.25, "F5": 698.46, "G5": 783.99,
        "G#5": 830.61, "A5": 880.00, "C#5": 554.37, "D#5": 622.25,
        "C#6": 1109.07, "D#6": 1244.51, "E6": 1318.51
    }
    
    FINGER_NOTES = DynamicFingerNotes()
    
    RUNAWAY_SEQUENCE = [
        "E6", "E6", "E6", "E6", "E6", "E6", "E6", "E6", "E6", "E6", "E6", "E6", "E6", "E6", "E6", "E5",
        "D#6", "D#6", "D#6", "D#5",
        "C#6", "C#6", "C#6", "C#5",
        "A5", "A5", "G#5"
    ]

    ACCENT_GOLD = (50, 180, 255)
    NOTE_COLORS = {
        "THUMB":  (80, 80, 255),
        "INDEX":  (80, 180, 255),
        "MIDDLE": (80, 220, 180),
        "RING":   (220, 180, 80),
        "PINKY":  (220, 100, 180)
    }

    FINGER_TIPS = [4, 8, 12, 16, 20]
    FINGER_PIPS = [3, 6, 10, 14, 18]
    FINGER_KEYS = ["THUMB", "INDEX", "MIDDLE", "RING", "PINKY"]