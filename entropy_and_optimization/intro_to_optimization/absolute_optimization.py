from manim import *
from math import log

config.background_color = '#dce2e1'
Mobject.set_default(color='#22323b')

class AbsoluteOptimization(Scene):
    def construct(self):

        ax = Axes(
            x_range=[0, 1, 0.25],
            y_range=[0, 5],
            x_axis_config={
                "include_tip": False,
                "include_numbers": True,
                # I wanted the x-axis to increment down instead of up, and this is the first fix I got working
                "rotation": 180*DEGREES,
            },
        )

        labels = ax.get_axis_labels(
            x_label='p_x',
            y_label='\Omega_{abs}(x)',
        )

        expo = ax.plot(lambda x: log(1/x), x_range=[0.009, 1, 0.01], color='#4c8095')

        # equation = Tex('$\Omega_{abs}(x) = \log \\frac{1}{p_x}$')

        self.add(
            ax,
            labels,
            expo,
            # equation,
        )
