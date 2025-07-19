from manim import *
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
import visual_config as vc


class UniformProb(Scene):
    def construct(self):
        vc.add_background_rectangle(self, config)

        x_axis_font_size = 33

        ax = Axes(
            x_range=[-0.5, 4.5],
            y_range=[0, 0.8],
            x_axis_config={
                "include_numbers": True,
                "font_size": x_axis_font_size,
                "tip_width": vc.ARROW_TIP_WIDTH,
                "tip_height": vc.ARROW_TIP_WIDTH,
            },
            y_axis_config={
                "tip_width": vc.ARROW_TIP_WIDTH,
                "tip_height": vc.ARROW_TIP_WIDTH,
            },
        )

        def lognormal(x, mu=0.0, sigma=1.0):
            # This is a base 10 log but it's just an arbitrary probability distribution
            return np.exp(-((np.log(x) - mu) ** 2) / (2 * sigma**2)) / (
                x * sigma * np.sqrt(2 * np.pi)
            )

        lognormal_curve = ax.plot(
            lambda x: lognormal(x), x_range=[0.01, 4.5], color=vc.PLOT_COLOR
        )
        lognormal_label = Tex("$p(x)$", color=lognormal_curve.color).shift(
            2 * LEFT + 1.2 * UP
        )

        uniform_dist = ax.plot(lambda x: 0.25, x_range=[0, 4], color=vc.DARK_BLUE)
        uniform_label = Tex("$p_u(x)$", color=uniform_dist.color).next_to(uniform_dist)

        intersection_x = 1.48
        intersection_point = [intersection_x, 0.25, 0]
        intersection_line = Line(
            start=ax.c2p(*intersection_point),
            end=ax.c2p(intersection_x, -0.07, 0),
        )
        intersection_label = Tex(
            f"$x = {intersection_x}$", font_size=x_axis_font_size
        ).next_to(intersection_line, 1 * DOWN)

        self.add(
            ax,
            lognormal_curve,
            lognormal_label,
            uniform_dist,
            uniform_label,
            intersection_line,
            intersection_label,
        )
