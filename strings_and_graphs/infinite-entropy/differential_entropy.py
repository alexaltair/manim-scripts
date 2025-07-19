import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import numpy as np
from manim import *

import binary_string as bs
import visual_config as vc


class DifferentialEntropy(Scene):
    def construct(self):
        vc.add_background_rectangle(self, config)

        x_range_end = 4.5

        ax = Axes(
            x_length=10,
            x_range=[0, x_range_end],
            y_range=[0, 0.8],
            x_axis_config={
                "include_ticks": False,
                "tip_width": vc.ARROW_TIP_WIDTH,
                "tip_height": vc.ARROW_TIP_WIDTH,
            },
            y_axis_config={
                "tip_width": vc.ARROW_TIP_WIDTH,
                "tip_height": vc.ARROW_TIP_WIDTH,
            },
        )

        # labels = ax.get_axis_labels(
        #     y_label='p(x)',
        # )

        def some_function(x):
            if x == 0:
                return 0
            mu = 0.0
            sigma = 1.0
            # This is a base 10 log but it's just an arbitrary probability distribution
            return np.exp(-((np.log(x) - mu) ** 2) / (2 * sigma**2)) / (
                x * sigma * np.sqrt(2 * np.pi)
            )

            # return np.exp(-x)*np.sqrt(x)
            # return -5*x + 4

        some_function_curve = ax.plot(
            some_function, x_range=[0, x_range_end], color=vc.PLOT_COLOR
        )

        dist_label = Tex("$p(x)$", color=some_function_curve.color).shift(
            3 * UP + 4 * LEFT
        )

        x_star = 1.48
        intersection_point = [x_star, 0, 0]
        intersection_line = Line(
            start=ax.c2p(*intersection_point),
            end=ax.c2p(x_star, -0.07, 0),
        )
        intersection_label = Tex(f"$x*$").next_to(intersection_line, 1 * DOWN)

        self.add(
            ax,
            dist_label,
            some_function_curve,
            intersection_line,
            intersection_label,
        )
        self.wait()

        def accumulate_area(desired_area, area_start_point):
            dx = x_range_end / 10000
            sample = area_start_point
            area = 0
            while area <= desired_area and sample + dx < x_range_end:
                area += (dx / 2) * (some_function(sample) + some_function(sample + dx))
                sample += dx

            return sample

        colors = color_gradient(["#6b2c2c", "#d9a337", "#4f725e"], 5)
        partition_lines = []

        converging_points = []
        area_start_point = 0
        for n in range(1, 6):
            area_point = accumulate_area(1 / 2**n, area_start_point)
            converging_points.append(area_point)
            compare_char = ">"
            bit_char = 1
            if area_point < x_star:
                area_start_point = area_point
                compare_char = "<"
                bit_char = 0

            partition_lines.append(
                ax.get_vertical_line(
                    ax.input_to_graph_point(area_point, some_function_curve),
                    color=colors[n - 1],
                    line_func=Line,
                    stroke_width=3,
                )
            )

            bit_height = 0.5
            bit_label = Tex(f"${compare_char} x* \Longrightarrow$").shift(
                2 * RIGHT + 3.5 * UP + bit_height * n * DOWN
            )
            a_n_label = Tex(f"$a_{n}$", color=colors[n - 1]).next_to(bit_label, LEFT)

            if n == 1:
                binary_square = bs.BinaryStringEnd(
                    value=bit_char,
                    side_length=bit_height,
                    radius=0.125,
                    direction=bs.UP,
                )
            else:
                binary_square = bs.BinaryStringBit(
                    value=bit_char,
                    side_length=bit_height,
                )

            binary_square.next_to(bit_label)

            self.add(*partition_lines, a_n_label, bit_label, binary_square)
            self.wait(1.2)
            self.remove(*partition_lines)
