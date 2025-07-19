import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import numpy as np
from manim import *

import visual_config as vc


class MeanValueTheorem(Scene):
    def construct(self):
        vc.add_background_rectangle(self, config)

        x_range_end = 4.5

        ax = Axes(
            x_range=[0, x_range_end],
            y_range=[0, 0.8],
            x_axis_config={
                "tip_width": vc.ARROW_TIP_WIDTH,
                "tip_height": vc.ARROW_TIP_WIDTH,
            },
            y_axis_config={
                "tip_width": vc.ARROW_TIP_WIDTH,
                "tip_height": vc.ARROW_TIP_WIDTH,
            },
        )

        def some_function(x):
            if x == 0:
                return 0
            mu = 0.0
            sigma = 1.0
            # This is a base 10 log but it's just an arbitrary probability distribution
            return np.exp(-((np.log(x) - mu) ** 2) / (2 * sigma**2)) / (
                x * sigma * np.sqrt(2 * np.pi)
            )

        some_function_curve = ax.plot(
            some_function, x_range=[0, x_range_end], color=vc.PLOT_COLOR
        )

        dist_label = Tex("$p(x)$", color=some_function_curve.color).shift(
            2 * UP + 4 * LEFT
        )

        x_i_minus_1 = 1.1
        intersection_point1 = [x_i_minus_1, some_function(x_i_minus_1), 0]
        intersection_line1 = Line(
            start=ax.c2p(*intersection_point1),
            end=ax.c2p(x_i_minus_1, -0.07, 0),
        )
        intersection_label1 = Tex(r"$x_{i-1}$").next_to(intersection_line1, 1 * DOWN)

        x_i = 2.1
        intersection_point2 = [x_i, some_function(x_i), 0]
        intersection_line2 = Line(
            start=ax.c2p(*intersection_point2),
            end=ax.c2p(x_i, -0.07, 0),
        )
        intersection_label2 = Tex(f"$x_i$").next_to(intersection_line2, 1 * DOWN)

        # Not the actually correct value, but just needs to look close
        x_tilde = (x_i + x_i_minus_1) * (0.98 / 2)
        intersection_point3 = [x_tilde, some_function(x_tilde), 0]
        intersection_line3 = Line(
            start=ax.c2p(*intersection_point3),
            end=ax.c2p(x_tilde, -0.07, 0),
        )
        intersection_label3 = Tex(r"$\tilde{x}_i$").next_to(
            intersection_line3, 1 * DOWN
        )

        func_area = ax.get_area(
            some_function_curve,
            [x_i_minus_1, x_i],
            color=vc.MEDIUM_BLUE,
            opacity=0.5,
        )

        rectangle_curve = ax.plot(
            lambda x: some_function(x_tilde),
            x_range=[x_i_minus_1, x_i],
            color=vc.PLOT_COLOR,
        )

        rect_area = ax.get_area(
            rectangle_curve,
            [x_i_minus_1, x_i],
            color=vc.BRIGHT_RED,
            opacity=0.5,
        )

        self.add(
            ax,
            dist_label,
            some_function_curve,
            intersection_line1,
            intersection_label1,
            intersection_line2,
            intersection_label2,
            intersection_line3,
            intersection_label3,
            func_area,
            rect_area,
        )
