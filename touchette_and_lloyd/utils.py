from manim import *

BG_COLOR = "#dde3e1"
OUTER_COLOR = "#22333a"
N_NODE_COLOR = "#d77f87"
X_NODE_COLOR = "#d49971"
S_NODE_COLOR = "#e0c181"
R_NODE_COLOR = "#a8c099"
Z_NODE_COLOR = "#9acfcd"


def add_shadow(mobject, color=BLACK, opacity=0.2, shift=(0.2, -0.2, 0)):
    shadow = (
        mobject.copy()
        .set_fill(color, opacity=opacity)
        .set_stroke(width=0)
        .shift(shift)
        .set_z_index(-1)
    )
    mobject.add(shadow)
    return mobject


def create_node(color=OUTER_COLOR, fill_color=WHITE, label=None, label_shift=None):
    node_group = VGroup()

    node = Circle(color=color, fill_color=fill_color, fill_opacity=1)
    add_shadow(node, opacity=1, shift=(0.1, -0.07, 0), color=color)

    node_group.add(node)

    if label:
        # rf"\textbf{{\textit{{{label}}}"
        text = Tex(rf"${label}$", color=color).scale(2).move_to(node)
        if label_shift:
            text.shift(label_shift)
            node_group.add(text)

    return node_group.scale(0.7)


def add_edge(
    node1, node2, start_pos=None, end_pos=None, color=OUTER_COLOR, tip_length=0.2
):
    """
    Create an arrow edge between two nodes with optional position specifications.

    Args:
        node1: Source node
        node2: Target node
        start_pos: Optional start position ("top_right", "bottom_right", "right")
        end_pos: Optional end position ("top_left", "bottom_left", "left")
        color: Arrow color
        tip_length: Length of arrow tip
    """

    # Create boundary rings around nodes for edge attachment
    node1_ring = _create_node_boundary_ring(node1)
    node2_ring = _create_node_boundary_ring(node2)

    # Define specific attachment points for precise positioning
    start_positions = {
        "top_right": node1[0].get_end() + 0.2 * UP + 0.2 * LEFT,
        "bottom_right": node1[0].get_end() + 0.2 * DOWN + 0.2 * LEFT,
        "right": node1.get_right() + 0.2 * LEFT,
    }

    end_positions = {
        "top_left": node2[0].get_start() + 1.34 * LEFT + 0.4 * UP,
        "bottom_left": node2[0].get_start() + 1.42 * LEFT + 0.2 * DOWN,
        "left": node2.get_left() + 0.05 * LEFT,
    }

    # Determine start and end points
    start_point = start_positions[start_pos] if start_pos else node1.get_center()
    end_point = end_positions[end_pos] if end_pos else node2_ring

    # Create the arrow edge
    edge = Arrow(
        start=start_point,
        end=end_point,
        buff=0,
        tip_shape=StealthTip,
        tip_length=tip_length,
    ).set_color(color)

    # Place edge behind nodes
    edge.set_z_index(-1)

    return edge


def _create_node_boundary_ring(node):
    """
    Create a boundary ring around a node for edge attachment.

    Args:
        node: The node to create a boundary around

    Returns:
        Circle or Rectangle representing the node boundary
    """
    # Check if node is a circular VGroup
    if isinstance(node, VGroup) and isinstance(node[0], Circle):
        return Circle(radius=node.width / 2 + 0.05).move_to(node)

    # Handle rectangular or other node types
    return Rectangle(width=node.width + 0.03, height=node.height + 0.03).move_to(node)
