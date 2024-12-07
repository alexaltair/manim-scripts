import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import numpy as np
import scipy.integrate as integrate

from manim import *

import visual_config as vc

class LimitOfProb(Scene):
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
        #     color=vc.PLOT_COLOR,
        # )


        def some_function(x):
            if x == 0:
                return 0
            mu = 0.0
            sigma = 1.0
            # This is a base 10 log but it's just an arbitrary probability distribution
            return np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) / (x * sigma * np.sqrt(2 * np.pi))


        some_function_curve = ax.plot(
            some_function,
            x_range=[0, x_range_end],
            color=vc.PLOT_COLOR,
        )

        dist_label = Tex("$p(x)$", color=some_function_curve.color).next_to(ax, LEFT)


        self.add(
            ax,
            dist_label,
            some_function_curve,
        )


        def area_fraction(i, n):
            fraction = x_range_end/n
            area, _ = integrate.quad(
                lambda x: some_function(x), (i-1)*fraction, i*fraction
            )
            return area

        speedup = 8
        sequence_of_n = [int(speedup*(1.2**i)) for i in range(16)]
        sequence_of_n = list(range(1, speedup)) + sequence_of_n

        for n in sequence_of_n:
            intersection_lines = []
            intersection_labels = []
            for i in range(1, n+1):
                x_loc = (i - 0.5)*x_range_end/n
                intersection_point = [x_loc, (n+1)*(0.22)*area_fraction(i, n), 0]
                # Next time you play with this, try using ax.get_vertical_line
                intersection_line = Line(
                    start=ax.c2p(x_loc, 0, 0),
                    end=ax.c2p(*intersection_point),
                    color=vc.MEDIUM_RED,
                )
                intersection_dot = Dot(
                    point=ax.c2p(*intersection_point),
                    color=vc.MEDIUM_RED,
                )
                intersection_lines.append(intersection_line)
                intersection_lines.append(intersection_dot)
                if n <= speedup:
                    intersection_labels.append(
                        Tex(
                            r'$x_{' + str(i) + r'}$',
                            color=vc.MEDIUM_RED,
                        ).next_to(intersection_line, 1*DOWN)
                    )
                    intersection_labels.append(
                        Tex(
                            r'$P_{' + str(n) + r'}(' + str(i) + r')$',
                            color=vc.MEDIUM_RED,
                        ).next_to(intersection_line, 1*UP)
                    )
                    if i == 1:
                        intersection_labels[-1].shift(0.4*UP)

            n_label = Tex(f'$n={n}$').shift(2*UP + 3*RIGHT).scale(1.8)

            self.add(
                *intersection_lines,
                *intersection_labels,
                n_label,
            )
            if n <= speedup:
                self.wait()
            else:
                self.wait(1.3/(n+1) + 0.1)
            self.remove(
                *intersection_lines,
                *intersection_labels,
                n_label,
            )
