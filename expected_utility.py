import random

from manim import *

config.background_color = '#ffeae3'
TEXT_COLOR = DARK_GRAY
PHI = (1 + 5**0.5)/2

class InitialBoxes(Scene):
    def create_initial_box_stuff(self, box, p1, p2, d1, d2, h1):
        prob_line = UnitInterval(
            unit_size=4,
            # tick_frequency=0,
            include_ticks=False,
        )
        prob_line.shift([box.get_x(), -1, 0])
        line1 = float(p1)*(prob_line.get_right() - prob_line.get_left())
        mid = prob_line.get_left() + line1

        brace1 = BraceBetweenPoints(
            prob_line.get_left(),
            mid,
            color=TEXT_COLOR,
        )
        brace_txt1 = Tex(p1, color=TEXT_COLOR)
        brace_txt1.next_to(brace1, DOWN)

        rect1 = Rectangle(width=line1[0], height=h1, color=TEXT_COLOR)
        rect1.next_to(brace1, UP)

        dollars1 = Tex(d1, color=TEXT_COLOR)
        dollars1.next_to(rect1, UP)


        brace2 = BraceBetweenPoints(
            mid,
            prob_line.get_right(),
            color=TEXT_COLOR,
        )
        brace_txt2 = Tex(p2, color=TEXT_COLOR)
        brace_txt2.next_to(brace2, DOWN)

        dollars2 = Tex(d2, color=TEXT_COLOR)
        dollars2.next_to(brace2, UP)


        self.play(
            Create(prob_line),
            Write(brace1),
            Write(brace_txt1),
            Create(rect1),
            Write(dollars1),
            Write(brace2),
            Write(brace_txt2),
            Write(dollars2),
        )

        return (
            prob_line,
            brace1,
            brace_txt1,
            rect1,
            dollars1,
            brace2,
            brace_txt2,
            dollars2,
        )

    def construct(self):
        choice = Tex("Choose between:", color=TEXT_COLOR)
        choice.to_corner(UP + LEFT)
        self.play(Write(choice))
        # self.wait()



        a_box = (
            Rectangle(width=PHI, height=1, color=TEXT_COLOR)
        )
        a_box.shift(LEFT*3)
        a_box_label = Tex("A", color=TEXT_COLOR)
        a_box_label.shift(a_box.get_center())

        b_box = Rectangle(width=PHI, height=1, color=TEXT_COLOR)
        b_box.shift(RIGHT*3)
        b_box_label = Tex("B", color=TEXT_COLOR)
        b_box_label.shift(b_box.get_center())

        self.play(
            Create(a_box),
            Write(a_box_label),
            Create(b_box),
            Write(b_box_label),
        )
        self.wait()

        a_box = Group(a_box, a_box_label)
        b_box = Group(b_box, b_box_label)

        self.play(
            a_box.animate.shift(DOWN*3),
            b_box.animate.shift(DOWN*3),
        )


        (
            a_prob_line,
            a_brace1,
            a_brace_txt1,
            a_rect1,
            a_dollars1,
            a_brace2,
            a_brace_txt2,
            a_dollars2,
        ) = self.create_initial_box_stuff(
            box=a_box,
            p1="0.25",
            p2="0.75",
            d1="\$100",
            d2="\$0",
            h1=1,
        )

        (
            b_prob_line,
            b_brace1,
            b_brace_txt1,
            b_rect1,
            b_dollars1,
            b_brace2,
            b_brace_txt2,
            b_dollars2,
        ) = self.create_initial_box_stuff(
            box=b_box,
            p1="0.1",
            p2="0.9",
            d1="\$300",
            d2="\$0",
            h1=3,
        )






        self.wait()



def random_ev_params():
    d1 = random.randrange(1000)
    d2 = random.randrange(1000)

    p1 = round(random.uniform(0, 1), 2)
    p2 = round(1 - p1, 2)
    assert p1 + p2 == 1

    ev = d1*p1 + d2+p2
    return Tex(fr"$\${d1} \cdot {p1} + \${d2} \cdot {p2}$", color=TEXT_COLOR)


class RandomBoxes(Scene):
    def construct(self):
        a_box = Rectangle(
            width=PHI,
            height=1,
            color=BLUE,
            fill_opacity=1,
        ).add(Tex("A", color=TEXT_COLOR))
        a_box.shift(LEFT*3 + DOWN*2)

        b_box = Rectangle(width=PHI, height=1, color=TEXT_COLOR).add(Tex("B", color=TEXT_COLOR))
        b_box.shift(RIGHT*3 + DOWN*2)

        self.play(
            Create(a_box),
            Create(b_box),
        )

        a_rand_params = random_ev_params()
        a_rand_params.scale(0.2)

        b_rand_params = random_ev_params()
        b_rand_params.scale(0.2)

        self.play(
            ScaleInPlace(a_rand_params, 4),
            MoveAlongPath(
                a_rand_params,
                Line(a_box.get_center(), a_box.get_center() + UP*3)
            ),
            ScaleInPlace(b_rand_params, 4),
            MoveAlongPath(
                b_rand_params,
                Line(b_box.get_center(), b_box.get_center() + UP*3)
            ),
        )




        self.wait()
