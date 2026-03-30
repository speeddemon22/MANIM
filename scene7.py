from manim import *
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d


GOLD_BRIGHT  = "#FFD700"
ORANGE_GLOW  = "#FF6B00"
CYAN_BRIGHT  = "#00FFFF"
TEAL_BRIGHT  = "#00E5CC"
WHITE_SOFT   = "#E8E8E8"


class Scene7DoublePendulum(Scene):
    def construct(self):

        # ════════════════════════════════════════════════════
        # ACT 1: TOP = diagram, BOTTOM = equations
        # ════════════════════════════════════════════════════

        title = Text("Double Pendulum", font_size=34,
                     color=GOLD_BRIGHT).to_edge(UP, buff=0.2)
        self.play(Write(title))
        self.wait(0.2)

        # horizontal divider
        h_line = Line(LEFT*7, RIGHT*7, color=GREY, stroke_opacity=0.3)\
                     .move_to(UP*0.3)

        # ── TOP HALF: diagram centered ────────────────────────
        d_pivot      = np.array([0, 2.5, 0])
        d_L          = 1.1
        th1_d, th2_d = 0.55, 1.0
        d_p1 = d_pivot + np.array([d_L*np.sin(th1_d), -d_L*np.cos(th1_d), 0])
        d_p2 = d_p1    + np.array([d_L*np.sin(th2_d), -d_L*np.cos(th2_d), 0])

        ref1 = DashedLine(d_pivot, d_pivot + DOWN*1.6,
                          color=GREY, stroke_opacity=0.5, dash_length=0.1)
        ref2 = DashedLine(d_p1,    d_p1    + DOWN*1.6,
                          color=GREY, stroke_opacity=0.5, dash_length=0.1)

        d_rod1 = Line(d_pivot, d_p1, color=WHITE_SOFT, stroke_width=4)
        d_rod2 = Line(d_p1,    d_p2, color=WHITE_SOFT, stroke_width=4)
        d_dot0 = Dot(d_pivot, color=WHITE,       radius=0.08)
        d_dot1 = Dot(d_p1,    color=CYAN_BRIGHT, radius=0.13)
        d_dot2 = Dot(d_p2,    color=GOLD_BRIGHT, radius=0.13)

        arc1 = Arc(radius=0.38, start_angle=-PI/2, angle=th1_d,
                   color=GOLD_BRIGHT).move_arc_center_to(d_pivot)
        arc2 = Arc(radius=0.38, start_angle=-PI/2, angle=th2_d,
                   color=GOLD_BRIGHT).move_arc_center_to(d_p1)

        lbl_th1 = MathTex(r"\theta_1", font_size=26, color=GOLD_BRIGHT)\
                      .next_to(arc1, RIGHT, buff=0.07)
        lbl_th2 = MathTex(r"\theta_2", font_size=26, color=GOLD_BRIGHT)\
                      .next_to(arc2, RIGHT, buff=0.07)
        lbl_L1  = MathTex(r"L_1,\,m_1", font_size=22, color=CYAN_BRIGHT)\
                      .next_to((d_pivot+d_p1)/2, LEFT, buff=0.1)
        lbl_L2  = MathTex(r"L_2,\,m_2", font_size=22, color=GOLD_BRIGHT)\
                      .next_to((d_p1+d_p2)/2,    LEFT, buff=0.1)

        diagram = VGroup(
            ref1, ref2, d_rod1, d_rod2,
            d_dot0, d_dot1, d_dot2,
            arc1, arc2,
            lbl_th1, lbl_th2, lbl_L1, lbl_L2,
        )

        # ── BOTTOM HALF: two equations side by side ───────────
        # ── BOTTOM HALF: equations stacked vertically ─────────
        eq1 = MathTex(
            r"\ddot{\theta}_1 = \frac{"
            r"-g(2m_1+m_2)\sin\theta_1"
            r"- m_2 g\sin(\theta_1-2\theta_2)"
            r"- 2\sin\delta\,m_2(\dot{\theta}_2^2 L_2"
            r"+\dot{\theta}_1^2 L_1\cos\delta)}"
            r"{L_1(2m_1+m_2-m_2\cos 2\delta)}",
            font_size=22, color=CYAN_BRIGHT
        ).move_to(DOWN * 1.2)

        eq2 = MathTex(
            r"\ddot{\theta}_2 = \frac{"
            r"2\sin\delta\,("
            r"\dot{\theta}_1^2 L_1(m_1+m_2)"
            r"+g(m_1+m_2)\cos\theta_1"
            r"+\dot{\theta}_2^2 L_2 m_2\cos\delta)}"
            r"{L_2(2m_1+m_2-m_2\cos 2\delta)}",
            font_size=22, color=ORANGE_GLOW
        ).move_to(DOWN * 2.5)

        delta_def = MathTex(r"\delta = \theta_1 - \theta_2",
                            font_size=22, color=GREY)\
                        .move_to(DOWN * 3.4)

        # Remove v_line — no longer needed
        
        delta_def = MathTex(r"\delta = \theta_1 - \theta_2",
                            font_size=22, color=GREY)\
                        .move_to(DOWN*3.2)

        self.play(Create(h_line))
        self.play(FadeIn(diagram), run_time=1.0)
        self.wait(0.3)
        self.play(Write(eq1), run_time=1.5)
        self.wait(0.2)
        self.play(Write(eq2), run_time=1.5)
        self.wait(0.2)
        self.play(Write(delta_def))
        self.wait(2.0)


        

        # ── Wipe ─────────────────────────────────────────────
        self.play(
            FadeOut(title), FadeOut(h_line),
            FadeOut(diagram), FadeOut(eq1), FadeOut(eq2), FadeOut(delta_def),
            run_time=1.0
        )

     
        m1, m2 = 1.0, 1.0
        L1, L2 = 1.2, 1.2
        g      = 9.8
        t_max  = 20
        t_eval = np.linspace(0, t_max, 6000)

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

        ic  = [np.pi*0.95, 0.0, np.pi*0.62, 0.0]
        sol = solve_ivp(double_pendulum, (0, t_max), ic,
                        t_eval=t_eval, method='DOP853',
                        rtol=1e-10, atol=1e-12)

        th1_fn = interp1d(sol.t, sol.y[0])
        th2_fn = interp1d(sol.t, sol.y[2])

        pivot = np.array([0.0, 1.2, 0])

        def pos1(time):
            tt = min(time, t_max - 0.01)
            return pivot + np.array([L1*np.sin(th1_fn(tt)),
                                     -L1*np.cos(th1_fn(tt)), 0])

        def pos2(time):
            tt = min(time, t_max - 0.01)
            return pos1(time) + np.array([L2*np.sin(th2_fn(tt)),
                                          -L2*np.cos(th2_fn(tt)), 0])

        tracker = ValueTracker(0)

        rod1 = always_redraw(lambda: Line(
            pivot, pos1(tracker.get_value()),
            color=WHITE_SOFT, stroke_width=3, stroke_opacity=0.85
        ))
        rod2 = always_redraw(lambda: Line(
            pos1(tracker.get_value()), pos2(tracker.get_value()),
            color=WHITE_SOFT, stroke_width=3, stroke_opacity=0.85
        ))

        pivot_dot = Dot(pivot, color=WHITE, radius=0.08)
        joint     = always_redraw(lambda: Dot(
            pos1(tracker.get_value()), color=WHITE, radius=0.07
        ))

        def make_glow(pos_fn, core_color, halo_color):
            return always_redraw(lambda: VGroup(
                Circle(radius=0.35, color=halo_color,
                       fill_opacity=0.04, stroke_width=0)
                    .move_to(pos_fn(tracker.get_value())),
                Circle(radius=0.22, color=halo_color,
                       fill_opacity=0.10, stroke_width=0)
                    .move_to(pos_fn(tracker.get_value())),
                Circle(radius=0.13, color=core_color,
                       fill_opacity=0.30, stroke_width=0)
                    .move_to(pos_fn(tracker.get_value())),
                Dot(pos_fn(tracker.get_value()),
                    color=core_color, radius=0.10, fill_opacity=1),
            ))

        glow1 = make_glow(pos1, CYAN_BRIGHT, TEAL_BRIGHT)
        glow2 = make_glow(pos2, GOLD_BRIGHT, ORANGE_GLOW)

        # ── always_redraw tail — zero lag ─────────────────────
        raw_pts      = np.array([pos2(ti) for ti in sol.t])
        mask         = (
            (raw_pts[:, 0] >= -6.8) & (raw_pts[:, 0] <= 6.8) &
            (raw_pts[:, 1] >= -3.8) & (raw_pts[:, 1] <= 3.8)
        )
        clipped_pts  = raw_pts[mask]
        clipped_time = sol.t[mask]

        def make_tail():
            current = tracker.get_value()
            idx = int(np.searchsorted(clipped_time, current))
            idx = max(2, min(idx + 1, len(clipped_pts)))
            mob = VMobject(stroke_width=2.5, stroke_opacity=0.85)
            mob.set_color_by_gradient(GOLD_BRIGHT, ORANGE_GLOW, RED)
            mob.set_points_smoothly(list(clipped_pts[:idx]))
            return mob

        tail = always_redraw(make_tail)

        sim_title = Text("Two equations. Completely irregular motion.",
                         font_size=24, color=GOLD_BRIGHT).to_edge(UP, buff=0.3)

        self.play(
            FadeIn(pivot_dot),
            FadeIn(rod1), FadeIn(rod2),
            FadeIn(joint),
            FadeIn(glow1), FadeIn(glow2),
            Write(sim_title),
        )
        self.add(tail)
        self.wait(0.3)

        self.play(
            tracker.animate.set_value(t_max),
            run_time=20,
            rate_func=linear
        )
        self.wait(3)