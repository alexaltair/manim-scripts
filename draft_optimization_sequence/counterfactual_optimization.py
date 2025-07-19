from manim import *
from math import log, exp

config.background_color = WHITE
Mobject.set_default(color=DARK_GRAY)


class CounterfactualOptimization(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 4],
            y_range=[-1, 3],
        )

        labels = ax.get_axis_labels(
            x_label="time",
            y_label="\Omega_{abs}",
        )

        def sigmoid(x):
            return 1 / (1 + exp(-x))

        nlog = ax.plot(lambda x: -log(x + 1) + 1, x_range=[0, 4], color=RED_C)
        messy = ax.plot(
            lambda x: 1.25
            - 0.5 * sigmoid(3.8 * x)
            - 0.5 * sigmoid(5 * (x - 1))
            - 0.5 * sigmoid(5 * (x - 3)),
            x_range=[0, 4],
            color=GREEN_C,
        )
        constant = ax.plot(lambda x: 1, x_range=[0, 4], color=BLUE_D)
        expo = ax.plot(lambda x: exp(0.2 * x), x_range=[0, 4], color=YELLOW_E)

        self.add(
            ax,
            labels,
            nlog,
            constant,
            messy,
            expo,
        )
