from manim import *
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from visual_config import add_background_rectangle
import visual_config as vg
import binary_string as bs

MARGIN = 0.9
MAX_BUFFER = 0.55

MAX_FRAME_WIDTH = config.frame_width - MARGIN * 2

MIN_WORD_ZONE_WIDTH = 1

MAX_FONT_SIZE = 60

PNG_WIDTH = 300
PNG_HEIGHT = 340
REAL_MEEPLE = 32

STROKE_WIDTH = 4.3

ELLIPSIS_SIZE_MULTIPLIER = 0.6

DOUBLINGS = 6

QUESTIONS = ["Glasses?", "Red shirt?", "Short hair?", "Light hair?", "Hat?", ""]
label_list = []

initial_frame_width = 0
initial_word_zone_width = 0
max_meeple_width = 0

bit_list_2d = [[] for _ in range(DOUBLINGS)]


# Given n, generate the binary strings for the first 2^n meeple that
# should be displayed.
def get_meeple_in_power(n, m=DOUBLINGS):
    if m < 0:
        return [""]
    if n < 1:
        return ["0" * m]
    binary_strings = []
    mip = get_meeple_in_power(n - 1, m - 1)
    for binary_string in mip:
        binary_strings.append("0" + binary_string)
    for binary_string in mip:
        binary_strings.append("1" + binary_string)
    return binary_strings


def create_binary_mobjects(binary):
    bit_list = []
    for i, bit in enumerate(binary):
        size_multiplier = 1

        if bit == "1":
            value = True
        else:
            value = False
        if i == 0:
            bit_list.append(bs.BinaryStringEnd(value=value, direction=bs.UP))
        elif i == len(binary) - 1:
            dot = Dot(color=vg.STROKE_COLOR)
            ellipsis = VGroup(dot, Mobject.copy(dot), Mobject.copy(dot))
            ellipsis.arrange_submobjects()
            ellipsis.rotate_about_origin(90 * DEGREES)
            bit_list.append(ellipsis)
            size_multiplier = ELLIPSIS_SIZE_MULTIPLIER
        else:
            bit_list.append(bs.BinaryStringBit(value=value))
        bit_list[i].scale_to_fit_height(max_binary_string_width * size_multiplier)
        bit_list[i].set_opacity(0)
        bit_list_2d[i].append(bit_list[i])
    return bit_list


def get_coords_by_stage(meeple, meeple_list, n, frame_width):
    index = meeple_list.index(meeple)

    ratio = get_ratio_by_stage(n, frame_width)

    m_width = ratio * max_meeple_width
    m_height = m_width / PNG_WIDTH * PNG_HEIGHT
    start = MAX_FRAME_WIDTH / 2 - frame_width + m_width / 2
    x = start + index * m_width

    # Do the equivalent of align_to_border(UP, buff=MARGIN)
    y = config.frame_height / 2 - MARGIN * 2 - m_height / 2
    meeple_coords = [x, y, 0]

    b_width = ratio * max_binary_string_width
    buffer = ratio * MAX_BUFFER
    bit_coords = []
    start_bit_y = meeple_coords[1] - m_width / 2 - buffer - b_width / 2
    bit_coords.append([x, start_bit_y, 0])
    for i in range(1, DOUBLINGS):
        y = start_bit_y - b_width * i
        bit_coords.append([x, y, 0])

    return meeple_coords, bit_coords


def get_label_coords_by_stage(n, frame_width):
    ratio = get_ratio_by_stage(n, frame_width)

    m_width = ratio * max_meeple_width
    m_height = m_width / PNG_WIDTH * PNG_HEIGHT

    # Do the equivalent of align_to_border(UP, buff=MARGIN)
    meeple_y = config.frame_height / 2 - MARGIN * 2 - m_height / 2

    b_width = ratio * max_binary_string_width
    buffer = ratio * MAX_BUFFER
    start_label_y = meeple_y - m_width / 2 - buffer - b_width / 2
    label_coords = [[0, start_label_y, 0]]
    for i in range(1, len(QUESTIONS)):
        y = start_label_y - b_width * i
        label_coords.append([0, y, 0])

    return label_coords


def get_ratio_by_stage(n, frame_width):
    current_meeple_width = min(frame_width / (2**n), max_meeple_width)
    return current_meeple_width / max_meeple_width


