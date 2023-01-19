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
            return np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) / (x * sigma * np.sqrt(2 * np.pi))

            # return np.exp(-x)*np.sqrt(x)
            # return -5*x + 4


        some_function_curve = ax.plot(
            some_function,
            x_range=[0, x_range_end],
            color=DARK_BLUE
        )

        dist_label = Tex("$p(x)$", color=some_function_curve.color).shift(2*UP + 4*LEFT)


        x_star = 1.48
        intersection_point = [x_star, 0.25, 0]
        intersection_line = Line(
            start=ax.c2p(*intersection_point),
            end=ax.c2p(x_star, -0.07, 0),
        )
        intersection_label = Tex(f'$x*$').next_to(intersection_line, 1*DOWN)



        self.add(
            ax,
            dist_label,
            some_function_curve,
            intersection_line,
            intersection_label,
        )


        def accumulate_area(desired_area, area_start_point):
            dx = x_range_end/10000
            sample = area_start_point
            area = 0
            while area <= desired_area and sample+dx < x_range_end:
                area += (dx/2)*(some_function(sample) + some_function(sample+dx))
                sample += dx

            return sample


        # import pdb;pdb.set_trace()

        converging_points = []
        area_start_point = 0
        for n in range(1, 6):
            area_point = accumulate_area(1/2**n, area_start_point)
            converging_points.append(area_point)
            if area_point < x_star:
                area_start_point = area_point
            # (else we keep area_start_point at 0)



            partition_lines = VGroup(*[
                ax.get_vertical_line(
                    ax.input_to_graph_point(point, some_function_curve),
                    color=GREEN,
                    line_func=Line,
                ) for point in converging_points
            ])
            n_label = Tex(f"$n = {n}$").shift(3*UP)

            self.add(n_label, partition_lines)
            self.wait()
            self.remove(n_label, partition_lines)



