from manim import *

config.background_color = '#ffeae3'
TEXT_COLOR = DARK_GRAY
STROKE_WIDTH = 3

class AltairLogo(Scene):
    def construct(self):
        basic_unit = 1
        # big_A = Tex("A", color=TEXT_COLOR).scale(10)
        big_square = Square(side_length=4*basic_unit, color=TEXT_COLOR, stroke_width=STROKE_WIDTH)
        big_circle = Circle(radius=2*basic_unit, color=TEXT_COLOR, stroke_width=STROKE_WIDTH)

        horz_line = Line(
            big_square.get_corner(direction=RIGHT),
            big_square.get_corner(direction=LEFT),
            color=TEXT_COLOR,
            stroke_width=STROKE_WIDTH,
        )
        horz_line.shift(0.08*DOWN)

        vert_line = Line(
            big_square.get_corner(direction=UP),
            big_square.get_corner(direction=DOWN),
            color=TEXT_COLOR,
            stroke_width=STROKE_WIDTH,
        )

        diag_line1 = Line(
            big_square.get_corner(direction=UP+LEFT),
            big_square.get_corner(direction=DOWN+RIGHT),
            color=TEXT_COLOR,
            stroke_width=STROKE_WIDTH,
        )

        diag_line2 = Line(
            big_square.get_corner(direction=UP+RIGHT),
            big_square.get_corner(direction=DOWN+LEFT),
            color=TEXT_COLOR,
            stroke_width=STROKE_WIDTH,
        )

        top_circle = Circle(radius=0.44*basic_unit, color=TEXT_COLOR, stroke_width=STROKE_WIDTH)
        top_circle.shift(0.28*LEFT*basic_unit)
        top_circle.shift(big_square.get_top() + [0, top_circle.radius, 0])

        med_left_circle = Circle(radius=0.56*basic_unit, color=TEXT_COLOR, stroke_width=STROKE_WIDTH)
        med_left_circle.shift(2.12*LEFT*basic_unit)
        med_left_circle.shift(big_square.get_bottom() + [0, med_left_circle.radius, 0])

        med_right_circle = Circle(radius=0.52*basic_unit, color=TEXT_COLOR, stroke_width=STROKE_WIDTH)
        med_right_circle.shift(2.32*RIGHT*basic_unit)
        med_right_circle.shift(big_square.get_bottom() + [0, med_right_circle.radius, 0])


        small_left_circle = Circle(radius=med_left_circle.radius/2, color=TEXT_COLOR, stroke_width=STROKE_WIDTH)
        small_left_circle.shift(1.12*LEFT*basic_unit)
        small_left_circle.shift(big_square.get_bottom() + [0, small_left_circle.radius, 0])

        small_right_circle = Circle(radius=small_left_circle.radius, color=TEXT_COLOR, stroke_width=STROKE_WIDTH)
        small_right_circle.shift([-small_left_circle.get_x(), 0, 0])
        small_right_circle.shift(big_square.get_bottom() + [0, small_right_circle.radius, 0])






        shape = VMobject(
            fill_opacity=1,
            color=BLACK,
            fill_color=TEXT_COLOR,
            stroke_width=2,
        )

        shape.start_new_path(small_left_circle.get_bottom())
        shape.add_line_to(med_left_circle.get_bottom())
        arc1 = ArcBetweenPoints(
            start=med_left_circle.get_bottom(),
            end=med_left_circle.get_right()*[1, 1.1, 1], #CALIBRATE
            radius=med_left_circle.radius,
        )
        for path in arc1.get_subpaths():
            shape.add_subpath(path)
        top_circle_almost_bottom = top_circle.get_bottom()*[0.7, 1, 1] #CALIBRATE
        shape.add_line_to(top_circle_almost_bottom)
        arc2 = ArcBetweenPoints(
            start=top_circle_almost_bottom,
            end=top_circle.get_right()*[0.7, 0.9, 1], #CALIBRATE
            radius=top_circle.radius,
        )
        for path in arc2.get_subpaths():
            shape.add_subpath(path)
        med_right_circle_almost_left = med_right_circle.get_left()*[1, 1.08, 1] #CALIBRATE
        shape.add_line_to(med_right_circle_almost_left)
        arc3 = ArcBetweenPoints(
            start=med_right_circle_almost_left,
            end=med_right_circle.get_bottom(),
            radius=med_right_circle.radius,
        )
        for path in arc3.get_subpaths():
            shape.add_subpath(path)
        shape.add_line_to(small_right_circle.get_bottom())
        arc4 = ArcBetweenPoints(
            start=small_right_circle.get_bottom(),
            end=small_right_circle.get_right()*[0.97, 0.9, 1], #CALIBRATE
            radius=small_right_circle.radius,
        )
        for path in arc4.get_subpaths():
            shape.add_subpath(path)
        crossbar_bottom = -0.2*basic_unit
        shape.add_line_to(ORIGIN+[0.6*small_right_circle.get_center()[0], crossbar_bottom, 0]) #CALIBRATE
        shape.add_line_to(ORIGIN+[0.7*small_left_circle.get_center()[0], crossbar_bottom, 0]) #CALIBRATE
        small_left_circle_almost_left = small_left_circle.get_left()*[0.97, 0.9, 1] #CALIBRATE
        shape.add_line_to(small_left_circle_almost_left)
        arc5 = ArcBetweenPoints(
            start=small_left_circle_almost_left,
            end=small_left_circle.get_bottom(),
            radius=small_left_circle.radius,
        )
        for path in arc5.get_subpaths():
            shape.add_subpath(path)


        triangle_top = 1.7*UP*basic_unit + 0.1*LEFT*basic_unit #CALIBRATE
        crossbar_top = 0.08*DOWN*basic_unit #CALIBRATE
        shape.start_new_path(triangle_top)
        shape.add_line_to(0.75*LEFT*basic_unit + crossbar_top) #CALIBRATE
        shape.add_line_to(0.65*RIGHT*basic_unit + crossbar_top) #CALIBRATE
        shape.add_line_to(triangle_top)









        self.play(
            AnimationGroup(
                Create(big_square),
                Create(big_circle),
                Create(diag_line1),
                Create(vert_line),
                Create(diag_line2),
                Create(horz_line),
                Create(top_circle),
                Create(med_left_circle),
                Create(small_left_circle),
                Create(small_right_circle),
                Create(med_right_circle),
                DrawBorderThenFill(
                    shape,
                    stroke_width=2,
                    run_time=4,
                    # draw_border_animation_config={'run_time': 8},
                ),
                lag_ratio=0.1,
            )
        )







        self.wait()