def frame_to_word_zone(frame_width):
    return MAX_FRAME_WIDTH - MARGIN / 2 - frame_width


def word_zone_to_frame(word_zone_width):
    return MAX_FRAME_WIDTH - MARGIN / 2 - word_zone_width


# Scale down all labels given that the longest label must match the
# new word zone width
def get_label_widths(frame_width):
    new_width = frame_to_word_zone(frame_width)
    widest_label_width = 0
    for label in label_list:
        widest_label_width = max(widest_label_width, label.width)
    ratio = new_width / widest_label_width
    label_widths = []
    for label in label_list:
        label_widths.append(ratio * label.width)
    return label_widths


def get_bit_size_by_stage(n, frame_width):
    ratio = get_ratio_by_stage(n, frame_width)
    bit_width = ratio * max_binary_string_width
    stroke_width = ratio * STROKE_WIDTH

    return bit_width, stroke_width


def create_meeple_mobject(binary):
    decimal = int(binary[::-1], 2) + 1
    if decimal <= REAL_MEEPLE:
        return ImageMobject("assets/meeple-margins/m-{:02d}.png".format(decimal))
    else:
        return ImageMobject(
            "assets/meeple-margins/m-{:02d}.png".format(random.randint(1, REAL_MEEPLE))
        )


def create_meeple_mobject_dict(meeple_list):
    mdict = {}
    for i in range(len(meeple_list)):
        meeple = create_meeple_mobject(meeple_list[i])
        binary_string = create_binary_mobjects(meeple_list[i])
        mdict[meeple_list[i]] = (meeple, binary_string)
    return mdict


def move_old_labels(n, frame_width):
    move_anims = []

    label_coords = get_label_coords_by_stage(n, frame_width)
    label_widths = get_label_widths(frame_width)

    if frame_width < MAX_FRAME_WIDTH:
        # Move to a new location and scale down
        for i, label in enumerate(label_list[:DOUBLINGS]):
            move_anims.append(
                label.animate.set(width=label_widths[i])
                .move_to(label_coords[i], coor_mask=[0, 1, 0])
                .align_on_border(LEFT, buff=MARGIN)
            )
    else:
        # Move offscreen and scale down
        x_coord_barely_offscreen = -1 * (
            config.frame_width / 2 + initial_word_zone_width
        )
        for i, label in enumerate(label_list[:DOUBLINGS]):
            move_anims.append(
                label.animate.set(width=label_widths[i]).move_to(
                    [x_coord_barely_offscreen, label_coords[i][1], 0],
                    coor_mask=[1, 1, 0],
                )
            )

    return move_anims


def move_old_meeple_and_bits(meeple_dict, meeple_list, n, frame_width):
    move_anims = []

    m_width = get_ratio_by_stage(n, frame_width) * max_meeple_width
    b_width, stroke_width = get_bit_size_by_stage(n, frame_width)

    # Move and scale meeple and bits
    for m in meeple_dict.keys():
        meeple_coords, bit_coords = get_coords_by_stage(m, meeple_list, n, frame_width)

        move_anims.append(
            meeple_dict[m][0].animate.scale_to_fit_width(m_width).move_to(meeple_coords)
        )

        for i, bit in enumerate(meeple_dict[m][1]):
            size_multiplier = 1
            if i == DOUBLINGS - 1:
                size_multiplier = ELLIPSIS_SIZE_MULTIPLIER

            move_anims.append(
                bit.animate.scale_to_fit_height(b_width * size_multiplier)
                .set(stroke_width=stroke_width)
                .move_to(bit_coords[i])
            )

    return move_anims


def add_x_axis(self, frame_width):
    x_axis = NumberLine(length=frame_width, include_numbers=True, x_range=[0, 1])
    center = config.frame_width / 2 - frame_width / 2 - MARGIN
    x_axis.move_to([center, 0, 0])
    x_axis.align_on_border(UP, buff=MARGIN)
    self.add(x_axis)
    return x_axis


def expand_x_axis(x_axis, n, frame_width):
    center = config.frame_width / 2 - frame_width / 2 - MARGIN

    new_x_axis = NumberLine(length=frame_width, include_numbers=True, x_range=[0, 1])
    new_x_axis.move_to([center, 0, 0])
    new_x_axis.align_on_border(UP, buff=MARGIN)

    return Transform(x_axis, new_x_axis)


