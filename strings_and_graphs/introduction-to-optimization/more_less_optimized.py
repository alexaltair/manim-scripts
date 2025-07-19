import random
from string import ascii_uppercase

from manim import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import directed_graphs as dg
from visual_config import add_background_rectangle

DOT_RADIUS = 0.4
NUM_STATES = 7
MARGIN = 0.8


def label_dot(self, label, dot):
    label_mobj = Text(label).move_to(dot).scale(dot.radius * 2)
    label_mobj.set_z_index(2)
    self.add_foreground_mobject(label_mobj)


def add_less_than_sign(self, dot1, dot2):
    x_coord = (dot1.get_center()[0] + dot2.get_center()[0]) / 2
    y_coord = dot1.get_center()[1]
    point = Point(location=[x_coord, y_coord, 0])
    self.add(Text("<").move_to(point).scale(dot1.radius * 2))


def create_labeled_dots_lineup(self, num_states, radius):
    dots = {}
    random.seed(1)
    labels = [*ascii_uppercase[0:num_states]]
    random.shuffle(labels)

    for i in range(len(labels)):
        label = labels[i]
        effective_screen_width = config.frame_width - (MARGIN + radius) * 2
        x_coord = effective_screen_width / (len(labels) - 1) * (i) - (
            effective_screen_width / 2
        )

        dot = Dot(
            point=[x_coord, 0, 0],
            radius=radius,
            stroke_width=dg.VERTEX_STROKE_WIDTH,
            color=dg.STROKE_COLOR,
            fill_color=dg.FILL_COLOR,
        )

        dots[label] = dot
        dot.align_on_border(DOWN, buff=MARGIN)
        self.add(dot)
        dg.add_drop_shadow(self, dot)
        label_dot(self, label, dot)
        if i > 0:
            add_less_than_sign(self, dots[labels[i - 1]], dot)

    return dots


def label_graph(self, graph):
    for i in range(len(graph.vertices)):
        vertex = graph.vertices[i]
        label_dot(self, ascii_uppercase[i], vertex)


def animate_graph_and_lineup(self, graph, dots):
    for i in range(len(graph.edges)):
        vertex = graph.vertices[i]

        self.play(
            Indicate(vertex, color=dg.INDICATE_COLOR, scale_factor=dg.INDICATE_SCALE),
            Indicate(
                dots[ascii_uppercase[i]],
                color=dg.INDICATE_COLOR,
                scale_factor=dg.INDICATE_SCALE,
            ),
        )

        if i + 1 < len(graph.edges):
            edge = graph.edges[(i, i + 1)]
        else:
            edge = graph.edges[(i, 0)]

        self.play(
            Indicate(edge, color=dg.INDICATE_COLOR, scale_factor=dg.INDICATE_SCALE)
        )


class MoreLessOptimized(Scene):
    def construct(self):
        add_background_rectangle(self, config)

        state_graph = dg.create_directed_graph(NUM_STATES, vertex_radius=DOT_RADIUS)
        state_graph.align_on_border(UP, buff=MARGIN)
        self.add(state_graph)
        label_graph(self, state_graph)
        dg.add_drop_shadows_to_graph(self, state_graph)

        dots = create_labeled_dots_lineup(self, NUM_STATES, DOT_RADIUS)

        less_optimized_label = (
            Text("Less optimized").shift(2.5 * DOWN).scale(2 * DOT_RADIUS)
        )
        less_optimized_label.align_on_border(LEFT, buff=MARGIN)
        self.add(less_optimized_label)

        more_optimized_label = (
            Text("More optimized").shift(2.5 * DOWN).scale(2 * DOT_RADIUS)
        )
        more_optimized_label.align_on_border(RIGHT, buff=MARGIN)
        self.add(more_optimized_label)

        animate_graph_and_lineup(self, state_graph, dots)
