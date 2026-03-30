from manim import *
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d


GOLD_BRIGHT = "#FFD700"
ORANGE_GLOW = "#FF6B00"
CYAN_BRIGHT = "#00FFFF"
TEAL_BRIGHT = "#00E5CC"
WHITE_SOFT  = "#E8E8E8"


class Scene8SensitiveDependence(Scene):
    def construct(self):

        # ── Physics ───────────────────────────────────────────
        m1, m2 = 1.0, 1.0
        L1, L2 = 1.2, 1.2
        g      = 9.8
        t_max  = 20
        t_eval = np.linspace(0, t_max, 8000)

        def double_pendulum(t, state):
            th1, w1, th2, w2 = state
            d   = th1 - th2
            D   = 2*m1 + m2 - m2*np.cos(2*d)
            dw1 = (
                -g*(2*m1+m2)*np.sin(th1)
                - m2*g*np.sin(th1 - 2*th2)
                - 2*np.sin(d)*m2*(w2**2*L2 + w1**2*L1*np.cos(d))
            ) / (L1 * D)
            dw2 = (
                2*np.sin(d)*(
                    w1**2*L1*(m1+m2)
                    + g*(m1+m2)*np.cos(th1)
                    + w2**2*L2*m2*np.cos(d)
                )
            ) / (L2 * D)
            return [w1, dw1, w2, dw2]

        # Identical except θ₁ differs by 0.0001π
        ic_a = [np.pi*0.9500, 0.0, np.pi*0.6200, 0.0]
        ic_b = [np.pi*0.9501, 0.0, np.pi*0.6200, 0.0]

        sol_a = solve_ivp(double_pendulum, (0, t_max), ic_a,
                          t_eval=t_eval, method='DOP853',
                          rtol=1e-10, atol=1e-12)
        sol_b = solve_ivp(double_pendulum, (0, t_max), ic_b,
                          t_eval=t_eval, method='DOP853',
                          rtol=1e-10, atol=1e-12)

        th1a = interp1d(sol_a.t, sol_a.y[0])
        th2a = interp1d(sol_a.t, sol_a.y[2])
        th1b = interp1d(sol_b.t, sol_b.y[0])
        th2b = interp1d(sol_b.t, sol_b.y[2])

        pivot = np.array([0.0, 2.0, 0])

        def pa1(time):
            tt = min(time, t_max - 0.01)
            return pivot + np.array([L1*np.sin(th1a(tt)),
                                     -L1*np.cos(th1a(tt)), 0])
        def pa2(time):
            tt = min(time, t_max - 0.01)
            return pa1(time) + np.array([L2*np.sin(th2a(tt)),
                                         -L2*np.cos(th2a(tt)), 0])
        def pb1(time):
            tt = min(time, t_max - 0.01)
            return pivot + np.array([L1*np.sin(th1b(tt)),
                                     -L1*np.cos(th1b(tt)), 0])
        def pb2(time):
            tt = min(time, t_max - 0.01)
            return pb1(time) + np.array([L2*np.sin(th2b(tt)),
                                         -L2*np.cos(th2b(tt)), 0])

        tracker = ValueTracker(0)

        # ── Rods ──────────────────────────────────────────────
        rod_a1 = always_redraw(lambda: Line(
            pivot, pa1(tracker.get_value()),
            color=CYAN_BRIGHT, stroke_width=2.5, stroke_opacity=0.7
        ))
        rod_a2 = always_redraw(lambda: Line(
            pa1(tracker.get_value()), pa2(tracker.get_value()),
            color=CYAN_BRIGHT, stroke_width=2.5, stroke_opacity=0.7
        ))
        rod_b1 = always_redraw(lambda: Line(
            pivot, pb1(tracker.get_value()),
            color=GOLD_BRIGHT, stroke_width=2.5, stroke_opacity=0.7
        ))
        rod_b2 = always_redraw(lambda: Line(
            pb1(tracker.get_value()), pb2(tracker.get_value()),
            color=GOLD_BRIGHT, stroke_width=2.5, stroke_opacity=0.7
        ))

        pivot_dot = Dot(pivot, color=WHITE, radius=0.08)

        # ── Glow bobs ─────────────────────────────────────────
        def make_glow(pos_fn, core, halo):
            return always_redraw(lambda: VGroup(
                Circle(radius=0.32, color=halo,
                       fill_opacity=0.04, stroke_width=0)
                    .move_to(pos_fn(tracker.get_value())),
                Circle(radius=0.20, color=halo,
                       fill_opacity=0.10, stroke_width=0)
                    .move_to(pos_fn(tracker.get_value())),
                Circle(radius=0.12, color=core,
                       fill_opacity=0.28, stroke_width=0)
                    .move_to(pos_fn(tracker.get_value())),
                Dot(pos_fn(tracker.get_value()),
                    color=core, radius=0.09, fill_opacity=1),
            ))

        glow_a = make_glow(pa2, CYAN_BRIGHT, TEAL_BRIGHT)
        glow_b = make_glow(pb2, GOLD_BRIGHT, ORANGE_GLOW)

        # ── Tails ─────────────────────────────────────────────
        raw_a = np.array([pa2(ti) for ti in sol_a.t])
        raw_b = np.array([pb2(ti) for ti in sol_b.t])

        mask_a = ((raw_a[:,0]>=-6.8)&(raw_a[:,0]<=6.8)&
                  (raw_a[:,1]>=-3.8)&(raw_a[:,1]<=3.8))
        mask_b = ((raw_b[:,0]>=-6.8)&(raw_b[:,0]<=6.8)&
                  (raw_b[:,1]>=-3.8)&(raw_b[:,1]<=3.8))

        cpts_a = raw_a[mask_a];  ctim_a = sol_a.t[mask_a]
        cpts_b = raw_b[mask_b];  ctim_b = sol_b.t[mask_b]

        def make_tail(cpts, ctim, color):
            def _tail():
                cur = tracker.get_value()
                idx = max(2, min(int(np.searchsorted(ctim, cur))+1, len(cpts)))
                mob = VMobject(stroke_width=2, stroke_opacity=0.7)
                mob.set_stroke(color=color)
                mob.set_points_smoothly(list(cpts[:idx]))
                return mob
            return always_redraw(_tail)

        tail_a = make_tail(cpts_a, ctim_a, CYAN_BRIGHT)
        tail_b = make_tail(cpts_b, ctim_b, GOLD_BRIGHT)

        # ── Distance graph (bottom strip) ─────────────────────
        dist_arr = np.linalg.norm(raw_a - raw_b, axis=1)
        dist_fn  = interp1d(sol_a.t, dist_arr)

        axes = Axes(
            x_range=[0, t_max, 5],
            y_range=[0, max(dist_arr)*1.1, 1],
            x_length=8, y_length=1.6,
            axis_config={"include_tip": False,
                         "stroke_color": GREY, "stroke_width": 1}
        ).to_edge(DOWN, buff=0.15)

        x_lbl = axes.get_x_axis_label(
            MathTex("t", font_size=20), direction=RIGHT
        )
        y_lbl = axes.get_y_axis_label(
            MathTex(r"\Delta r", font_size=20), direction=UP
        )

        dist_trace = always_redraw(lambda: axes.plot(
            lambda t: float(dist_fn(min(t, t_max-0.01))),
            x_range=[0, max(0.01, tracker.get_value())],
            color=RED, stroke_width=2
        ))

        # ── Labels ────────────────────────────────────────────
        title = Text("Sensitive Dependence on Initial Conditions",
                     font_size=26, color=GOLD_BRIGHT).to_edge(UP, buff=0.2)

        ic_lbl = VGroup(
            MathTex(r"\theta_1^{(A)} = 0.9500\pi",
                    font_size=20, color=CYAN_BRIGHT),
            MathTex(r"\theta_1^{(B)} = 0.9501\pi",
                    font_size=20, color=GOLD_BRIGHT),
        ).arrange(DOWN, buff=0.15).to_corner(UL).shift(DOWN*0.8)

        diff_lbl = MathTex(
            r"\Delta\theta_1 = 0.0001\pi \approx 0.018°",
            font_size=20, color=GREY
        ).next_to(ic_lbl, DOWN, buff=0.15)

        dist_title = Text("Distance between bobs",
                          font_size=18, color=GREY)\
                         .next_to(axes, UP, buff=0.1)

        # ── Build ─────────────────────────────────────────────
        self.play(Write(title))
        self.play(
            Write(ic_lbl), Write(diff_lbl),
            run_time=1.0
        )
        self.play(
            FadeIn(pivot_dot),
            FadeIn(rod_a1), FadeIn(rod_a2),
            FadeIn(rod_b1), FadeIn(rod_b2),
            FadeIn(glow_a), FadeIn(glow_b),
            FadeIn(axes), FadeIn(x_lbl), FadeIn(y_lbl),
            FadeIn(dist_title),
        )
        self.add(tail_a, tail_b, dist_trace)
        self.wait(0.3)

        self.play(
            tracker.animate.set_value(t_max),
            run_time=20,
            rate_func=linear
        )
        self.wait(0.5)

        end = Text(
            "Same equations. 0.018° difference. Completely different futures.",
            font_size=22, color=GOLD_BRIGHT
        ).to_edge(DOWN, buff=0.1)
        self.play(FadeOut(dist_title), FadeOut(axes),
                  FadeOut(x_lbl), FadeOut(y_lbl))
        self.play(Write(end))
        self.wait(3)