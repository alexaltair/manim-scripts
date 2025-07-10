from manim import *

OUTER_COLOR = "#22333a"
N_NODE_COLOR = "#d77f87"
X_NODE_COLOR = "#d49971"
S_NODE_COLOR = "#e0c181"
R_NODE_COLOR = "#a8c099"
Z_NODE_COLOR = "#9acfcd"

config.background_color = "#dde3e1"

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

def add_edge(node1, node2, start_pos=None, end_pos=None, color=OUTER_COLOR, tip_length=0.2):
    node1_ring = Circle(radius=node1.width / 2 + 0.05).move_to(node1)
    node2_ring = Circle(radius=node2.width / 2 + 0.03).move_to(node2)

    start_dict = {
        "top_right": node1[0].get_end() + 0.2 * UP + 0.2 * LEFT,
        "bottom_right": node1[0].get_end() + 0.2 * DOWN + 0.2 * LEFT,
        "right": node1.get_right() + 0.2 * LEFT
    }

    end_dict = {
        "top_left": node2[0].get_start() + 1.34 * LEFT + 0.4 * UP,
        "bottom_left": node2[0].get_start() + 1.42 * LEFT + 0.2 * DOWN,
        "left": node2.get_left() + 0.05 * LEFT
    }

    edge = Arrow(
        start=start_dict[start_pos] if start_pos else node1.get_center(),
        end=end_dict[end_pos] if end_pos else node2_ring,
        buff=0,
        tip_shape=StealthTip,
        tip_length=tip_length
    ).set_color(color)
    edge.set_z_index(-1)

    return edge

class BayesNetNew(Scene):
    def construct(self):
        x_node = create_node(fill_color=N_NODE_COLOR, label="X", label_shift=(-0.05, 0, 0))
        y_node = create_node(fill_color=S_NODE_COLOR, label="Y")
        a_node = create_node(fill_color=R_NODE_COLOR, label="A", label_shift=(-0.05, 0.1, 0))

        xy_group = VGroup(x_node, y_node).arrange(buff=2.5)
        xya_group = VGroup(xy_group, a_node).arrange(DOWN, buff=1)

        xy_edge = add_edge(x_node, y_node, start_pos="right", end_pos="left")
        xa_edge = add_edge(x_node, a_node)
        ay_edge = add_edge(a_node, y_node)

        left_group = VGroup(xya_group, xy_edge, xa_edge, ay_edge)
        right_group = left_group.copy()

        left_group[2].set_opacity(0)

        full_group = VGroup(left_group, right_group).arrange(buff=1.5)

        left_group_caption = Tex("(a) A blind policy", color=OUTER_COLOR).next_to(left_group, DOWN, buff=0.8)
        right_group_caption = Tex("(b) A sighted policy", color=OUTER_COLOR).next_to(right_group, DOWN, buff=0.8)

        VGroup(full_group, left_group_caption, right_group_caption).move_to(ORIGIN)

        self.add(full_group, left_group_caption, right_group_caption)


class BarChartNew(Scene):
    def construct(self):
        CAPTION_FONT_SIZE = 42
        AXES_FONT_SIZE = 28
        LABELS_FONT_SIZE = 32
        CAPTION_BUFF = 0.4

        chart = BarChart(
            values=[4.94, 4.85, 4.63, 4.11, 2.83, 0],
            bar_names=[0, 1, 2, 3, 4, 5],
            y_range=[0, 6, 2],
            bar_colors=[N_NODE_COLOR, X_NODE_COLOR, S_NODE_COLOR, R_NODE_COLOR, Z_NODE_COLOR],
            bar_fill_opacity=0.8,
            y_axis_config={
                "numbers_to_include": [0, 2, 4, 6],
                "numbers_to_exclude": [],
                "font_size": AXES_FONT_SIZE
            },
        ).scale(1.2)
        chart.axes.set_color(OUTER_COLOR)

        labels = chart.get_bar_labels(color=OUTER_COLOR, label_constructor=MathTex, font_size=LABELS_FONT_SIZE)

        x_label = Tex("Number of Bits Known", font_size=CAPTION_FONT_SIZE).next_to(chart, DOWN, buff=CAPTION_BUFF)
        y_label = Tex("Output Entropy", font_size=CAPTION_FONT_SIZE).rotate(PI/2).next_to(chart, LEFT, buff=CAPTION_BUFF)
        axes_labels = VGroup(x_label, y_label).set_color(OUTER_COLOR)

        full_chart = VGroup(chart, labels, axes_labels).scale(1.1).move_to(ORIGIN)

        self.add(full_chart)
