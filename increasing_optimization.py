from manim import *
import numpy as np

config.pixel_height = 580
config.background_color = WHITE
Mobject.set_default(color=DARK_GRAY)

class IncreasingOptimization(Scene):
    def construct(self):
        current_state = ValueTracker(0.001)

        ax = Axes(
            x_range=[0, 4],
            y_range=[0, 0.8],
            # x_axis_config={"numbers_to_include": [current_state]},
        )

        labels = ax.get_axis_labels(
            y_label='p(x)',
        )

        x_axis_text = Tex(r'$\leftarrow$ States ordered according to $C \rightarrow$').next_to(ax, DOWN)


        def lognormal(x, mu=0.0, sigma=1.0):
            # This is a base 10 log but it's just an arbitrary probability distribution so that doesn't matter
            return np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) / (x * sigma * np.sqrt(2 * np.pi))

        lognormal_curve = ax.plot(lambda x: lognormal(x), x_range=[0.01, 4], color=BLUE_C)

        def current_area():
            samples, dx = np.linspace(current_state.get_value(), 20, retstep=True)
            return np.trapz(lognormal(samples), dx=dx)

        area_polygon = always_redraw(
            lambda: ax.get_area(lognormal_curve, [current_state.get_value(), 4], color=GREY, opacity=0.5)
        )

        area_text = always_redraw(
            lambda: Tex(f"$p_x = {current_area():.2f}$").shift(2*UP + 2*RIGHT)
        )

        def draw_opt_text():
            opt_bits = np.log2(1/current_area())
            return Tex(r'$\Omega_{abs}(x) = ' + f'{opt_bits:.2f}$ bits of optimization').next_to(area_text, DOWN)

        opt_text = always_redraw(draw_opt_text)

        self.add(
            ax,
            labels,
            x_axis_text,
            lognormal_curve,
            area_polygon,
            area_text,
            opt_text,
        )

        self.play(
            current_state.animate.set_value(4),
            run_time=8,
        )
        self.wait()
