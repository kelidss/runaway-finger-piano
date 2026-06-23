import numpy as np
import pygame
from scipy.signal import sawtooth
from config import Config

class AudioEngine:
    def __init__(self):
        pygame.mixer.init(frequency=Config.SAMPLE_RATE, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self._pregenerate_sounds()

    def _synthesize_note(self, freq: float) -> np.ndarray:
        t = np.linspace(0, Config.DURATION, int(Config.SAMPLE_RATE * Config.DURATION), endpoint=False)
        
        wave = 0.50 * np.sin(2 * np.pi * freq * 1.000 * t) * np.exp(-2.0 * t)
        wave += 0.35 * np.sin(2 * np.pi * freq * 1.0025 * t) * np.exp(-2.0 * t)
        
        wave += 0.25 * np.sin(2 * np.pi * freq * 2 * t) * np.exp(-4.0 * t)
        wave += 0.15 * np.sin(2 * np.pi * freq * 3 * t) * np.exp(-6.0 * t)
        wave += 0.08 * np.sin(2 * np.pi * freq * 4 * t) * np.exp(-9.0 * t)
        wave += 0.04 * np.sin(2 * np.pi * freq * 5 * t) * np.exp(-12.0 * t)
        
        click = np.random.normal(0, 1, len(t)) * np.exp(-150.0 * t) * 0.15
        wave += click
        
        fade_out = int(0.05 * Config.SAMPLE_RATE)
        if len(t) > fade_out:
            wave[-fade_out:] *= np.linspace(1, 0, fade_out)

        wave = wave * Config.VOLUME
        wave_int = (wave * 32767).astype(np.int16)
        return np.column_stack([wave_int, wave_int])

    def _pregenerate_sounds(self):
        for name, freq in Config.NOTE_FREQS.items():
            self.sounds[name] = pygame.sndarray.make_sound(self._synthesize_note(freq))

    def play_note(self, note_name: str):
        if note_name in self.sounds:
            self.sounds[note_name].play()

    def quit(self):
        pygame.quit()