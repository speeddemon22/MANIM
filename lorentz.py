from manim import *
import numpy as np
from scipy.integrate import solve_ivp


CYAN_BRIGHT = "#00FFFF"
GOLD_BRIGHT = "#FFD700"


class Scene8bLorenzAttractor(ThreeDScene):
    def construct(self):

        # ── Lorenz parameters ─────────────────────────────────
        sigma, rho, beta = 10, 28, 8/3
        t_max  = 50
        t_eval = np.linspace(0, t_max, 50000)

        def lorenz(t, state):
            x, y, z = state
            return [
                sigma * (y - x),
                x * (rho - z) - y,
                x * y - beta * z
            ]

        # ── 5 ICs differing by 0.00001 ────────────────────────
        ics = [
            [0.10000, 0.0, 0.0],
            [0.10001, 0.0, 0.0],
            [0.10002, 0.0, 0.0],
            [0.10003, 0.0, 0.0],
            [0.10004, 0.0, 0.0],
        ]

        # Cyan → gold gradient across 5 trajectories
        traj_colors = color_gradient([CYAN_BRIGHT, GOLD_BRIGHT], 5)

        solutions = [
            solve_ivp(lorenz, (0, t_max), ic,
                      t_eval=t_eval, method='DOP853',
                      rtol=1e-10, atol=1e-12)
            for ic in ics
        ]

        # ── Scale to Manim scene ──────────────────────────────
        def scale(sol):
            pts = np.array([sol.y[0], sol.y[1], sol.y[2]]).T
            pts[:, 0] /= 10
            pts[:, 1] /= 15
            pts[:, 2]  = pts[:, 2] / 12 - 1.5
            return pts

        all_pts = [scale(s) for s in solutions]
        n_total = len(all_pts[0])

        # ── Camera ────────────────────────────────────────────
        self.set_camera_orientation(phi=75*DEGREES, theta=-60*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.06)

        axes = ThreeDAxes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            z_range=[-2.0, 3.0, 1],
            x_length=5, y_length=5, z_length=5,
            axis_config={"stroke_color": GREY,
                         "stroke_opacity": 0.3,
                         "include_tip": False}
        )
        self.add(axes)

        # ── Fixed frame labels ────────────────────────────────
        title = Text("Lorenz Attractor", font_size=32,
                     color=GOLD_BRIGHT).to_edge(UP)
        subtitle = Text("Five trajectories. Five nearly identical starts.",
                        font_size=20, color=GREY)\
                       .next_to(title, DOWN, buff=0.1)
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(Write(title), Write(subtitle))
        self.wait(0.4)

        # ── Equations briefly ─────────────────────────────────
        eq = MathTex(
            r"\dot{x}=\sigma(y-x) \quad"
            r"\dot{y}=x(\rho-z)-y \quad"
            r"\dot{z}=xy-\beta z",
            font_size=24, color=CYAN_BRIGHT
        ).to_edge(DOWN, buff=0.4)
        params = MathTex(
            r"\sigma=10,\quad\rho=28,\quad\beta=\tfrac{8}{3}",
            font_size=22, color=GREY
        ).next_to(eq, UP, buff=0.15)

        self.add_fixed_in_frame_mobjects(eq, params)
        self.play(Write(eq), Write(params))
        self.wait(2)
        self.play(FadeOut(eq), FadeOut(params))

        # ── IC labels ─────────────────────────────────────────
        ic_labels = VGroup(*[
            MathTex(
                rf"x_0^{{({i+1})}} = 0.1000{i}",
                font_size=18, color=traj_colors[i]
            )
            for i in range(5)
        ]).arrange(DOWN, buff=0.12).to_corner(UL).shift(DOWN*0.8)

        self.add_fixed_in_frame_mobjects(ic_labels)
        self.play(Write(ic_labels))
        self.wait(0.3)

        # ── Build 5 paths — set_shade_in_3d(False) for color ──
        paths = []
        for i, pts in enumerate(all_pts):
            path = VMobject(stroke_width=1.5, stroke_opacity=0.90)
            path.set_stroke(color=traj_colors[i])
            path.set_shade_in_3d(False)          # ← key fix
            path.set_points_smoothly([np.array(p) for p in pts])
            paths.append(path)

        # ── Live dots using Dot3D ─────────────────────────────
        tracker = ValueTracker(0)

        def make_dot(pts, color):
            return always_redraw(lambda: Dot3D(
                point=pts[min(int(tracker.get_value() * n_total),
                              n_total - 1)],
                color=color,
                radius=0.07
            ))

        dots = [make_dot(pts, col)
                for pts, col in zip(all_pts, traj_colors)]

        for d in dots:
            self.add(d)

        # ── Draw all 5 simultaneously ─────────────────────────
        self.play(
            *[Create(p) for p in paths],
            tracker.animate.set_value(1.0),
            run_time=25,
            rate_func=linear
        )
        self.wait(1)

        # ── Divergence callout ────────────────────────────────
        diverge_note = Text(
            "Δx₀ = 0.00001   →   completely different futures",
            font_size=22, color=GOLD_BRIGHT
        ).to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(diverge_note)
        self.play(Write(diverge_note))
        self.wait(1.5)

        # ── Rotate to show butterfly from all angles ──────────
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=90*DEGREES, theta=0*DEGREES,   run_time=4)
        self.wait(1)
        self.move_camera(phi=55*DEGREES, theta=90*DEGREES,  run_time=4)
        self.wait(1)
        self.move_camera(phi=75*DEGREES, theta=-60*DEGREES, run_time=3)
        self.wait(1)

        # ── End card ──────────────────────────────────────────
        self.play(FadeOut(diverge_note))
        end = Text("Deterministic. Bounded. Never repeating.",
                   font_size=26, color=GOLD_BRIGHT)\
                  .to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(end)
        self.play(Write(end))
        self.wait(3)