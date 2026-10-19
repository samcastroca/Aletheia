"""Proyección estereográfica: un círculo de la esfera se proyecta en un círculo del plano."""

import manimgx as m
import numpy as np

from common import audio, style

style.apply()

R = 1.5  # radio de la esfera
NORTH = np.array([0.0, 0.0, R])

# Círculo inclinado de la esfera: eje a 130° del polo norte, radio angular 35°.
# Queda en el hemisferio sur, así que su imagen cabe en el plano visible (|Q| < 2R).
ALPHA, BETA = 130 * m.DEGREES, 35 * m.DEGREES
AXIS = np.array([np.sin(ALPHA), 0.0, np.cos(ALPHA)])
U = np.array([np.cos(ALPHA), 0.0, -np.sin(ALPHA)])
V = np.cross(AXIS, U)


def on_sphere(t: float) -> np.ndarray:
    """Punto del círculo inclinado, para t en [0, 2π]."""
    return R * (np.cos(BETA) * AXIS + np.sin(BETA) * (np.cos(t) * U + np.sin(t) * V))


def project(p: np.ndarray) -> np.ndarray:
    """Proyección desde el polo norte sobre el plano tangente en el polo sur, z = -R."""
    k = 2 * R / (R - p[2])
    return np.array([k * p[0], k * p[1], -R])


class StereographicProjection(m.ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(
            phi=64 * m.DEGREES, theta=-55 * m.DEGREES, zoom=0.9, frame_center=[0, 0, -0.5 * R]
        )
        music = self.add_sound(audio.pad().gain(-22).fade_in(2).loop())

        title = m.Text("Proyección estereográfica", font_size=style.TITLE_SIZE, color=style.INK)
        title.to_corner(m.UL)
        self.add_fixed_in_frame_mobjects(title)

        plane = m.Square(
            side_length=6,
            stroke_color=style.DIM,
            stroke_width=1,
            fill_color=style.DIM,
            fill_opacity=0.12,
        ).shift([0, 0, -R])
        sphere = m.Sphere(radius=R, resolution=(36, 18)).set_fill_by_checkerboard(
            style.CYAN, m.ManimColor(style.CYAN).darker(0.4), opacity=0.18
        )
        north = m.Dot3D(point=NORTH, radius=0.07, color=style.AMBER)
        self.play(m.FadeIn(title), m.Create(plane), m.FadeIn(sphere), run_time=2)
        self.play(m.FadeIn(north, scale=2), audio.chime(), run_time=0.8)

        # Todo lo que se mueve deriva de t: nada cuenta frames.
        t = m.ValueTracker(1e-3)
        point = m.always_redraw(
            lambda: m.Dot3D(point=on_sphere(t.get_value()), radius=0.06, color=style.CYAN)
        )
        image = m.always_redraw(
            lambda: m.Dot3D(point=project(on_sphere(t.get_value())), radius=0.06, color=style.MAGENTA)
        )
        ray = m.always_redraw(
            lambda: m.Line3D(
                NORTH, project(on_sphere(t.get_value())), thickness=0.012, color=style.AMBER
            )
        )
        arc = m.always_redraw(
            lambda: m.ParametricFunction(
                on_sphere, t_range=(0, t.get_value()), color=style.CYAN, stroke_width=3
            )
        )
        shadow = m.always_redraw(
            lambda: m.ParametricFunction(
                lambda s: project(on_sphere(s)),
                t_range=(0, t.get_value()),
                color=style.MAGENTA,
                stroke_width=3,
            )
        )
        self.play(m.FadeIn(point), m.FadeIn(image), m.Create(ray), audio.whoosh(), run_time=1)
        self.add(arc, shadow)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(t.animate.set_value(m.TAU), run_time=6, rate_func=m.linear)

        caption = m.Text(
            "Un círculo de la esfera se proyecta en un círculo del plano",
            font_size=style.TEXT_SIZE,
            color=style.INK,
        ).to_edge(m.DOWN)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(m.FadeIn(caption, shift=0.2 * m.UP), run_time=1.5)
        self.wait(2)
        music.stop(fade=2)
        self.wait(2)
