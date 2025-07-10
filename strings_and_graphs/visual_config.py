from manim import *


config.pixel_height = 1300
config.pixel_width = 2000
config.frame_height = config.pixel_height / config.pixel_width * config.frame_width
# TODO: Inclusion of the above line results in clippage of the rounded
# corners from all directions (vs clippage only from left and right)


BINARY_STRING_WHITE = "#f1f2f2"
BINARY_STRING_BLACK = "#61786c"

DARK_BLUE = "#395385"
MEDIUM_BLUE = "#4c8095"
LIGHT_BLUE = "#9acecc"

MEDIUM_GREEN = "#698857"

BRIGHT_RED = "#b84a54"
MEDIUM_RED = "#91463d"

MEDIUM_YELLOW = "#daa538"

PLOT_COLOR = MEDIUM_BLUE

STROKE_COLOR = "#22323b"
Mobject.set_default(color=STROKE_COLOR)

ARROW_TIP_WIDTH = 0.25

def add_background_rectangle(self, config):
    background_color = "#dce2e1"
    bg_radius_in_pixels = 125
    # Manim clips things by about this much when border-aligned
    unclip = 0.015
    radius = bg_radius_in_pixels / \
            config.pixel_width * config.frame_width

    tlc = Circle(
            color=background_color,
            fill_color=background_color,
            fill_opacity=1,
            radius=radius)
    tlc.align_on_border(UP, buff=unclip)
    tlc.align_on_border(LEFT, buff=unclip)

    trc = tlc.copy()
    trc.align_on_border(RIGHT, buff=unclip)

    blc = tlc.copy()
    blc.align_on_border(DOWN, buff=unclip)

    brc = trc.copy()
    brc.align_on_border(DOWN, buff=unclip)

    tall_r = Rectangle(
            color=background_color,
            fill_color=background_color,
            fill_opacity=1,
            width=config.frame_width - radius * 2,
            height=config.frame_height)

    wide_r = Rectangle(
            color=background_color,
            fill_color=background_color,
            fill_opacity=1,
            width=config.frame_width,
            height=config.frame_height - radius * 2)

    self.add(tall_r)
    self.add(wide_r)
    self.add(tlc)
    self.add(trc)
    self.add(blc)
    self.add(brc)
