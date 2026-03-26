from manim import *
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d


class NormalModes(Scene):
    def construct(self):
        lwall = -6
        rwall = 6
        eqm1 = -3
        eqm2 = 3
        omega1 = 2.0
        omega2 = 2.0
        kc = 0.3
        mass = 1

        def equations(t, state):
            x1, v1, x2, v2 = state
            ax1 = -omega1**2 * (x1 - eqm1) + (kc/mass) * (x2 - x1 - (eqm2 - eqm1))
            ax2 = -omega2**2 * (x2 - eqm2) + (kc/mass) * (x1 - x2 + (eqm2 - eqm1))
            return [v1, ax1, v2, ax2]

        sol1 = solve_ivp(equations, (0, 12), [eqm1 + 1.5, 0, eqm2 + 1.5, 0], t_eval=np.linspace(0, 12, 1000))
        x1_m1 = interp1d(sol1.t, sol1.y[0])
        x2_m1 = interp1d(sol1.t, sol1.y[2])

        sol2 = solve_ivp(equations, (0, 12), [eqm1 + 1.5, 0, eqm2 - 1.5, 0], t_eval=np.linspace(0, 12, 1000))
        x1_m2 = interp1d(sol2.t, sol2.y[0])
        x2_m2 = interp1d(sol2.t, sol2.y[2])

        current_mode = [1]

        def get_x1(time):
            return x1_m1(time) if current_mode[0] == 1 else x1_m2(time)

        def get_x2(time):
            return x2_m1(time) if current_mode[0] == 1 else x2_m2(time)

        t = ValueTracker(0)

        wall_left  = Line([lwall, 2.5, 0], [lwall, 0.5, 0], color=GREY)
        wall_right = Line([rwall, 2.5, 0], [rwall, 0.5, 0], color=GREY)

        mass1 = always_redraw(lambda: Square(0.6, fill_color=BLUE, fill_opacity=1).move_to([get_x1(t.get_value()), 1.5, 0]))
        mass2 = always_redraw(lambda: Square(0.6, fill_color=GREEN, fill_opacity=1).move_to([get_x2(t.get_value()), 1.5, 0]))

        label1 = always_redraw(lambda: MathTex("m_1").next_to(mass1, UP, buff=0.2))
        label2 = always_redraw(lambda: MathTex("m_2").next_to(mass2, UP, buff=0.2))

        def make_spring(x_start, x_end, color=YELLOW):
            pts = []
            n = 8
            dx = (x_end - x_start) / (2*n + 2)
            pts.append([x_start, 1.5, 0])
            pts.append([x_start + dx, 1.5, 0])
            for i in range(1, 2*n + 1):
                y = 1.75 if i % 2 == 1 else 1.25
                pts.append([x_start + dx*(i+1), y, 0])
            pts.append([x_end, 1.5, 0])
            return VMobject(color=color).set_points_as_corners(pts)

        left_spring   = always_redraw(lambda: make_spring(lwall, get_x1(t.get_value()), color=YELLOW))
        middle_spring = always_redraw(lambda: make_spring(get_x1(t.get_value()), get_x2(t.get_value()), color=GREEN))
        right_spring  = always_redraw(lambda: make_spring(get_x2(t.get_value()), rwall, color=YELLOW))

        label_k_left  = always_redraw(lambda: MathTex("k", color=YELLOW).move_to([(lwall + get_x1(t.get_value())) / 2, 2.0, 0]))
        label_kc      = always_redraw(lambda: MathTex("k_c", color=GREEN).move_to([(get_x1(t.get_value()) + get_x2(t.get_value())) / 2, 2.0, 0]))
        label_k_right = always_redraw(lambda: MathTex("k", color=YELLOW).move_to([(get_x2(t.get_value()) + rwall) / 2, 2.0, 0]))

        axes = Axes(
            x_range=[0, 12, 4],
            y_range=[-2.5, 2.5, 1],
            x_length=12,
            y_length=2,
        ).shift(DOWN * 2.5)

        def trace1_pos():
            time = t.get_value()
            return axes.c2p(time, get_x1(time) - eqm1)

        def trace2_pos():
            time = t.get_value()
            return axes.c2p(time, get_x2(time) - eqm2)

        x_label = axes.get_x_axis_label("t", direction=RIGHT)
        y_label = axes.get_y_axis_label("x(t)", direction=UP)
        legend1 = MathTex("m_1", color=BLUE).to_corner(DL).shift(UP * 1)
        legend2 = MathTex("m_2", color=GREEN).to_corner(DL).shift(UP * 0.5)

        
        title = Text("Normal Mode 1 — In Phase", font_size=28).to_edge(UP)
        self.play(Write(title))
        self.play(Create(wall_left), Create(wall_right))
        self.play(
            FadeIn(mass1), FadeIn(mass2),
            FadeIn(left_spring), FadeIn(middle_spring), FadeIn(right_spring),
            FadeIn(label1), FadeIn(label2),
            FadeIn(label_k_left), FadeIn(label_kc), FadeIn(label_k_right),
            FadeIn(axes), FadeIn(x_label), FadeIn(y_label),
            FadeIn(legend1), FadeIn(legend2)
        )
        self.wait(0.5)

        trace1 = TracedPath(trace1_pos, stroke_color=BLUE, stroke_width=2)
        trace2 = TracedPath(trace2_pos, stroke_color=GREEN, stroke_width=2)
        self.add(trace1, trace2)
        self.play(t.animate.set_value(12), run_time=12, rate_func=linear)

        
        self.play(FadeOut(trace1), FadeOut(trace2))
        self.play(Transform(title, Text("Normal Mode 2 — Out of Phase", font_size=28).to_edge(UP)))
        current_mode[0] = 2
        t.set_value(0)

        trace1 = TracedPath(trace1_pos, stroke_color=BLUE, stroke_width=2)
        trace2 = TracedPath(trace2_pos, stroke_color=GREEN, stroke_width=2)
        self.add(trace1, trace2)
        self.play(t.animate.set_value(12), run_time=12, rate_func=linear)