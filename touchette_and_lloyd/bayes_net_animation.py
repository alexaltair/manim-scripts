import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from strings_and_graphs.binary_string import BinaryString
from utils import *

BG_COLOR = "#dde3e1"
OUTER_COLOR = "#22333a"
X_NODE_COLOR = "#d77f87"
Y_NODE_COLOR = "#e0c181"
A_NODE_COLOR = "#a8c099"

# Binary string colors
X_ONE_COLOR = "#b8686e"
Y_ONE_COLOR = "#c3a55e"
A_ONE_COLOR = "#8ca37e"

config.background_color = BG_COLOR


class BayesNet(Scene):
    def construct(self):
        # Constants
        FAST_RUN_TIME = 1
        MED_RUN_TIME = 1.5
        SLOW_RUN_TIME = 2

        # Nodes
        x_node = create_node(fill_color=X_NODE_COLOR, label_shift=(-0.05, 0, 0))
        y_node = create_node(fill_color=Y_NODE_COLOR)
        a_node = create_node(fill_color=A_NODE_COLOR, label_shift=(-0.05, 0.1, 0))
        laptop_node = Laptop().scale(0.5)

        # Arrange nodes
        xlaptop_group = VGroup(x_node, laptop_node).arrange(buff=4)
        xlaptopa_group = VGroup(xlaptop_group, a_node).arrange(DOWN, buff=2)

        xlaptop_edge = add_edge(x_node, laptop_node, start_pos="right", end_pos="left")
        xa_edge = add_edge(x_node, a_node)
        alaptop_edge = add_edge(a_node, laptop_node)

        # Place the y node next to laptop base
        y_node.next_to(laptop_node.base, RIGHT, buff=0.1)

        # Move entire diagram to ORIGIN
        net_group = VGroup(
            xlaptopa_group, xlaptop_edge, xa_edge, alaptop_edge, y_node
        ).move_to(ORIGIN)

        # Add magnifying glass
        magnifying_glass = (
            MagnifyingGlass(
                radius=0.4, handle_length=0.7, fill_opacity=1, fill_color=BG_COLOR
            )
            .move_to(xa_edge.get_center())
            .shift(DOWN * 0.5)
            .rotate(-PI / 5)
        )
        magnifying_glass.lens_fill.set_z_index(-1)

        # Binay strings
        x_binary_string = BinaryString("10100", one_color=X_ONE_COLOR).move_to(x_node)
        binary_string_zoom = (
            x_binary_string.copy()
            .scale(1.5)
            .move_to(magnifying_glass.lens, aligned_edge=UP)
            .shift(DOWN * 0.1)
        )
        binary_string_zoom[2:].set_opacity(0)

        a_binary_string = BinaryString("10110", one_color=A_ONE_COLOR).move_to(a_node)
        y_binary_string = BinaryString("00010", one_color=Y_ONE_COLOR).move_to(y_node)
        y_binary_string.rotate(PI / 2)

        binary_string_screen = (
            VGroup(x_binary_string.copy(), a_binary_string.copy())
            .scale(0.5)
            .arrange(buff=0.1)
        )

        # f(x, a)
        f = VGroup(
            MathTex("f(").scale(0.65),
            binary_string_screen[0],
            MathTex(", ").scale(0.65),
            binary_string_screen[1],
            MathTex(")").scale(0.65),
        ).arrange(buff=0.1)
        f[2].shift(DOWN * 0.1)
        f.move_to(laptop_node.screen)

        # self.add(net_group, magnifying_glass, x_binary_string, a_binary_string, y_binary_string, binary_string_zoom, binary_string_screen)
        # return

        # Animations
        self.add(net_group, magnifying_glass)
        self.wait()

        # Fill the red node with a random 5-bit binary string
        self.play(Write(x_binary_string), run_time=MED_RUN_TIME)

        # The first copy moves downward toward the magnifying glass icon.
        binary_string_zoom.set_z_index(3)
        self.play(
            ReplacementTransform(x_binary_string.copy(), binary_string_zoom),
            run_time=SLOW_RUN_TIME,
        )

        # Copy the visible top 2 bits and move them into the green node.
        self.play(
            ReplacementTransform(binary_string_zoom[:2].copy(), a_binary_string[:2]),
            run_time=SLOW_RUN_TIME,
        )
        self.play(Write(a_binary_string[2:]), run_time=MED_RUN_TIME)

        # Move towards the computer
        self.play(
            ReplacementTransform(a_binary_string.copy(), binary_string_screen[-1]),
            run_time=MED_RUN_TIME,
        )

        # Fed the other copy into the computer
        self.play(
            ReplacementTransform(x_binary_string.copy(), binary_string_screen[0]),
            run_time=MED_RUN_TIME,
        )

        # Display f(x, a) on the screen
        self.play(FadeIn(f[0], f[2], f[-1]))

        # Bring the laptop to the front, but keep the text on screen
        laptop_node.set_z_index(1)
        f.set_z_index(2)

        # Print out the y string
        self.play(
            FadeIn(y_binary_string, target_position=laptop_node.base),
            run_time=MED_RUN_TIME,
        )

        # Fade out all binary strings
        self.play(
            *[
                FadeOut(obj)
                for obj in [
                    x_binary_string,
                    binary_string_zoom,
                    a_binary_string,
                    y_binary_string,
                    binary_string_screen,
                    f,
                ]
            ]
        )
