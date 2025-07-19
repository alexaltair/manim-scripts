import math

from manim import *

from visual_config import STROKE_COLOR


VERTEX_STROKE_WIDTH = 2.5
ARROW_STROKE_WIDTH = 4
DROP_SHADOW_THICKNESS = 0.02
FILL_COLOR = "#f1f2f2"
INDICATE_COLOR = "#daa538"
INDICATE_SCALE = 1.1

EDGE_LENGTH = 0.8
EDGE_MARGIN = 0.1


def add_drop_shadow(self, mobj):
    mobj.set_z_index(1)
    shadow = mobj.copy()
    shadow.set_z_index(0)
    shadow.fill_color = STROKE_COLOR
    shadow.stroke_color = STROKE_COLOR
    shadow.shift(DROP_SHADOW_THICKNESS * DOWN)
    shadow.shift(DROP_SHADOW_THICKNESS * RIGHT)
    self.add(shadow)


def add_drop_shadows_to_graph(self, graph):
    for _, vertex in graph.vertices.items():
        add_drop_shadow(self, vertex)


def get_edge_length(edge):
    return math.dist((edge.start[0], edge.start[1]), (edge.end[0], edge.end[1]))


# This creates a graph and scales it such that all the arrowheads are
# approximately evenly sized. They will no longer be approximately
# evenly sized if you make a graph with fewer than four vertices.
def create_directed_graph(num_vertices, vertex_radius=0.2, layout_scale=1):
    vertex_settings = {
        "radius": vertex_radius,
        "stroke_color": STROKE_COLOR,
        "stroke_opacity": 100,
        "stroke_width": VERTEX_STROKE_WIDTH,
        "fill_color": FILL_COLOR,
    }
    edge_settings = {
        "stroke_color": STROKE_COLOR,
        "stroke_opacity": 100,
        "stroke_width": ARROW_STROKE_WIDTH,
        "max_stroke_width_to_length_ratio": 100,
        "max_tip_length_to_length_ratio": 0.2,
    }

    vertices = list(range(0, num_vertices))

    edges = []
    for i in range(0, num_vertices - 1):
        edges.append((i, i + 1))
    edges.append((num_vertices - 1, 0))

    vertex_config = {}
    for i in range(0, num_vertices):
        vertex_config[i] = vertex_settings

    edge_config = {}
    for edge in edges:
        edge_config[edge] = edge_settings

    # Calculate scale factor for entire layout
    scale_factor = EDGE_LENGTH + EDGE_MARGIN * 2 + vertex_radius * 2

    g = Graph(
        vertices,
        edges,
        vertex_config=vertex_config,
        edge_config=edge_config,
        layout="circular",
        layout_scale=num_vertices * 0.1 * 2 * scale_factor,
        edge_type=Arrow,
    )

    g.update()
    g.clear_updaters()

    # Normalize edge lengths
    # TODO: This appears to be scaling things too small. (There is a
    # margin even when EDGE_MARGIN is set to 0.)
    initial_length = get_edge_length(g.edges[edge])
    edge_scale_factor = EDGE_LENGTH / initial_length
    for edge in g.edges:
        g.edges[edge].scale(edge_scale_factor)

        # This line is necessary for the edges to render above the
        # background rectangle
        g.edges[edge].set_z_index(2)

    # TODO: Need to scale arrowheads as well. And arrow line thickness.
    # The arrows look very different for a graph with vertex_radius = 0.1
    # vs a graph with vertex_radius = 2.1

    return g


def animate_graph(self, graph):
    for i in range(0, len(graph.edges)):
        vertex = graph.vertices[i]

        self.play(Indicate(vertex, color=INDICATE_COLOR, scale_factor=INDICATE_SCALE))

        if i + 1 < len(graph.edges):
            edge = graph.edges[(i, i + 1)]
        else:
            edge = graph.edges[(i, 0)]

        self.play(Indicate(edge, color=INDICATE_COLOR, scale_factor=INDICATE_SCALE))
