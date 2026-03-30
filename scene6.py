from manim import *
import numpy as np


class Scene6EnterChaos(Scene):
    def construct(self):

        # ── Act 1: What we've seen so far ─────────────────────
        line1 = Text("So far:", font_size=36, color=GREY).to_edge(UP, buff=1.2)
        self.play(FadeIn(line1))
        self.wait(0.3)

        step1 = MathTex(
            r"\text{Linear oscillator} \;\rightarrow\; \text{predictable, perfect sine}",
            font_size=34, color=BLUE
        ).next_to(line1, DOWN, buff=0.5)
        self.play(Write(step1))
        self.wait(0.6)

        step2 = MathTex(
            r"\text{Coupled oscillators} \;\rightarrow\; \text{normal modes, beats}",
            font_size=34, color=GREEN
        ).next_to(step1, DOWN, buff=0.4)
        self.play(Write(step2))
        self.wait(0.6)

        step3 = MathTex(
            r"\text{Nonlinear pendulum} \;\rightarrow\; \text{amplitude warps the period}",
            font_size=34, color=YELLOW
        ).next_to(step2, DOWN, buff=0.4)
        self.play(Write(step3))
        self.wait(1.0)

        # ── Act 2: The question ───────────────────────────────
        question = Text(
            "What happens if we add one more degree of freedom?",
            font_size=30, color=WHITE
        ).next_to(step3, DOWN, buff=0.7)

        self.play(Write(question))
        self.wait(1.2)

        # ── Act 3: Dramatic answer ────────────────────────────
        self.play(
            FadeOut(line1), FadeOut(step1),
            FadeOut(step2), FadeOut(step3),
            FadeOut(question),
            run_time=1.0
        )

        chaos_word = Text("Chaos.", font_size=96, color=RED, weight=BOLD)\
                         .move_to(ORIGIN)
        self.play(Write(chaos_word), run_time=1.5)
        self.wait(0.8)

        sub = Text(
            "deterministic equations  ·  unpredictable motion",
            font_size=26, color=GREY
        ).next_to(chaos_word, DOWN, buff=0.4)
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(1.0)

        # ── Act 4: The ingredients ────────────────────────────
        self.play(FadeOut(chaos_word), FadeOut(sub))

        recipe_title = Text("The recipe:", font_size=32, color=WHITE).shift(UP * 2.0)
        self.play(Write(recipe_title))

        ingredients = VGroup(
            MathTex(r"1.\;\text{Nonlinear restoring force}",
                    font_size=32, color=YELLOW),
            MathTex(r"2.\;\text{Two or more degrees of freedom}",
                    font_size=32, color=YELLOW),
            MathTex(r"3.\;\text{Sensitive dependence on initial conditions}",
                    font_size=32, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)\
         .next_to(recipe_title, DOWN, buff=0.5)

        for item in ingredients:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(0.4)

        self.wait(0.5)

        # ── Act 5: Tease double pendulum phase portrait ───────
        self.play(FadeOut(recipe_title), FadeOut(ingredients))

        tease = Text("A simple example:", font_size=28, color=GREY)\
                    .to_edge(UP, buff=0.8)
        self.play(Write(tease))

        def chaotic_curve(t):
            x = 2.5 * np.sin(2.3 * t) * np.cos(0.7 * t + 0.5)
            y = 2.0 * np.cos(1.7 * t) * np.sin(1.1 * t + 1.0)
            return np.array([x, y, 0])

        axes_p = Axes(
            x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
            x_length=5, y_length=4,
            axis_config={"include_tip": False, "stroke_opacity": 0.4}
        ).shift(DOWN * 0.5)

        # ── Fixed: pass MathTex objects, no font_size kwarg ───
        x_p = axes_p.get_x_axis_label(
            MathTex(r"\theta_1", font_size=28), direction=RIGHT
        )
        y_p = axes_p.get_y_axis_label(
            MathTex(r"\dot{\theta}_1", font_size=28), direction=UP
        )

        portrait = ParametricFunction(
            chaotic_curve,
            t_range=[0, 20, 0.01],
            color=RED,
            stroke_width=1.5,
            stroke_opacity=0.85
        )

        phase_lbl = Text("Phase portrait — double pendulum",
                         font_size=22, color=GREY)\
                        .next_to(axes_p, DOWN, buff=0.2)

        self.play(FadeIn(axes_p), FadeIn(x_p), FadeIn(y_p), FadeIn(phase_lbl))
        self.play(Create(portrait), run_time=4, rate_func=linear)
        self.wait(0.5)

        # ── Act 6: Bridge to Scene 7 ──────────────────────────
        bridge = Text("Meet the double pendulum →",
                      font_size=30, color=WHITE).to_edge(DOWN, buff=0.4)
        self.play(Write(bridge))
        self.wait(2.5)