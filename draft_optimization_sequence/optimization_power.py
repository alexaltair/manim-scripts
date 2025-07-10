from manim import *
from math import log, exp
import numpy as np

config.pixel_height = 600
config.background_color = WHITE
Mobject.set_default(color=DARK_GRAY)

class OptimizationPower(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 4],
            y_range=[-1, 4],
        )

        labels = ax.get_axis_labels(
            x_label='time',
            y_label='\Omega_{abs}',
        )

        def normal(x):    
            return exp(-x**2)
            # mean = 0
            # std = 1
            # variance = np.square(std)
            # return np.exp(-np.square(x-mean)/2*variance)/(np.sqrt(2*np.pi*variance))

        hyp = ax.plot(lambda x: -1/(x-4) - 1/4, x_range=[0, 3.9], color=RED_C)
        expo = ax.plot(lambda x: exp(0.4*x) - 1, x_range=[0, 4], color=BLUE_D)
        messy = ax.plot(lambda x: exp(0.4*x) - 1 - 1.5*normal(x - 1.2) + 1.5*normal(1.2), x_range=[0, 4], color=GREEN_C)

        self.add(
            ax,
            labels,
            hyp,
            messy,
            expo,
        )
