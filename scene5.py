from manim import *
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d


class Scene5NonlinearPendulum(Scene):
    def construct(self):
        L, g, t_max = 1.8, 9.8, 12
        t_eval = np.linspace(0, t_max, 2000)
        A_s, A_l = 0.17, 1.40

        sol_s = solve_ivp(lambda t, y: [y[1], -(g / L) * np.sin(y[0])],
                          (0, t_max), [A_s, 0], t_eval=t_eval)
        sol_l = solve_ivp(lambda t, y: [y[1], -(g / L) * np.sin(y[0])],
                          (0, t_max), [A_l, 0], t_eval=t_eval)

        th_s = interp1d(sol_s.t, sol_s.y[0])
        th_l = interp1d(sol_l.t, sol_l.y[0])

        # ── Compute actual periods from simulation ───────────
        def compute_period(y0, t_arr):
            crossings = []
            for i in range(1, len(t_arr)):
                if y0[i - 1] < 0 and y0[i] >= 0:
                    t_cross = t_arr[i - 1] + (0 - y0[i - 1]) * \
                              (t_arr[i] - t_arr[i - 1]) / (y0[i] - y0[i - 1])
                    crossings.append(t_cross)
                if len(crossings) == 2:
                    break
            return crossings[1] - crossings[0]

        T_s = compute_period(sol_s.y[0], sol_s.t)
        T_l = compute_period(sol_l.y[0], sol_l.t)

        t = ValueTracker(0)

        # ── Pendulums ─────────────────────────────────────────
        piv_s = np.array([-2.8, 2.2, 0])
        piv_l = np.array([ 2.8, 2.2, 0])

        def bpos(piv, fn):
            th = fn(min(t.get_value(), t_max - 0.01))
            return piv + np.array([L * np.sin(th), -L * np.cos(th), 0])

        pivot_s = Dot(piv_s, color=WHITE, radius=0.07)
        pivot_l = Dot(piv_l, color=WHITE, radius=0.07)

        bob_s = always_redraw(lambda: Dot(bpos(piv_s, th_s), color=BLUE, radius=0.20))
        bob_l = always_redraw(lambda: Dot(bpos(piv_l, th_l), color=RED,  radius=0.20))
        rod_s = always_redraw(lambda: Line(piv_s, bpos(piv_s, th_s), color=BLUE, stroke_width=4))
        rod_l = always_redraw(lambda: Line(piv_l, bpos(piv_l, th_l), color=RED,  stroke_width=4))

        lbl_s = Text("θ₀ = 10°", color=BLUE, font_size=26).next_to(piv_s, UP, buff=0.15)
        lbl_l = Text("θ₀ = 80°", color=RED,  font_size=26).next_to(piv_l, UP, buff=0.15)

        # ── Graph (both normalized to amplitude 1) ───────────
        axes = Axes(
            x_range=[0, t_max, 2],
            y_range=[-1.2, 1.2, 1],
            x_length=10, y_length=2.4,
            axis_config={"include_tip": False}
        ).shift(DOWN * 3.0)

        x_lbl = axes.get_x_axis_label("t",                direction=RIGHT)
        y_lbl = axes.get_y_axis_label(r"\theta/\theta_0", direction=UP, buff=0.15)

        trace_s = TracedPath(
            lambda: axes.c2p(t.get_value(),
                             th_s(min(t.get_value(), t_max - 0.01)) / A_s),
            stroke_color=BLUE, stroke_width=3
        )
        trace_l = TracedPath(
            lambda: axes.c2p(t.get_value(),
                             th_l(min(t.get_value(), t_max - 0.01)) / A_l),
            stroke_color=RED, stroke_width=3
        )

        title   = Text("Same equation — larger amplitude → longer period",
                       font_size=26).to_edge(UP)
        divider = DashedLine(UP * 2.5, DOWN * 1.5, color=GREY, stroke_opacity=0.3)

        # ── Build scene ───────────────────────────────────────
        self.play(Write(title))
        self.play(
            Create(divider),
            FadeIn(pivot_s), FadeIn(pivot_l),
            FadeIn(lbl_s),   FadeIn(lbl_l),
            FadeIn(bob_s),   FadeIn(bob_l),
            FadeIn(rod_s),   FadeIn(rod_l),
            FadeIn(axes), FadeIn(x_lbl), FadeIn(y_lbl),
        )
        self.add(trace_s, trace_l)
        self.wait(0.3)
        self.play(t.animate.set_value(t_max), run_time=12, rate_func=linear)
        self.wait(0.5)

        # ── Peak markers (computed from real periods) ─────────
        peak_markers = VGroup()
        y_top = axes.c2p(0,  1.1)[1]
        y_bot = axes.c2p(0, -1.1)[1]

        n = 1
        while n * T_s <= t_max:
            x = axes.c2p(n * T_s, 0)[0]
            peak_markers.add(
                DashedLine([x, y_bot, 0], [x, y_top, 0],
                           color=BLUE, stroke_width=2, dash_length=0.12)
            )
            n += 1

        n = 1
        while n * T_l <= t_max:
            x = axes.c2p(n * T_l, 0)[0]
            peak_markers.add(
                DashedLine([x, y_bot, 0], [x, y_top, 0],
                           color=RED, stroke_width=2, dash_length=0.12)
            )
            n += 1

        self.play(Create(peak_markers), run_time=1.0)

        # ── Period labels ─────────────────────────────────────
        period_lbl_s = MathTex(f"T_{{\\text{{blue}}}} = {T_s:.2f}\\,s",
                               color=BLUE, font_size=26) \
                           .next_to(axes, DOWN, buff=0.25).shift(LEFT * 2.5)
        period_lbl_l = MathTex(f"T_{{\\text{{red}}}} = {T_l:.2f}\\,s",
                               color=RED, font_size=26) \
                           .next_to(axes, DOWN, buff=0.25).shift(RIGHT * 2.5)

        self.play(Write(period_lbl_s), Write(period_lbl_l))
        self.wait(0.5)

        verdict = MathTex(
            r"\sin\theta \neq \theta \;\Rightarrow\; T \text{ depends on amplitude}",
            color=YELLOW, font_size=28
        ).to_edge(DOWN, buff=3)
        self.play(Write(verdict))
        self.wait(3)