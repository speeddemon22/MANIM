from manim import *
class TestTex(Scene):
    def construct(self):
        eq = MathTex(r"\ddot{x} = -\omega^2 x")
        self.play(Write(eq))
        self.wait()