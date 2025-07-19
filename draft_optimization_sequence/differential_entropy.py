from manim import *
import numpy as np

from optimization_config import *

config.pixel_height = 580


class DifferentialEntropy(Scene):
    def construct(self):
        x_range_end = 4.5

        ax = Axes(
            x_range=[0, x_range_end],
            y_range=[0, 0.8],
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
            some_function, x_range=[0, x_range_end], color=DARK_BLUE
        )

        dist_label = Tex("$p(x)$", color=some_function_curve.color).shift(
            2 * UP + 4 * LEFT
        )

        x_star = 1.48
        intersection_point = [x_star, 0.25, 0]
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
                )
            )

            a_n_label = Tex(f"$a_{n}$", color=colors[n - 1]).shift(
                RIGHT + 3 * UP + 0.5 * n * DOWN
            )
            bit_label = Tex(f"${compare_char} x* \Longrightarrow {bit_char}$").next_to(
                a_n_label
            )

            self.add(*partition_lines, a_n_label, bit_label)
            self.wait()
            self.remove(*partition_lines)
