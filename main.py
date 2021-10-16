import numpy as np
from manim import *


class Animate(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 10, 1],
            y_range=[-1, 7, 1],
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "tick_size": 0.04,
                "include_tip": False
            },
            x_axis_config={"numbers_to_include": np.arange(-3, 10, 1)},
            y_axis_config={"numbers_to_include": np.arange(-1, 7, 1)},
        )
        axes_no_num = Axes(
            x_range=[-3, 10, 1],
            y_range=[-1, 7, 1],
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "tick_size": 0.04,
                "include_tip": False
            },
        )
        self.play(Create(axes), lag_ratio=0.5, run_time=3)

        def poly_func(x):
            return 0.07 * x ** 3 - 0.45 * x ** 2 + 0.25 * x + 2.87

        poly_graph = axes.get_graph(
            poly_func,
            color=GREEN,
            x_range=[-2, 10])
        self.play(Create(poly_graph))

        # Limit mover
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

        # Area generator
        area = axes.get_area(poly_graph, x_range=(1, 6), color=[ORANGE, PURPLE], opacity=0.5)
        self.play(FadeIn(area))
        itexsp = Tex(r'$\displaystyle \int_1^6 f(x)\,dx$')
        itexsp.shift(3 * UP)
        self.play(TransformFromCopy(area, itexsp))
        self.play(ReplacementTransform(axes, axes_no_num), run_time=2)
        liml = Text('a', font_size=25).set_color(BLUE).next_to(axes.c2p(1, 0), DOWN)
        limr = Text('b', font_size=25).set_color(GREEN).next_to(axes.c2p(6, 0), DOWN)
        self.play(Write(liml), Write(limr), run_time=2)
        # itexgen = Tex(r'$\displaystyle \int', r'_a', r'^b', r'f(x)\,dx$')
        itexgen = Tex(r'$\displaystyle \int_a^b f(x)\,dx$').move_to(itexsp)
        self.play(ReplacementTransform(itexsp, itexgen))
        self.play(ShowCreationThenFadeOut(SurroundingRectangle(itexgen).set_stroke(BLUE, 2.5)), run_time=2)
        self.play(*[FadeOut(x) for x in [liml, limr, area, dl, dr, ll, lr, itexgen]])

        # Zero area??
        an = Axes(
            x_range=[-1, 7, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "tick_size": 0.04,
                "include_tip": False
            },
            # x_axis_config={"numbers_to_include": np.arange(-3, 10, 1)},
            # y_axis_config={"numbers_to_include": np.arange(-3, 5, 1)},
        )
        an.to_edge(LEFT, buff=1)
        sin_graph = an.get_graph(lambda x: np.sin(x), x_range=[0, TAU], color=BLUE)
        self.play(ReplacementTransform(axes_no_num, an), ReplacementTransform(poly_graph, sin_graph), run_time=2)
        area_start = Tex('$0$', font_size=25).next_to(an.c2p(-0.2, 0), DOWN)
        area_end = Tex('$2\pi$', font_size=25).next_to(an.c2p(TAU, 0), DOWN)
        # area_start = an.get_graph_label(sin_graph, "x=0", x_val=0, direction=UL, color=WHITE)
        # area_end = an.get_graph_label(sin_graph, "x=2\pi", x_val=TAU, direction=UR, color=WHITE)
        self.play(*[FadeIn(x) for x in [area_start, area_end]])
        pos_dx_list = [0.4, 0.25, 0.1, 0.05, 0.005]
        neg_dx_list = [0.4, 0.25, 0.1, 0.05, 0.005]
        stroke_list = [0.4, 0.2, 0.1, 0.05, 0.0]
        pos_area_list = VGroup(
            *[
                an.get_riemann_rectangles(
                    sin_graph,
                    x_range=[0, PI],
                    dx=pos_dx_list[i],
                    stroke_width=stroke_list[i],
                    stroke_color=BLACK,
                    fill_opacity=0.7,
                    color=[BLUE, GREEN]
                )
                for i in range(0, len(pos_dx_list))
            ]
        )
        neg_area_list = VGroup(
            *[
                an.get_riemann_rectangles(
                    sin_graph,
                    x_range=[PI, 2 * PI],
                    dx=pos_dx_list[i],
                    stroke_width=stroke_list[i],
                    stroke_color=BLACK,
                    fill_opacity=0.7,
                    color=[ORANGE, PURPLE]
                )
                for i in range(0, len(neg_dx_list))
            ]
        )
        pa = pos_area_list[-1]
        na = neg_area_list[-1]
        self.play(Create(pa), run_time=1.5)
        self.play(Create(na), run_time=1.5)
        integral_area = MathTex(r'\text{Area} &= \int_0^{2\pi}\sin{x}\,dx\\',
                                r' &= \left[-\cos{x}\right]_0^{2\pi} \\',
                                r' &= 0', font_size=35).to_corner(UR, buff=0.6)
        for txt in integral_area:
            self.play(Write(txt))
            self.wait()
        for i in range(len(pos_dx_list) - 2, -1, -1):
            new_pa = pos_area_list[i]
            new_na = neg_area_list[i]
            self.play(Transform(pa, new_pa), Transform(na, new_na))
            self.wait()

        self.play(FadeOut(integral_area), run_time=2)

        # pos neg area
        