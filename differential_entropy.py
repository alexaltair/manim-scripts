from manim import *
import numpy as np

config.background_color = WHITE
Mobject.set_default(color=DARK_GRAY)

class DifferentialEntropy(Scene):
    def construct(self):
        iteration = ValueTracker(0)
        def current_n():
            return int(2**iteration.get_value())

        x_range_end = 5

        ax = Axes(
            x_range=[0, x_range_end],
            y_range=[0, 1.2],
        )

        labels = ax.get_axis_labels(
            y_label='p(x)',
        )

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

        def equal_area_rectangles(n):
            dx = x_range_end/10000
            rect_x_coords = [0]
            sample = 0
            area = 0
            for i in range(int(n)):
                while area <= (i+1)/int(n) and sample+dx < x_range_end:
                    area += (dx/2)*(some_function(sample) + some_function(sample+dx))
                    sample += dx

                rect_x_coords.append(sample)

            rect_colors = color_gradient([BLUE, GREEN], int(n))

            rectangles = []
            for i in range(int(n)):
                left = rect_x_coords[i]
                right = rect_x_coords[i+1]
                bottom = 0
                top = 1/(int(n)*(right - left))

                new_rect = Polygon(
                    ax.coords_to_point(left, bottom),
                    ax.coords_to_point(left, top),
                    ax.coords_to_point(right, top),
                    ax.coords_to_point(right, bottom),
                )
                new_rect.stroke_width = 1
                new_rect.set_fill(rect_colors[i], opacity=0.5)
                new_rect.set_stroke(GRAY)
                rectangles.append(new_rect)

            return VGroup(*rectangles)

        rectangles = always_redraw(
            lambda: equal_area_rectangles(current_n())
        )

        n_label = always_redraw(
            lambda: Tex(f"$n = {current_n()}$").shift(2*UP + 2*RIGHT)
        )

        self.add(
            ax,
            labels,
            n_label,
            some_function_curve,
            rectangles,
        )

        for i in range(7):
            self.play(
                iteration.animate.set_value(i),
                run_time=0.01,
            )
            self.wait()
