from functools import reduce
import os, sys

# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *

from .visual_config import STROKE_COLOR, BINARY_STRING_WHITE, BINARY_STRING_BLACK


# This is a modification of Polygram#round_corners.
def round_some_corners(self, corners_to_round, radius: float = 0.5):
    all_vertices = reduce(
        lambda el1, el2: len(el1) + len(el2), self.get_vertex_groups()
    )
    assert len(corners_to_round) == len(all_vertices)

    if radius == 0:
        return self

    new_points = []

    for vertices in self.get_vertex_groups():
        former_corners = []
        for index, (v1, v2, v3) in enumerate(adjacent_n_tuples(vertices, 3)):
            if corners_to_round[index]:
                vect1 = v2 - v1
                vect2 = v3 - v2
                unit_vect1 = normalize(vect1)
                unit_vect2 = normalize(vect2)

                angle = angle_between_vectors(vect1, vect2)
                # Negative radius gives concave curves
                angle *= np.sign(radius)

                # Distance between vertex and start of the arc
                cut_off_length = radius * np.tan(angle / 2)

                # Determines counterclockwise vs. clockwise
                sign = np.sign(np.cross(vect1, vect2)[2])

                arc = ArcBetweenPoints(
                    v2 - unit_vect1 * cut_off_length,
                    v2 + unit_vect2 * cut_off_length,
                    angle=sign * angle,
                )
                former_corners.append(arc)
            else:
                former_corners.append(v2)

        # To ensure that we loop through starting with last
        former_corners = [former_corners[-1], *former_corners[:-1]]
        from manim.mobject.geometry.line import Line

        for corn1, corn2 in adjacent_pairs(former_corners):
            if hasattr(corn1, "points") and hasattr(corn2, "points"):
                new_points.extend(corn1.points)

                line = Line(corn1.get_end(), corn2.get_start())

                # Make sure anchors are evenly distributed
                len_ratio = line.get_length() / corn1.get_arc_length()

                line.insert_n_curves(int(corn1.get_num_curves() * len_ratio))

                new_points.extend(line.points)
            elif hasattr(corn1, "points") and not hasattr(corn2, "points"):
                new_points.extend(corn1.points)
                line = Line(corn1.get_end(), corn2)
                new_points.extend(line.points)
            elif not hasattr(corn1, "points") and hasattr(corn2, "points"):
                line = Line(corn1, corn2.get_start())
                new_points.extend(line.points)
                new_points.extend(corn2.points)
            else:  # both are points
                line = Line(corn1, corn2)
                new_points.extend(line.points)

    self.set_points(new_points)

    return self


Polygram.round_some_corners = round_some_corners

UP = [True, False, False, True]
DOWN = [False, True, True, False]
LEFT = [True, True, False, False]
RIGHT = [False, False, True, True]


class BinaryStringBit(Square):
    def __init__(
        self,
        value=None,
        zero_color=BINARY_STRING_WHITE,
        one_color=BINARY_STRING_BLACK,
        **kwargs,
    ):
        super().__init__(
            color=STROKE_COLOR,
            fill_opacity=1,
            stroke_width=kwargs.get("stroke_width", 3),
            **kwargs,
        )

        if value == 0:
            fill_color = zero_color
        elif value == 1:
            fill_color = one_color
        else:
            fill_color = None

        self.set_fill(fill_color)


class BinaryStringEnd(BinaryStringBit):
    def __init__(self, direction=UP, radius=0.5, **kwargs):
        super().__init__(**kwargs)

        self.round_some_corners(
            corners_to_round=direction,
            radius=radius,
        )


class BinaryString(VGroup):
    def __init__(
        self,
        binary_string,
        zero_color=BINARY_STRING_WHITE,
        one_color=BINARY_STRING_BLACK,
        spacing=0,
        corner_radius=0.5,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.binary_string = str(binary_string)
        self.zero_color = zero_color
        self.one_color = one_color
        self.spacing = spacing
        self.corner_radius = corner_radius

        # Create the binary string visualization
        self._create_binary_string()

    def _create_binary_string(self):
        """Create the visual representation of the binary string"""
        if not self.binary_string:
            return

        bits = []

        for i, bit_char in enumerate(self.binary_string):
            # Convert character to integer, handle invalid characters
            try:
                bit_value = int(bit_char)
                if bit_value not in [0, 1]:
                    raise ValueError(f"Invalid bit value: {bit_value}")
            except ValueError:
                # Skip invalid characters or treat them as None
                bit_value = None

            # Create appropriate bit based on position
            if i == 0:
                # First bit - round top corners
                bit = BinaryStringEnd(
                    value=bit_value,
                    direction=UP,
                    radius=self.corner_radius,
                    zero_color=self.zero_color,
                    one_color=self.one_color,
                )
            elif i == len(self.binary_string) - 1:
                # Last bit - round bottom corners
                bit = BinaryStringEnd(
                    value=bit_value,
                    direction=DOWN,
                    radius=self.corner_radius,
                    zero_color=self.zero_color,
                    one_color=self.one_color,
                )
            else:
                # Middle bits - no rounded corners
                bit = BinaryStringBit(
                    value=bit_value,
                    zero_color=self.zero_color,
                    one_color=self.one_color,
                )

            bits.append(bit)

        # Arrange bits
        self.add(*bits)
        self.scale(0.11).arrange(direction=np.array([0, -1, 0]), buff=0)
