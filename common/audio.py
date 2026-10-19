"""Música y efectos sintetizados con numpy, como `m.Sound` listos para usar.

Música de fondo: `self.add_sound(audio.pad().gain(-22).fade_in(2).loop())`,
y al final `clip.stop(fade=2)`. Efectos: `self.play(anim, audio.whoosh())`.
"""

import manimgx as m
import numpy as np


def pad(duration: float = 4.0, root_hz: float = 110.0) -> m.Sound:
    """Acorde mayor suave que enlaza sin corte en bucle.

    Cada frecuencia da un número entero de ciclos en `duration`, así el final
    empalma con el principio.
    """
    ratios = (1.0, 1.25, 1.5, 2.0)  # tónica, tercera, quinta, octava

    def wave(t: np.ndarray) -> np.ndarray:
        out = np.zeros_like(t)
        for i, r in enumerate(ratios):
            f = round(root_hz * r * duration) / duration
            out += np.sin(2 * np.pi * f * t) / (i + 1)
        swell = 0.75 + 0.25 * np.sin(2 * np.pi * t / duration)  # un vaivén por ciclo
        return 0.15 * out * swell

    return m.Sound.of(wave, duration)


def whoosh(duration: float = 0.8, seed: int = 0) -> m.Sound:
    """Soplo de ruido filtrado que crece y se apaga."""
    duration = min(duration, 1.0)
    rng = np.random.default_rng(seed)

    def wave(t: np.ndarray) -> np.ndarray:
        noise = rng.standard_normal(len(t))
        kernel = np.ones(64) / 64
        smooth = np.convolve(noise, kernel, mode="same")
        envelope = np.sin(np.pi * t / duration) ** 2
        return 0.6 * smooth * envelope

    return m.Sound.of(wave, duration)


def chime(hz: float = 880.0, duration: float = 0.8) -> m.Sound:
    """Campanita: dos parciales que decaen."""

    def wave(t: np.ndarray) -> np.ndarray:
        tone = np.sin(2 * np.pi * hz * t) + 0.4 * np.sin(2 * np.pi * 1.5 * hz * t)
        return 0.25 * tone * np.exp(-5 * t)

    return m.Sound.of(wave, min(duration, 1.0))
