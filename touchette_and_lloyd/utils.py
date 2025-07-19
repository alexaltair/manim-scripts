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
    if isinstance(node1, VGroup) and isinstance(node1[0], Circle):
        node1_ring = Circle(radius=node1.width / 2 + 0.05).move_to(node1)
    else:
        node1_ring = Rectangle(
            width=node1.width + 0.03, height=node1.height + 0.03
        ).move_to(node1)

    if isinstance(node2, VGroup) and isinstance(node2[0], Circle):
        node2_ring = Circle(radius=node2.width / 2 + 0.03).move_to(node2)
    else:
        node2_ring = Rectangle(
            width=node2.width + 0.03, height=node2.height + 0.03
        ).move_to(node2)

    start_dict = {
        "top_right": node1[0].get_end() + 0.2 * UP + 0.2 * LEFT,
        "bottom_right": node1[0].get_end() + 0.2 * DOWN + 0.2 * LEFT,
        "right": node1.get_right() + 0.2 * LEFT,
    }

    end_dict = {
        "top_left": node2[0].get_start() + 1.34 * LEFT + 0.4 * UP,
        "bottom_left": node2[0].get_start() + 1.42 * LEFT + 0.2 * DOWN,
        "left": node2.get_left() + 0.05 * LEFT,
    }

    edge = Arrow(
        start=start_dict[start_pos] if start_pos else node1.get_center(),
        end=end_dict[end_pos] if end_pos else node2_ring,
        buff=0,
        tip_shape=StealthTip,
        tip_length=tip_length,
    ).set_color(color)
    edge.set_z_index(-1)

    return edge


class MagnifyingGlass(VMobject):
    def __init__(self, radius=1.0, handle_length=1.5, handle_color="#5b7c86", **kwargs):
        super().__init__(**kwargs)

        # Create the lens
        self.lens = Circle(
            radius=radius,
            color=kwargs.get("color", "#9bbec8"),
            stroke_width=6,
        )
        self.lens_fill = Circle(
            radius=radius,
            stroke_width=0,
            fill_opacity=kwargs.get("fill_opacity", 0.1),
            fill_color=kwargs.get("fill_color", RED),
        )

        # Create the handle as a line with thickness
        handle_start = DOWN * radius
        handle_end = DOWN * (radius + handle_length)

        self.handle = Line(
            start=handle_start,
            end=handle_end,
            color=handle_color,
            stroke_width=12,
        ).set_z_index(-1)

        # Add all parts to the VMobject
        self.add(self.handle, self.lens, self.lens_fill).set_z_index(5)


class Laptop(VMobject):
    def __init__(self, width=3.0, height=2.0, thickness=0.1, **kwargs):
        super().__init__(**kwargs)

        self.width = width
        self.height = height
        self.thickness = thickness

        # Create the base (bottom part with keyboard)
        self.base = Rectangle(
            width=width, height=height * 0.6, color=GRAY, fill_opacity=1, stroke_width=2
        )

        # Create the screen (top part)
        self.screen = Rectangle(
            width=width * 0.9,
            height=height * 0.8,
            color=WHITE,  # BLACK,
            fill_opacity=1,
            stroke_color=GRAY,
            stroke_width=3,
        )

        # Create the screen bezel/frame
        self.screen_frame = Rectangle(
            width=width * 0.95,
            height=height * 0.85,
            color=DARK_GRAY,
            fill_opacity=1,
            stroke_width=2,
        )

        # Position screen above base (open laptop)
        self.screen_frame.next_to(self.base, UP, buff=0)
        self.screen.move_to(self.screen_frame.get_center())

        # Create keyboard representation
        self.keyboard = VGroup()
        rows = 4
        keys_per_row = 12
        key_size = 0.15

        for row in range(rows):
            for col in range(keys_per_row):
                key = Rectangle(
                    width=key_size,
                    height=key_size,
                    color=WHITE,
                    fill_opacity=0.8,
                    stroke_width=1,
                    stroke_color=GRAY,
                )
                key.move_to(
                    self.base.get_center()
                    + LEFT * (keys_per_row - 1) * key_size * 0.6
                    + RIGHT * col * key_size * 1.2
                    + UP * (rows - 1) * key_size * 0.3
                    - DOWN * row * key_size * 0.6
                )
                self.keyboard.add(key)

        # Create trackpad
        self.trackpad = Rectangle(
            width=width * 0.2,
            height=height * 0.15,
            color=DARK_GRAY,
            fill_opacity=0.5,
            stroke_width=1,
        )
        self.trackpad.move_to(self.base.get_center() + DOWN * height * 0.15)

        # Add all parts to the VMobject
        self.add(
            self.base, self.screen_frame, self.screen, self.keyboard, self.trackpad
        )
