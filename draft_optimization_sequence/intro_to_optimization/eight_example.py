from manim import *

config.background_color = "#dce2e1"
Mobject.set_default(color="#22323b")


class EightExample(Scene):
    def construct(self):
        chart = BarChart(
            values=[0, 0.19, 0.42, 0.68, 1, 1.42, 2, 3],
            bar_names=[
                # Apparently this is already being Tex'ified
                f"$x_{i}$"
                for i in range(8)
            ],
            y_range=[0, 3, 1],
            # y_length=6,
            # x_length=10,
            x_axis_config={"font_size": 36},
            bar_colors=["#b84a54"],
            bar_width=1,
        )

        axis_label = chart.get_axis_labels(
            y_label="$\Omega_{abs}(x)$",
        )[1]

        bar_labels = chart.get_bar_labels()

        self.add(chart, axis_label, bar_labels)
