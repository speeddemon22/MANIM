from manim import *
import numpy as np

class SpringMassSystem(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-5, 10, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=4
        ).to_edge(DOWN)

        wall_x = -5
        equilibrium_x = 0
        amplitude = 1.5
        omega = 2
        t = ValueTracker(0)

        def mass_x():
            return equilibrium_x + amplitude * np.cos(omega * t.get_value())

        wall = Line(
            ax.c2p(wall_x, -1.5),
            ax.c2p(wall_x, 1.5),
            color=GREY
        )

        mass = always_redraw(
            lambda: Square(side_length=0.5, fill_color=BLUE, fill_opacity=1)
            .move_to(ax.c2p(mass_x(), 0))
        )

        def spring_points():
            x1 = wall_x
            x2 = mass_x() - 0.3
            n = 8
            pts = [ax.c2p(x1, 0)]
            dx = (x2 - x1) / (2 * n + 1)

            pts.append(ax.c2p(x1 + dx, 0))

            for i in range(1, 2 * n + 1):
                y = 0.25 if i % 2 else -0.25
                pts.append(ax.c2p(x1 + dx * (i + 1), y))

            pts.append(ax.c2p(x2, 0))
            return pts

        spring = always_redraw(
            lambda: VMobject(color=YELLOW).set_points_as_corners(spring_points())
        )

        eq_line = DashedLine(
            ax.c2p(equilibrium_x, -1.5),
            ax.c2p(equilibrium_x, 1.5),
            color=WHITE
        )

        title = Text("Spring-Mass System").scale(0.6).to_edge(UP)
        
        
        self.add( ax, wall, eq_line, spring, mass)
        self.play(Write(title))
        self.play(t.animate.set_value(8), run_time=8, rate_func=linear)
        self.wait()