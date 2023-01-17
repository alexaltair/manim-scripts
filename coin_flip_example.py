from os import linesep

from manim import *

# config.pixel_height = 580
config.background_color = '#dce2e1'
Mobject.set_default(color='#22323b')

class CoinFlipExample(Scene):
    def construct(self):
        x_axis_font_size = 26

        chart = BarChart(
            values=[1/8, 3/8, 3/8, 1/8],
            bar_names=[
                # Apparently this is already being Tex'ified
                "TTT",
                "TTH,",
                "HHT,",
                "HHH",
            ],
            y_range=[0, 1, 1/8],
            # y_length=6,
            x_length=4.8,
            x_axis_config={"font_size": x_axis_font_size},
            bar_colors=['#4b7d92'],
            bar_width=1,
        ).shift(3*LEFT)


        # c_bar_lbls = chart.get_bar_labels()
        drop_labels1 = [
            Tex("THT,", font_size=x_axis_font_size).shift(2.8*DOWN + 3.6*LEFT),
            Tex("and HTT", font_size=x_axis_font_size).shift(3.2*DOWN + 3.6*LEFT),
            Tex("HTH,", font_size=x_axis_font_size).shift(2.8*DOWN + 2.4*LEFT),
            Tex("and THH", font_size=x_axis_font_size).shift(3.2*DOWN + 2.3*LEFT),
        ]

        ylabel = chart.get_axis_labels(
            y_label='$p(x)$',
        )[1]


        self.add(
            chart,
            ylabel,
            *drop_labels1,
        )




        chart2 = BarChart(
            values=[1, 7/8, 4/8, 1/8],
            bar_names=[
                # Apparently this is already being Tex'ified
                "TTT",
                "TTH,",
                "HHT,",
                "HHH",
            ],
            y_range=[0, 1, 1/8],
            # y_length=6,
            x_length=4.8,
            x_axis_config={"font_size": x_axis_font_size},
            bar_colors=['#395385'],
            bar_width=1,
        ).shift(3.8*RIGHT)


        # c_bar_lbls = chart2.get_bar_labels()
        drop_labels2 = [
            Tex("THT,", font_size=x_axis_font_size).shift(2.8*DOWN + 3.2*RIGHT),
            Tex("and HTT", font_size=x_axis_font_size).shift(3.2*DOWN + 3.2*RIGHT),
            Tex("HTH,", font_size=x_axis_font_size).shift(2.8*DOWN + 4.4*RIGHT),
            Tex("and THH", font_size=x_axis_font_size).shift(3.2*DOWN + 4.5*RIGHT),
        ]

        ylabel2 = chart2.get_axis_labels(
            y_label='$p_x$',
        )[1]


        self.add(
            chart2,
            ylabel2,
            *drop_labels2,
        )
