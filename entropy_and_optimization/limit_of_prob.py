from manim import *
import numpy as np
import scipy.integrate as integrate

from optimization_config import *

config.pixel_height = 580

class LimitOfProb(Scene):
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


        self.add(
            ax,
            dist_label,
            some_function_curve,
        )


        def area_fraction(i, n):
            fraction = x_range_end/n
            area, _ = integrate.quad(
                lambda x: some_function(x), i*fraction, (i+1)*fraction
            )
            return area

        for n in range(100):
            intersection_lines = []
            intersection_labels = []
            for i in range(n): 
                x_loc = (i + 0.5)*x_range_end/n
                intersection_point = [x_loc, (n+1)*(0.22)*area_fraction(i, n), 0]
                intersection_line = Line(
                    start=ax.c2p(*intersection_point),
                    end=ax.c2p(x_loc, 0, 0),
                )
                intersection_lines.append(intersection_line)
                # intersection_labels.append(
                #     Tex(r'$i_\{' + str(i) + r'\}$').next_to(intersection_line, 1*DOWN)
                # )

            self.add(
                *intersection_lines,
                # *intersection_labels,
            )
            self.wait(1/(n+1) + 0.1)
            self.remove(
                *intersection_lines,
                # *intersection_labels,
            )


        # def accumulate_area(desired_area, area_start_point):
        #     dx = x_range_end/10000
        #     sample = area_start_point
        #     area = 0
        #     while area <= desired_area and sample+dx < x_range_end:
        #         area += (dx/2)*(some_function(sample) + some_function(sample+dx))
        #         sample += dx

        #     return sample

        # partition_lines = []

        # converging_points = []
        # area_start_point = 0
        # for n in range(1, 6):
        #     area_point = accumulate_area(1/2**n, area_start_point)
        #     converging_points.append(area_point)
        #     compare_char = ">"
        #     bit_char = 1
        #     if area_point < x_star:
        #         area_start_point = area_point
        #         compare_char = "<"
        #         bit_char = 0


        #     partition_lines.append(
        #         ax.get_vertical_line(
        #             ax.input_to_graph_point(area_point, some_function_curve),
        #             line_func=Line,
        #         )
        #     )

        #     self.add(*partition_lines)
        #     self.wait()
        #     self.remove(*partition_lines)
