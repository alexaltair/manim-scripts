from manim import *
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import directed_graphs as dg
from visual_config import add_background_rectangle

class DirectedGraphs(Scene):
    def construct(self):
        add_background_rectangle(self, config)

        outer_circle = dg.create_directed_graph(9).shift(2 * RIGHT)
        self.add(outer_circle)
        dg.add_drop_shadows_to_graph(self, outer_circle)

        inner_circle = dg.create_directed_graph(5).shift(2 * RIGHT)
        self.add(inner_circle)
        dg.add_drop_shadows_to_graph(self, inner_circle)

        left_circle = dg.create_directed_graph(7)
        left_circle.next_to(outer_circle, LEFT, buff=1)
        left_circle.shift(1.2 * UP)
        self.add(left_circle)
        dg.add_drop_shadows_to_graph(self, left_circle)

        low_circle = dg.create_directed_graph(3)
        low_circle.next_to(outer_circle, LEFT, buff=0.5)
        low_circle.shift(2 * DOWN)
        self.add(low_circle)
        dg.add_drop_shadows_to_graph(self, low_circle)

        # TODO it's not MVP, but Alex would prefer at least the 1-node
        # graph on here

        dg.animate_graph(self, inner_circle)

