from manim import *
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d


class Superposition(MovingCameraScene):
    def construct(self):
        lwall  = -6
        rwall  =  6
        eqm1   = -3
        eqm2   =  3
        omega1 = 2.0
        omega2 = 2.0
        kc     = 0.3
        mass   = 1
        C      = 0.5
        t_snap = 3.04
        amp    = 1.5

        def equations(t, state):
            x1, v1, x2, v2 = state
            ax1 = -omega1**2 * (x1 - eqm1) + (kc/mass) * (x2 - x1 - (eqm2 - eqm1))
            ax2 = -omega2**2 * (x2 - eqm2) + (kc/mass) * (x1 - x2 + (eqm2 - eqm1))
            return [v1, ax1, v2, ax2]

        sol    = solve_ivp(equations, (0, 12), [eqm1 + 1.5, 0, eqm2,       0], t_eval=np.linspace(0, 12, 1000))
        sol_m1 = solve_ivp(equations, (0, 12), [eqm1 + 1.5, 0, eqm2 + 1.5, 0], t_eval=np.linspace(0, 12, 1000))
        sol_m2 = solve_ivp(equations, (0, 12), [eqm1 + 1.5, 0, eqm2 - 1.5, 0], t_eval=np.linspace(0, 12, 1000))

        x1_actual = interp1d(sol.t,    sol.y[0])
        x2_actual = interp1d(sol.t,    sol.y[2])
        x1_m1     = interp1d(sol_m1.t, sol_m1.y[0])
        x1_m2     = interp1d(sol_m2.t, sol_m2.y[0])

        t = ValueTracker(0)

        wall_left  = Line([lwall, 2.5, 0], [lwall, 0.5, 0], color=GREY)
        wall_right = Line([rwall, 2.5, 0], [rwall, 0.5, 0], color=GREY)

        mass1 = always_redraw(lambda: Square(0.6, fill_color=BLUE,  fill_opacity=1).move_to([x1_actual(t.get_value()), 1.5, 0]))
        mass2 = always_redraw(lambda: Square(0.6, fill_color=GREEN, fill_opacity=1).move_to([x2_actual(t.get_value()), 1.5, 0]))
        label1 = always_redraw(lambda: MathTex("m_1").next_to(mass1, UP, buff=0.2))
        label2 = always_redraw(lambda: MathTex("m_2").next_to(mass2, UP, buff=0.2))

        def make_spring(x_start, x_end, color=YELLOW):
            pts, n = [], 8
            dx = (x_end - x_start) / (2*n + 2)
            pts.append([x_start, 1.5, 0])
            pts.append([x_start + dx, 1.5, 0])
            for i in range(1, 2*n + 1):
                pts.append([x_start + dx*(i+1), 1.75 if i % 2 == 1 else 1.25, 0])
            pts.append([x_end, 1.5, 0])
            return VMobject(color=color).set_points_as_corners(pts)

        left_spring   = always_redraw(lambda: make_spring(lwall,                    x1_actual(t.get_value()), color=YELLOW))
        middle_spring = always_redraw(lambda: make_spring(x1_actual(t.get_value()), x2_actual(t.get_value()), color=GREEN))
        right_spring  = always_redraw(lambda: make_spring(x2_actual(t.get_value()), rwall,                    color=YELLOW))
        label_k_left  = always_redraw(lambda: MathTex("k",   color=YELLOW).move_to([(lwall + x1_actual(t.get_value())) / 2,                   2.0, 0]))
        label_kc      = always_redraw(lambda: MathTex("k_c", color=GREEN ).move_to([(x1_actual(t.get_value()) + x2_actual(t.get_value())) / 2, 2.0, 0]))
        label_k_right = always_redraw(lambda: MathTex("k",   color=YELLOW).move_to([(x2_actual(t.get_value()) + rwall) / 2,                   2.0, 0]))

        axes = Axes(
            x_range=[0, 12, 4], y_range=[-2.5, 2.5, 1],
            x_length=12, y_length=2,
        ).shift(DOWN * 2.5)

        def trace1_pos():
            time = t.get_value()
            return axes.c2p(time, x1_actual(time) - eqm1)
        def trace2_pos():
            time = t.get_value()
            return axes.c2p(time, x2_actual(time) - eqm2)
        def trace_mode1_pos():
            time = t.get_value()
            return axes.c2p(time, C * (x1_m1(time) - eqm1))
        def trace_mode2_pos():
            time = t.get_value()
            return axes.c2p(time, C * (x1_m2(time) - eqm1))

        trace1      = TracedPath(trace1_pos,      stroke_color=BLUE,   stroke_width=2)
        trace2      = TracedPath(trace2_pos,      stroke_color=GREEN,  stroke_width=2)
        trace_mode1 = TracedPath(trace_mode1_pos, stroke_color=YELLOW, stroke_width=1.5, stroke_opacity=0.6)
        trace_mode2 = TracedPath(trace_mode2_pos, stroke_color=RED,    stroke_width=1.5, stroke_opacity=0.6)

        x_label = axes.get_x_axis_label("t",    direction=RIGHT)
        y_label = axes.get_y_axis_label("x(t)", direction=UP)
        legend1 = MathTex("m_1",     color=BLUE  ).to_corner(DL).shift(UP * 1.0)
        legend2 = MathTex("m_2",     color=GREEN ).to_corner(DL).shift(UP * 0.5)
        legend3 = MathTex("A_1 q_1", color=YELLOW).to_corner(DR).shift(UP * 2.0)
        legend4 = MathTex("A_2 q_2", color=RED   ).to_corner(DR).shift(UP * 1.5)
        eq = MathTex("x(t) = A_1 q_1(t) + A_2 q_2(t)", font_size=36).to_edge(DOWN)

        title = Text("General Motion as Superposition", font_size=28).to_edge(UP)
        self.play(Write(title))
        self.play(Create(wall_left), Create(wall_right))
        self.play(
            FadeIn(mass1), FadeIn(mass2),
            FadeIn(left_spring), FadeIn(middle_spring), FadeIn(right_spring),
            FadeIn(label1), FadeIn(label2),
            FadeIn(label_k_left), FadeIn(label_kc), FadeIn(label_k_right),
            FadeIn(axes), FadeIn(x_label), FadeIn(y_label),
            FadeIn(legend1), FadeIn(legend2), FadeIn(legend3), FadeIn(legend4)
        )
        self.wait(0.5)
        self.play(Write(eq))
        self.wait(0.5)

        self.add(trace1, trace2, trace_mode1, trace_mode2)
        self.play(t.animate.set_value(t_snap), run_time=t_snap, rate_func=linear)
        v1_val = C * (x1_m1(t_snap) - eqm1)   # 0.735
        v2_val = C * (x1_m2(t_snap) - eqm1)   # 0.729
        vt_val = x1_actual(t_snap) - eqm1      # 1.464
        base_y    = -0.8
        chain_x   = -1.2
        result_x  =  1.2

        p_base_chain  = np.array([chain_x,  base_y, 0])
        p_mid_chain   = np.array([chain_x,  base_y + v1_val * amp, 0])
        p_top_chain   = np.array([chain_x,  base_y + (v1_val + v2_val) * amp, 0])
        p_base_result = np.array([result_x, base_y, 0])
        p_top_result  = np.array([result_x, base_y + vt_val * amp, 0])

        # Background booooxxxxxx
        panel_box = SurroundingRectangle(
            VGroup(
                Dot(p_base_chain + LEFT * 0.8),
                Dot(p_top_result + UP * 0.3 + RIGHT * 0.8)
            ),
            color=DARK_GREY, fill_color=BLACK, fill_opacity=0.8, buff=0.2
        )
        snap_line = DashedLine(
            axes.c2p(t_snap, -2.5), axes.c2p(t_snap, 2.5),
            color=WHITE, dash_length=0.08
        )
        arr_v1 = Arrow(p_base_chain, p_mid_chain,  color=YELLOW, buff=0, max_tip_length_to_length_ratio=0.12)
        arr_v2 = Arrow(p_mid_chain,  p_top_chain,  color=RED,    buff=0, max_tip_length_to_length_ratio=0.12)
        arr_vt = Arrow(p_base_result, p_top_result, color=BLUE, buff=0,
                       max_tip_length_to_length_ratio=0.08, stroke_width=5)

   
        lbl_v1 = MathTex("A_1 q_1", color=YELLOW, font_size=28).next_to(arr_v1, LEFT,  buff=0.15)
        lbl_v2 = MathTex("A_2 q_2", color=RED, font_size=28).next_to(arr_v2, LEFT,  buff=0.15)
        lbl_vt = MathTex("x(t)",  color=BLUE, font_size=28).next_to(arr_vt, RIGHT, buff=0.15)

        lbl_plus = MathTex("+", color=WHITE, font_size=36).move_to(
            (p_mid_chain + p_base_chain) / 2 + RIGHT * 0.4
        )
        lbl_eq = MathTex("=", color=WHITE, font_size=36).move_to(
            np.array([0, base_y + vt_val * amp / 2, 0])
        )

        # Dashed horizontal lines showing same base and same top
        base_connect = DashedLine(
            p_base_chain + LEFT * 0.1,
             p_base_result + RIGHT * 0.1,
             color=GREY, dash_length=0.1, stroke_opacity=0.5
        )
        top_connect = DashedLine(
            p_top_chain  + LEFT * 0.1,
            p_top_result + RIGHT * 0.1,
            color=GREY, dash_length=0.1, stroke_opacity=0.5
        )
        self.play(FadeOut(eq), run_time=0.5)
        self.play(Create(snap_line))
        self.play(FadeIn(panel_box))
        self.play(GrowArrow(arr_v1), Write(lbl_v1), run_time=0.9)
        self.wait(0.2)
        self.play(Write(lbl_plus))
        self.play(GrowArrow(arr_v2), Write(lbl_v2), run_time=0.9)
        self.wait(0.3)
        self.play(Create(base_connect), Create(top_connect), run_time=0.5)
        self.play(Write(lbl_eq))
        self.play(GrowArrow(arr_vt), Write(lbl_vt), run_time=0.9)
        self.play(Indicate(arr_vt, color=WHITE, scale_factor=1.15))
        self.wait(1.5)
        self.play(
            FadeOut(panel_box), FadeOut(snap_line),
            FadeOut(arr_v1), FadeOut(arr_v2), FadeOut(arr_vt),
            FadeOut(lbl_v1), FadeOut(lbl_v2), FadeOut(lbl_vt),
            FadeOut(lbl_plus), FadeOut(lbl_eq),
            FadeOut(base_connect), FadeOut(top_connect),
            run_time=1.0
        )
        self.wait(0.3)
        self.play(t.animate.set_value(12), run_time=12 - t_snap, rate_func=linear)