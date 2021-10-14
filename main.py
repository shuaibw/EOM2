import numpy as np
from manim import *


class Animate(Scene):
    def construct(self):
        x_range = [-3, 10, 1]
        y_range = [-1, 7, 1]
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "tick_size": 0.04,
                "include_tip": False
            },
            x_axis_config={"numbers_to_include": np.arange(-3, 10, 1)},
            y_axis_config={"numbers_to_include": np.arange(-1, 7, 1)},
        )
        self.play(Create(axes), lag_ratio=0.5, run_time=3)

        def poly_func(x):
            return 0.07 * x ** 3 - 0.45 * x ** 2 + 0.25 * x + 2.87

        poly_graph = axes.get_graph(
            poly_func,
            color=GREEN,
            x_range=[-2, 10])
        self.play(Create(poly_graph))

        tl = ValueTracker(3)
        tr = ValueTracker(3)
        dl = Dot(point=[axes.c2p(3, poly_func(3))]).set_color(RED)
        dr = Dot(point=[axes.c2p(3, poly_func(3))]).set_color(RED)
        dl.add_updater(lambda x: x.move_to(axes.c2p(tl.get_value(), poly_func(tl.get_value()))))
        dr.add_updater(lambda x: x.move_to(axes.c2p(tr.get_value(), poly_func(tr.get_value()))))
        ll = always_redraw(lambda: axes.get_vertical_line(dl.get_bottom()))
        lr = always_redraw(lambda: axes.get_vertical_line(dr.get_bottom()))
        self.play(FadeIn(dl), FadeIn(dr))
        self.wait()
        self.play(Create(ll), Create(lr))
        self.wait()
        self.play(tl.animate.set_value(1), tr.animate.set_value(6), run_time=2)
        self.wait()