def move_old(meeple_dict, meeple_list, n, frame_width, x_axis):
    move_anims = []
    move_anims.extend(
        move_old_meeple_and_bits(meeple_dict, meeple_list, n, frame_width)
    )
    move_anims.extend(move_old_labels(n, frame_width))
    move_anims.append(expand_x_axis(x_axis, n, frame_width))
    return move_anims


def fade_in_new(new_md, n):
    fade_in_anims = []
    for m in new_md.keys():
        fade_in_anims.append(new_md[m][0].animate.set_opacity(1))
    for row in range(n):
        for bit in bit_list_2d[row]:
            fade_in_anims.append(bit.animate.set_opacity(1))
        fade_in_anims.append(label_list[row].animate.set_opacity(1))
    return fade_in_anims


def define_initial_dimensions():
    word_zone_width = 0
    for question in QUESTIONS:
        with register_font("SourceSerifPro-Regular.ttf"):
            label = Text(
                question,
                font_size=MAX_FONT_SIZE,
                font="Source Serif Pro",
                should_center=False,
            ).set_opacity(0)
        label_list.append(label)
        word_zone_width = max(label.width, word_zone_width)

    # Define initial dimensions
    global initial_word_zone_width
    initial_word_zone_width = word_zone_width

    global initial_frame_width
    initial_frame_width = word_zone_to_frame(word_zone_width)

    global max_meeple_width
    max_meeple_width = initial_frame_width / 4

    global max_binary_string_width
    max_binary_string_width = max_meeple_width * 4 / 5

    return initial_frame_width


def update_frame_width(n, frame_width):
    ratio = get_ratio_by_stage(n, frame_width)
    word_zone_width = ratio * initial_word_zone_width

    if word_zone_width >= MIN_WORD_ZONE_WIDTH:
        frame_width = word_zone_to_frame(word_zone_width)
    else:
        frame_width = MAX_FRAME_WIDTH

    return frame_width


def add_label(self, n, frame_width):
    if n < DOUBLINGS and n > 0:
        label_coords = get_label_coords_by_stage(n, frame_width)
        label_y = label_coords[n][1]

        # Add label at the right y position and size
        label_list[n].set_opacity(0)
        self.add(label_list[n])


def add_meeple_stage(self, n, meeple_dict, frame_width):
    meeple_list = get_meeple_in_power(n)

    old_ml = list(meeple_dict.keys())
    new_ml = [m for m in meeple_list if m not in old_ml]
    new_md = create_meeple_mobject_dict(new_ml)

    m_width = get_ratio_by_stage(n, frame_width) * max_meeple_width
    b_width, stroke_width = get_bit_size_by_stage(n, frame_width)

    # Add meeple and bits at the right position, size, and stroke width
    for m in new_md.keys():
        # Place and scale new individual meeple
        meeple_coords, bit_coords = get_coords_by_stage(m, meeple_list, n, frame_width)
        new_md[m][0].move_to(meeple_coords)
        if n != 0:
            new_md[m][0].set_opacity(0)
        new_md[m][0].scale_to_fit_width(m_width)
        self.add(new_md[m][0])

        # Place and scale new individual meeple's bits
        for i, bit in enumerate(new_md[m][1]):
            size_multiplier = 1
            if i == DOUBLINGS - 1:
                size_multiplier = ELLIPSIS_SIZE_MULTIPLIER

            bit.move_to(bit_coords[i])
            bit.scale_to_fit_height(b_width * size_multiplier)
            bit.set(stroke_width=stroke_width)
            self.add(bit)

    return new_md, meeple_list


def add_all_meeple_stages(self):
    frame_width = define_initial_dimensions()
    x_axis = add_x_axis(self, frame_width)
    add_label(self, 0, frame_width)
    meeple_dict, meeple_list = add_meeple_stage(self, 0, {}, frame_width)

    for n in range(1, 1 + DOUBLINGS):
        frame_width = update_frame_width(n, frame_width)
        add_label(self, n, frame_width)
        new_md, meeple_list = add_meeple_stage(self, n, meeple_dict, frame_width)
        self.play(*move_old(meeple_dict, meeple_list, n, frame_width, x_axis))
        self.play(*fade_in_new(new_md, n))

        meeple_dict.update(new_md)


class InfiniteMeeple(Scene):
    def construct(self):
        add_background_rectangle(self, config)
        add_all_meeple_stages(self)
        self.wait()
