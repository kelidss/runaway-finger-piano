import cv2
import time
import numpy as np

# Importações dos seus novos módulos locais
from config import Config
from audio import AudioEngine
from vision import ModelDownloader, HandTracker
from ui import UIRenderer

class FingerPianoApp:
    def __init__(self):
        ModelDownloader.ensure_model_exists()
        
        self.audio_engine = AudioEngine()
        self.hand_tracker = HandTracker()
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            raise RuntimeError("Câmera não encontrada!")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAM_HEIGHT)

        self.prev_pressed = {k: False for k in Config.FINGER_KEYS}
        self.cooldowns = {k: 0.0 for k in Config.FINGER_KEYS}
        self.seq_idx = 0
        self.wave_buf = [0.0] * 360

    def run(self):
        print("\n🎵 RUNAWAY - HUD Edition iniciada! Aperte Q na janela de vídeo para sair.\n")

        cv2.namedWindow("RUNAWAY - Finger Piano (HUD Edition)", cv2.WINDOW_NORMAL)

        while True:
            ret, frame = self.cap.read()
            if not ret: break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            now = time.time()
            display_frame = frame.copy()

            UIRenderer.draw_background_tint(display_frame)

            result = self.hand_tracker.process_frame(frame)
            active_fingers = {k: False for k in Config.FINGER_KEYS}

            if result.hand_landmarks:
                for hand_idx, landmarks in enumerate(result.hand_landmarks):
                    handedness_str = result.handedness[hand_idx][0].category_name if result.handedness else "Right"

                    for i, finger in enumerate(Config.FINGER_KEYS):
                        is_pressed = self.hand_tracker.is_finger_pressed(landmarks, i, handedness_str)
                        active_fingers[finger] = is_pressed

                        if is_pressed and not self.prev_pressed[finger] and now > self.cooldowns[finger]:
                            note = Config.FINGER_NOTES[finger]
                            self.audio_engine.play_note(note)
                            self.cooldowns[finger] = now + Config.COOLDOWN_SEC

                            freq = Config.NOTE_FREQS[note]
                            self.wave_buf.extend([np.sin(2*np.pi*freq*t/Config.SAMPLE_RATE) for t in range(40)])

                            target_note = Config.RUNAWAY_SEQUENCE[self.seq_idx % len(Config.RUNAWAY_SEQUENCE)]
                            if note == target_note:
                                self.seq_idx += 1

                        self.prev_pressed[finger] = is_pressed

                    UIRenderer.draw_landmarks(display_frame, landmarks, active_fingers, w, h)

            self.wave_buf = self.wave_buf[-360:]
            if len(self.wave_buf) < 360:
                self.wave_buf = [0.0]*(360 - len(self.wave_buf)) + self.wave_buf

            UIRenderer.draw_title(display_frame, w, h)
            UIRenderer.draw_sequence(display_frame, self.seq_idx, w, h)
            UIRenderer.draw_waveform(display_frame, self.wave_buf, w, h)
            UIRenderer.draw_piano_keys(display_frame, active_fingers, h, w)

            s = w / 1280.0
            cv2.putText(display_frame, "Dobre os dedos para tocar  |  Pressione 'Q' para sair", 
                        (w//2 - int(200*s), h - int(15*s)), cv2.FONT_HERSHEY_SIMPLEX, 0.5*s, (100,100,100), max(1, int(1*s)), cv2.LINE_AA)

            cv2.imshow("RUNAWAY - Finger Piano (HUD Edition)", display_frame)
            if cv2.waitKey(1) & 0xFF in (ord('q'), 27):
                break

        self.cleanup()

    def cleanup(self):
        self.hand_tracker.close()
        self.cap.release()
        cv2.destroyAllWindows()
        self.audio_engine.quit()

if __name__ == "__main__":
    app = FingerPianoApp()
    app.run()