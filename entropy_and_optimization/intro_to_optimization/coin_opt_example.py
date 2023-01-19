from manim import *

config.background_color = '#dce2e1'
Mobject.set_default(color='#22323b')

class CoinOptExample(Scene):
    def construct(self):
        x_axis_font_size = 26

        chart = BarChart(
            values=[0, 0.19, 1, 3],
            bar_names=[
                "TTT",
                "TTH,",
                "HHT,",
                "HHH",
            ],
            y_range=[0, 3, 1],
            # y_length=6,
            # x_length=10,
            x_axis_config={"font_size": x_axis_font_size},
            bar_colors=['#b84a54'],
            bar_width=1,
        )

        axis_label = chart.get_axis_labels(
            y_label='$\Omega_{abs}(x)$',
        )[1]

        bar_labels = chart.get_bar_labels()

        drop_labels1 = [
            Tex("THT,", font_size=x_axis_font_size).shift(2.8*DOWN + 0.5*LEFT),
            Tex("and HTT", font_size=x_axis_font_size).shift(3.2*DOWN + 0.6*LEFT),
            Tex("HTH,", font_size=x_axis_font_size).shift(2.8*DOWN + 0.5*RIGHT),
            Tex("and THH", font_size=x_axis_font_size).shift(3.2*DOWN + 0.7*RIGHT),
        ]

        self.add(
            chart,
            axis_label,
            bar_labels,
            *drop_labels1,
        )
