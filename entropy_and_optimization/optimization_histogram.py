from manim import *
from math import log, exp
import numpy as np

config.pixel_height = 600
config.background_color = WHITE
Mobject.set_default(color=DARK_GRAY)

class OptimizationHistogram(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 2.5],
            y_range=[0, 2],
        )

        labels = ax.get_axis_labels(
            x_label='\Omega_{abs}',
            y_label= Tex(r'fraction of states'),
        )
        # x_axis_text = Tex(r'fraction of states').next_to(ax, DOWN)

        def lognormal(x, mu=0.0, sigma=1.0):
            # This is a base 10 log but it's just an arbitrary probability distribution so that doesn't matter
            return np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) / (x * sigma * np.sqrt(2 * np.pi))

        def normal(x):    
            return exp(-x**2)
            # mean = 0
            # std = 1
            # variance = np.square(std)
            # return np.exp(-np.square(x-mean)/2*variance)/(np.sqrt(2*np.pi*variance))

        def pareto(x, scale=1, alpha=1):
            return alpha*(scale**alpha)/(x + scale)**(alpha + 1)

        # hyp = ax.plot(lambda x: 2/(x+1)**4, x_range=[0, 2.5], color=PURPLE_C)
        # less_hyp = ax.plot(lambda x: 0.2/(x+0.05)**(0.5), x_range=[0, 2.5, 0.001], color=GOLD_C)
        hyp = ax.plot(lambda x: pareto(x, 0.5), x_range=[0.01, 2.5], color=PURPLE_C)
        less_hyp = ax.plot(lambda x: pareto(x), x_range=[0.01, 2.5], color=GOLD_C)
        lognormal = ax.plot(lambda x: lognormal(x+0.05, 0, 0.2), x_range=[0, 2.5], color=TEAL_E)

        self.add(
            ax,
            labels,
            hyp,
            less_hyp,
            lognormal,
        )
