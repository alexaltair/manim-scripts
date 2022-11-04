from manim import *
from math import log, exp

config.background_color = '#ffeae3'
Mobject.set_default(color=DARK_GRAY)

class AbsoluteOptimization(Scene):
    def construct(self):

        ax = Axes(
            x_range=[0, 1, 0.25],
            y_range=[0, 5],
            x_axis_config={
                "include_tip": False,
                "include_numbers": True,
            },
        )

        labels = ax.get_axis_labels(
            x_label='p_x',
            y_label='\Omega_{abs}(x)',
        )

        expo = ax.plot(lambda x: log(1/x), x_range=[0.01, 1, 0.01], color=BLUE)

        # equation = Tex('$\Omega_{abs}(x) = \log \\frac{1}{p_x}$')

        self.add(
            ax,
            labels,
            expo,
            # equation,
        )
