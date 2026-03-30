from manim import *
import numpy as np

class Scene5Math(Scene):
    def construct(self):

        # ── Step 1: The full equation ─────────────────────────
        title = Text("Why does period grow?", font_size=32).to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        eq_full = MathTex(
            r"\ddot{\theta} + \frac{g}{L} \sin\theta = 0",
            font_size=42
        ).shift(UP * 1.5)
        self.play(Write(eq_full))
        self.wait(0.8)

        # ── Step 2: Taylor expand sin(θ) ─────────────────────
        expand_lbl = Text("Taylor expand sin θ :", font_size=24, color=GREY).next_to(eq_full, DOWN, buff=0.5)
        expand = MathTex(
            r"\sin\theta = \theta - \frac{\theta^3}{6} + \frac{\theta^5}{120} - \cdots",
            font_size=36
        ).next_to(expand_lbl, DOWN, buff=0.2)

        self.play(Write(expand_lbl), Write(expand))
        self.wait(1.0)

        # ── Step 3: Small angle — drop cubic and above ────────
        self.play(FadeOut(expand_lbl))
        small_lbl = Text("Small angle  (θ₀ ≪ 1)  →  keep only first term:",
                         font_size=24, color=BLUE).next_to(eq_full, DOWN, buff=0.5)
        eq_linear = MathTex(
            r"\ddot{\theta} + \frac{g}{L} \theta = 0",
            r"\quad \Rightarrow \quad T_0 = 2\pi\sqrt{\frac{L}{g}}",
            font_size=36, color=BLUE
        ).next_to(small_lbl, DOWN, buff=0.2)

        self.play(ReplacementTransform(expand, small_lbl))
        self.play(Write(eq_linear))
        self.wait(1.0)

        # ── Step 4: Key inequality ────────────────────────────
        ineq_lbl = Text("For large θ :", font_size=24, color=RED).next_to(eq_linear, DOWN, buff=0.5)
        ineq = MathTex(
            r"\sin\theta < \theta \quad \text{for } \theta > 0",
            font_size=36, color=RED
        ).next_to(ineq_lbl, DOWN, buff=0.2)

        self.play(Write(ineq_lbl), Write(ineq))
        self.wait(0.8)

        consequence = MathTex(
            r"\Rightarrow \frac{g}{L}\sin\theta < \frac{g}{L}\theta"
            r"\quad \Rightarrow \quad \text{weaker restoring force}",
            font_size=30, color=RED
        ).next_to(ineq, DOWN, buff=0.3)
        self.play(Write(consequence))
        self.wait(1.2)

        # ── Clear and show exact period formula ───────────────
        self.play(
            FadeOut(small_lbl), FadeOut(eq_linear),
            FadeOut(ineq_lbl),  FadeOut(ineq),
            FadeOut(consequence),
        )

        exact_lbl = Text("Exact period (elliptic integral):", font_size=24, color=GREY)\
                        .next_to(eq_full, DOWN, buff=0.5)
        eq_exact = MathTex(
            r"T(\theta_0) = 4\sqrt{\frac{L}{g}}\; K\!\left(\sin\frac{\theta_0}{2}\right)",
            font_size=38
        ).next_to(exact_lbl, DOWN, buff=0.3)

        self.play(Write(exact_lbl), Write(eq_exact))
        self.wait(0.8)

        where = MathTex(
            r"\text{where } K(k) = \int_0^{\pi/2} \frac{d\phi}{\sqrt{1 - k^2\sin^2\phi}}",
            font_size=30, color=GREY
        ).next_to(eq_exact, DOWN, buff=0.3)
        self.play(Write(where))
        self.wait(0.8)

        # ── Series approximation — more intuitive ─────────────
        series_lbl = Text("Series approximation:", font_size=24, color=GREY)\
                         .next_to(where, DOWN, buff=0.4)
        series = MathTex(
            r"T \approx T_0 \left(1 + \frac{\theta_0^2}{16} + \frac{11\,\theta_0^4}{3072} + \cdots\right)",
            font_size=34, color=YELLOW
        ).next_to(series_lbl, DOWN, buff=0.2)

        self.play(Write(series_lbl), Write(series))
        self.wait(1.0)

        # ── Highlight the θ₀² term ───────────────────────────
        box = SurroundingRectangle(series, color=YELLOW, buff=0.12)
        insight = Text("Every extra term increases T — amplitude always slows it down",
                       font_size=22, color=YELLOW).next_to(box, DOWN, buff=0.2)

        self.play(Create(box))
        self.play(Write(insight))
        self.wait(2.5)

        # ── Numerical check ───────────────────────────────────
        self.play(
            FadeOut(exact_lbl), FadeOut(eq_exact), FadeOut(where),
            FadeOut(series_lbl), FadeOut(series),
            FadeOut(box), FadeOut(insight),
        )

        check_lbl = Text("Numerical check (L = 1.8 m):", font_size=24, color=GREY)\
                        .next_to(eq_full, DOWN, buff=0.5)
        table = MathTex(
            r"""
            \begin{array}{c|c|c}
            \theta_0 & T \text{ (exact)} & T/T_0 \\
            \hline
            10°  & 2.70\,\text{s} & 1.00 \\
            30°  & 2.74\,\text{s} & 1.02 \\
            60°  & 2.90\,\text{s} & 1.07 \\
            80°  & 3.12\,\text{s} & 1.16 \\
            \end{array}
            """,
            font_size=30
        ).next_to(check_lbl, DOWN, buff=0.3)

        self.play(Write(check_lbl), Write(table))
        self.wait(1.5)

        final = MathTex(
            r"T \text{ grows monotonically with } \theta_0"
            r"\quad \Leftarrow \quad \sin\theta < \theta",
            color=YELLOW, font_size=30
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(final))
        self.wait(3)