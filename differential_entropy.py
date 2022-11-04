from manim import *
import numpy as np

config.background_color = WHITE
Mobject.set_default(color=DARK_GRAY)

class DifferentialEntropy(Scene):
    def construct(self):
        x_range_end = 5

        ax = Axes(
            x_range=[0, x_range_end],
            y_range=[0, 1.2],
        )

        # labels = ax.get_axis_labels(
        #     y_label='p(x)',
        # )

        dist_label = Tex("$p(x)$", color=BLUE_C).shift(2*UP + 4*LEFT)
        entro_label = Tex(r"$\log \frac{1}{p(x)}$", color=RED_C).shift(4*RIGHT)

        def some_function(x):
            # return 1
            return np.exp(-x)
            # return -5*x + 4
            # return 1.2 - 0.2*x

        some_function_curve = ax.plot(
            some_function,
            x_range=[0, x_range_end],
            color=BLUE_C
        )

        scale = 0.15
        diff_entro = ax.plot(
            lambda x: scale*np.log2(1/some_function(x)),
            x_range=[0, x_range_end],
            color=RED_C
        )

        self.add(
            ax,
            dist_label,
            entro_label,
            some_function_curve,
            diff_entro,
        )


        def equal_area_partitions(n):
            dx = x_range_end/10000
            line_positions = [0]
            sample = 0
            area = 0
            for i in range(n):
                while area <= (i+1)/n and sample+dx < x_range_end:
                    area += (dx/2)*(some_function(sample) + some_function(sample+dx))
                    sample += dx

                line_positions.append(sample)

            partitions = []
            for i in range(n):
                left = line_positions[i]

                vert_line = ax.get_vertical_line(
                    ax.input_to_graph_point(left, some_function_curve),
                    color=GREEN,
                    line_func=Line,
                    # line_config={"dashed_ratio": 1},
                )

                partitions.append(vert_line)

            return VGroup(*partitions)

        for i in range(7):
            n = 2**i
            partitions = equal_area_partitions(n)
            n_label = Tex(f"$n = {n}$").shift(3*UP)

            self.add(n_label,partitions)
            self.wait()
            self.remove(n_label,partitions)
