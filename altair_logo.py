from manim import *

config.background_color = '#ffeae3'
TEXT_COLOR = DARK_GRAY

class AltairLogo(Scene):
    def construct(self):
        basic_unit = 4
        # big_A = Tex("A", color=TEXT_COLOR).scale(10)
        big_square = Square(side_length=basic_unit, color=TEXT_COLOR)
        big_circle = Circle(radius=basic_unit/2, color=TEXT_COLOR)

        horz_line = Line(
            big_square.get_corner(direction=RIGHT),
            big_square.get_corner(direction=LEFT),
            color=TEXT_COLOR,
        )
        horz_line.shift(0.08*DOWN)

        vert_line = Line(
            big_square.get_corner(direction=UP),
            big_square.get_corner(direction=DOWN),
            color=TEXT_COLOR,
        )

        diag_line1 = Line(
            big_square.get_corner(direction=UP+LEFT),
            big_square.get_corner(direction=DOWN+RIGHT),
            color=TEXT_COLOR,
        )

        diag_line2 = Line(
            big_square.get_corner(direction=UP+RIGHT),
            big_square.get_corner(direction=DOWN+LEFT),
            color=TEXT_COLOR,
        )

        top_circle = Circle(radius=basic_unit/9, color=TEXT_COLOR)
        top_circle.shift(0.07*LEFT*basic_unit)
        top_circle.shift(big_square.get_top() + [0, top_circle.radius, 0])

        med_left_circle = Circle(radius=0.14*basic_unit, color=TEXT_COLOR)
        med_left_circle.shift(0.53*LEFT*basic_unit)
        med_left_circle.shift(big_square.get_bottom() + [0, med_left_circle.radius, 0])

        med_right_circle = Circle(radius=0.13*basic_unit, color=TEXT_COLOR)
        med_right_circle.shift(0.58*RIGHT*basic_unit)
        med_right_circle.shift(big_square.get_bottom() + [0, med_right_circle.radius, 0])


        small_left_circle = Circle(radius=med_left_circle.radius/2, color=TEXT_COLOR)
        small_left_circle.shift(0.28*LEFT*basic_unit)
        small_left_circle.shift(big_square.get_bottom() + [0, small_left_circle.radius, 0])

        small_right_circle = Circle(radius=small_left_circle.radius, color=TEXT_COLOR)
        small_right_circle.shift([-small_left_circle.get_x(), 0, 0])
        small_right_circle.shift(big_square.get_bottom() + [0, small_right_circle.radius, 0])


        self.play(
            # Write(big_A),
            Create(big_square),
            Create(big_circle),
            Create(horz_line),
            Create(vert_line),
            Create(diag_line1),
            Create(diag_line2),
            Create(top_circle),
            Create(med_left_circle),
            Create(med_right_circle),
            Create(small_left_circle),
            Create(small_right_circle),
        )

        self.wait()
