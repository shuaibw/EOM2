import numpy as np
from manim import *


class Animate(Scene):
    def construct(self):
        # intro

        # main
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
        self.play(Create(axes), run_time=2)

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
        dx_list = [0.4, 0.25, 0.1, 0.05, 0.005]
        stroke_list = [0.4, 0.2, 0.1, 0.05, 0.0]
        pos_area_list = VGroup(
            *[
                an.get_riemann_rectangles(
                    sin_graph,
                    x_range=[0, PI],
                    dx=dx_list[i],
                    stroke_width=stroke_list[i],
                    stroke_color=BLACK,
                    fill_opacity=0.7,
                    color=[ORANGE, PURPLE]
                )
                for i in range(0, len(dx_list))
            ]
        )
        neg_area_list = VGroup(
            *[
                an.get_riemann_rectangles(
                    sin_graph,
                    x_range=[PI, 2 * PI],
                    dx=dx_list[i],
                    stroke_width=stroke_list[i],
                    stroke_color=BLACK,
                    fill_opacity=0.7
                )
                for i in range(0, len(dx_list))
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
        for i in range(len(dx_list) - 2, -1, -1):
            new_pa = pos_area_list[i]
            new_na = neg_area_list[i]
            self.play(Transform(pa, new_pa), Transform(na, new_na))
            self.wait()

        self.play(FadeOut(integral_area), run_time=2)

        # pos area expl
        area_pos = pos_area_list[0]
        rect = area_pos[3].copy()
        rect.shift(2 * (2 * RIGHT + UP))
        self.play(TransformFromCopy(area_pos[3], rect))
        dx_brace = Brace(rect, DOWN).set_stroke(width=0.2)
        f_brace = Brace(rect, LEFT).set_stroke(width=0.2)
        dx_brace_text = dx_brace.get_text(
            r"$dx$"
        ).scale(0.8)
        f_brace_text = f_brace.get_text(
            r"$f(x)$", buff=0.1
        ).scale(0.8)
        self.play(FadeIn(dx_brace), FadeIn(f_brace))
        self.play(Write(dx_brace_text), Write(f_brace_text))
        f_pos_tex = Tex(
            r"$f(x)>0$"
        ).scale(0.8).move_to(f_brace_text).shift(LEFT / 4)
        dx_pos_tex = Tex(
            r"$dx>0$"
        ).scale(0.8).move_to(dx_brace_text)
        dptc = dx_pos_tex.copy()
        self.play(
            ReplacementTransform(f_brace_text, f_pos_tex),
            ReplacementTransform(dx_brace_text, dx_pos_tex)
        )
        why_pos = MathTex(r'dx = \frac{2\pi-0}{n}').scale(0.8).next_to(dx_brace, DOWN, buff=0.1)
        dgtr = SurroundingRectangle(dx_pos_tex, color=GREEN)
        self.play(Create(dgtr))
        self.wait()
        self.play(Uncreate(dgtr))
        self.play(Transform(dx_pos_tex, why_pos))
        num_of_rect = MathTex(r'n=\text{No. of rectangles}').scale(0.65).next_to(why_pos, RIGHT)
        self.play(Write(num_of_rect))
        self.play(FadeOut(num_of_rect))
        self.wait()
        self.play(Transform(dx_pos_tex, dptc))
        small_area = Tex(
            r"$dA = f(x)dx > 0$"
        ).scale(0.8).next_to(rect, RIGHT)
        self.play(ShowCreationThenFadeOut(SurroundingRectangle(rect, color=BLUE, buff=0)))
        self.play(Write(small_area))
        to_remove = [f_brace, dx_brace, f_pos_tex, dx_pos_tex, small_area, rect]
        self.play(*[FadeOut(x) for x in to_remove])

        # neg area expl
        area_neg = neg_area_list[0]
        rect = area_neg[3].copy()
        rect.shift(2.5 * UP)
        self.play(TransformFromCopy(area_neg[3], rect))
        dx_brace = Brace(rect, DOWN).set_stroke(width=0.2)
        f_brace = Brace(rect, LEFT).set_stroke(width=0.2)
        dx_brace_text = dx_brace.get_text(
            r"$dx$"
        ).scale(0.8)
        f_brace_text = f_brace.get_text(
            r"$f(x)$", buff=0.1
        ).scale(0.8)
        self.play(FadeIn(dx_brace), FadeIn(f_brace))
        self.play(Write(dx_brace_text), Write(f_brace_text))
        f_pos_tex = Tex(
            r"$f(x)<0$"
        ).scale(0.8).move_to(f_brace_text).shift(LEFT / 4)
        dx_pos_tex = Tex(
            r"$dx>0$"
        ).scale(0.8).move_to(dx_brace_text)
        self.play(
            ReplacementTransform(f_brace_text, f_pos_tex),
            ReplacementTransform(dx_brace_text, dx_pos_tex)
        )
        small_area = Tex(
            r"$dA = f(x)dx < 0$"
        ).scale(0.8).next_to(rect, RIGHT)
        self.play(ShowCreationThenFadeOut(SurroundingRectangle(rect, color=BLUE, buff=0)))
        self.play(Write(small_area))
        to_remove = [f_brace, dx_brace, f_pos_tex, dx_pos_tex, small_area, rect]
        self.play(*[FadeOut(x) for x in to_remove])

        # show cancelling
        area_pos_shift = area_pos.copy()
        area_neg_shift = area_neg.copy()
        area_pos_shift.shift(5 * RIGHT + 2.5 * UP)
        area_neg_shift.next_to(area_pos_shift, DOWN, buff=0)
        self.play(TransformFromCopy(area_pos, area_pos_shift))
        self.play(TransformFromCopy(area_neg, area_neg_shift))
        for i in range(len(area_pos_shift)):
            if i % 2 == 0:
                a = area_pos_shift[i]
                b = area_neg_shift[i]
            else:
                a = area_neg_shift[i]
                b = area_pos_shift[i]
            self.play(a.animate.move_to(b), run_time=0.5)
            self.play(FadeOut(a), FadeOut(b), run_time=0.5)
        zero_area_tex = MathTex(r'\int_0^{2\pi}\sin{x}\,dx=0').to_corner(UR, buff=0.5)
        riemann_grp = VGroup(pos_area_list, neg_area_list)
        self.play(ReplacementTransform(riemann_grp, zero_area_tex))
        self.play(ShowCreationThenFadeOut(SurroundingRectangle(zero_area_tex, color=BLUE)))
        self.play(*[Unwrite(x) for x in [area_start, area_end, zero_area_tex]])
        self.remove(pos_area_list, neg_area_list)

        # Non zero error area
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 5, 1],
            x_length=8,
            y_length=7,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "tick_size": 0.04,
                "include_tip": False
            },
            # x_axis_config={"numbers_to_include": np.arange(-3, 10, 1)},
            # y_axis_config={"numbers_to_include": np.arange(-3, 5, 1)},
        )
        axes.to_edge(LEFT, buff=0.3)
        poly_graph2 = axes.get_graph(
            lambda x: 2 / 5 * (x ** 2 - 4), [-4, 4], color=GREEN_C
        )
        pg2_label = axes.get_graph_label(poly_graph2, r"f(x) = \frac{2}{5}(x^2-2)", x_val=-4, direction=UP,
                                         color=BLUE).scale(0.7)
        self.play(ReplacementTransform(an, axes), ReplacementTransform(sin_graph, poly_graph2), Write(pg2_label),
                  run_time=2)
        area_start = MathTex('0', font_size=25).next_to(axes.c2p(-0.2, 0), DOWN)
        area_end = MathTex('4', font_size=25).next_to(axes.c2p(4, 0), DOWN)
        self.play(*[FadeIn(x) for x in [area_start, area_end]])
        dx_list = [0.4, 0.25, 0.1, 0.05, 0.005]
        stroke_list = [0.4, 0.2, 0.1, 0.05, 0.0]
        pos_area_list = VGroup(
            *[
                axes.get_riemann_rectangles(
                    poly_graph2,
                    x_range=[2, 4],
                    dx=dx_list[i],
                    stroke_width=stroke_list[i],
                    stroke_color=BLACK,
                    fill_opacity=0.7,
                    color=[GREEN, BLUE]
                )
                for i in range(0, len(dx_list))
            ]
        )
        neg_area_list = VGroup(
            *[
                axes.get_riemann_rectangles(
                    poly_graph2,
                    x_range=[0, 2],
                    dx=dx_list[i],
                    stroke_width=stroke_list[i],
                    stroke_color=BLACK,
                    fill_opacity=0.7
                )
                for i in range(0, len(dx_list))
            ]
        )
        pa = pos_area_list[-1]
        na = neg_area_list[-1]
        self.play(Create(na), run_time=1.5)
        self.play(Create(pa), run_time=1.5)
        integral_area = MathTex(r'\text{Area} &= \int_0^{4}\frac{2}{5}(x^2-4)\,dx\\',
                                r' &= \frac{2}{5}\left[\frac{x^3}{3}-4x\right]_0^{4} \\',
                                r' &= ', r'\frac{32}{15}', font_size=35).to_corner(UR, buff=0.6)
        for txt in integral_area:
            self.play(Write(txt))
            self.wait()
        self.play(ShowCreationThenFadeOut(SurroundingRectangle(integral_area[3], color=GREEN)))
        for i in range(len(dx_list) - 2, -1, -1):
            new_pa = pos_area_list[i]
            new_na = neg_area_list[i]
            self.play(Transform(pa, new_pa), Transform(na, new_na))
            self.wait()

        self.play(FadeOut(integral_area[1:]))
        pa_shift = pa.copy()
        na_shift = na.copy()
        pa_shift.shift(5 * RIGHT)
        na_shift.next_to(pa_shift, DOWN, buff=0)
        self.play(TransformFromCopy(pa, pa_shift))
        self.play(TransformFromCopy(na, na_shift))
        self.play(*[na_shift[i].animate.align_to(pa_shift[i], DOWN) for i in range(len(pa_shift))])
        self.play(*[FadeOut(x) for x in na_shift], pa_shift.animate.stretch(0.5, 1).shift(DOWN))
        area_surround = SurroundingRectangle(pa_shift, color=BLUE)
        aro = Arrow(start=area_surround.get_corner(UR), end=integral_area[0].get_bottom(), color=YELLOW,
                    tip_shape=ArrowCircleFilledTip, stroke_width=1.3, tip_length=0.2)
        self.play(Create(area_surround))
        self.play(ShowCreationThenFadeOut(aro))
        new_tex = MathTex(r'\text{Area} = \frac{32}{15}}', font_size=35).move_to(integral_area[0])
        self.play(ReplacementTransform(integral_area[0], new_tex), Uncreate(area_surround))
        self.play(*[FadeOut(i) for i in [pa_shift, new_tex]])
        _a = axes.get_area(poly_graph2, x_range=(0, 2), color=[ORANGE, PURPLE], opacity=0.7)
        _b = axes.get_area(poly_graph2, x_range=(2, 4), color=[GREEN, BLUE], opacity=0.7)
        self.play(ReplacementTransform(na, _a),
                  ReplacementTransform(pa, _b),
                  run_time=2)

        # Now explain what to do
        find_intersect_tex = MathTex(r"\frac{2}{5}(x^2-4) &= 0\\",
                                     r"x&=", r"+2", r",-2",
                                     font_size=35).to_corner(UR, buff=0.6)
        self.play(ReplacementTransform(pg2_label, find_intersect_tex[0]))
        for x in find_intersect_tex[1:]:
            self.play(Write(x))
        intersect_rect = SurroundingRectangle(find_intersect_tex[2], color=BLUE)
        self.play(Create(intersect_rect))
        x_intersect_dot = Dot(point=axes.c2p(2, 0), color=RED)
        self.play(ReplacementTransform(intersect_rect, x_intersect_dot), FadeOut(find_intersect_tex))
        pg2_na_brace = Brace(na, direction=UP, color=PURPLE)
        self.play(FadeIn(pg2_na_brace))
        big_minus = MathTex("-", color=BLUE, stroke_width=5).move_to(axes.c2p(0.8, -0.8))
        big_plus = MathTex("+", color=ORANGE, stroke_width=5).move_to(axes.c2p(3.5, 1.6))
        pg2_area_tex = MathTex(r"A_1 &= \int_0^2 f(x)\,dx",
                               r"= -\frac{32}{15}\\",
                               r"A_2 &= \int_2^4 f(x)\,dx",
                               r"=\frac{64}{15}\\",
                               r"\text{Area} &= |A_1| + |A_2|\\",
                               r"&=\frac{32}{15} + \frac{64}{15}\\",
                               r"&=\frac{32}{5}",
                               font_size=35).to_corner(UR, buff=0.6)
        self.play(ReplacementTransform(pg2_na_brace, pg2_area_tex[0]), FadeIn(big_minus))
        self.wait()
        self.play(Write(pg2_area_tex[1]))
        pg2_pa_brace = Brace(pa, direction=DOWN, color=GREEN)
        self.play(FadeIn(pg2_pa_brace))
        self.play(ReplacementTransform(pg2_pa_brace, pg2_area_tex[2]), FadeIn(big_plus))
        self.wait()
        for x in pg2_area_tex[3:]:
            self.play(Write(x))
            self.wait()
        poly_group = [_a, _b, x_intersect_dot, big_plus, big_minus, area_start, area_end, pg2_area_tex]
        self.play(*[FadeOut(x) for x in poly_group])

        # Now sin area
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
        an.to_edge(LEFT, buff=0.6)
        area_start = Tex('$0$', font_size=25).next_to(an.c2p(-0.2, 0), DOWN)
        area_mid = Tex('$\pi$', font_size=25).next_to(an.c2p(PI, 0), DOWN)
        area_end = Tex('$2\pi$', font_size=25).next_to(an.c2p(TAU, 0), DOWN)
        sin_graph = an.get_graph(lambda x: np.sin(x), x_range=[0, TAU], color=BLUE)
        sg_label = an.get_graph_label(sin_graph, label=r'f(x)=\sin(x)', color=GREEN, x_val=1).scale(0.7).shift(UP)
        self.play(ReplacementTransform(axes, an), ReplacementTransform(poly_graph2, sin_graph))
        self.play(Write(sg_label))
        self.play(*[FadeIn(x) for x in [area_start, area_mid, area_end]])
        sg_pa = an.get_area(sin_graph, (0, PI), color=[GREEN, BLUE], opacity=0.7)
        sg_na = an.get_area(sin_graph, (PI, 2 * PI), color=[ORANGE, PURPLE], opacity=0.7)
        sg_pa_br = Brace(sg_pa, DOWN, color=BLUE)
        sg_na_br = Brace(sg_na, UP, color=ORANGE)
        self.play(FadeIn(sg_pa), FadeIn(sg_na))
        sg_area_tex = MathTex(r"A_1 &= \int_0^{\pi} f(x)\,dx",
                              r"= 2\\",
                              r"A_2 &= \int_{\pi}^{2\pi} f(x)\,dx",
                              r"=-2\\",
                              r"\text{Area} &= |A_1| + |A_2|\\",
                              r"&=2 + 2\\",
                              r"&=4",
                              font_size=35).to_corner(UR, buff=0.6)
        self.play(FadeIn(sg_pa_br))
        self.wait()
        self.play(ReplacementTransform(sg_pa_br, sg_area_tex[0]))
        self.play(Write(sg_area_tex[1]), FadeIn(big_plus.move_to(an.c2p(PI / 2, 0.3))))
        self.play(FadeIn(sg_na_br))
        self.wait()
        self.play(ReplacementTransform(sg_na_br, sg_area_tex[2]), FadeIn(big_minus.move_to(an.c2p(3 * PI / 2, -0.3))))
        self.play(Write(sg_area_tex[3]))
        for x in sg_area_tex[3:]:
            self.play(Write(x))
            self.wait()
        self.wait()
        to_remove = [area_start, area_end, area_mid, sg_area_tex]
        self.play(*[FadeOut(x) for x in to_remove])

        # evil rotation hack
        rot_grp = VGroup(sin_graph, an, sg_pa, sg_na, big_minus, big_plus)
        self.play(Rotate(rot_grp, PI / 2), FadeOut(sg_label))
        bm_op = big_minus.get_center()
        self.play(Rotate(big_minus, PI / 2))
        self.play(big_minus.animate.move_to(big_plus), big_plus.animate.move_to(bm_op))
        self.wait()
        x_fn_tex = MathTex(r'y=f(x)').scale(0.8).to_corner(UR, buff=0.7).shift(LEFT)
        x_int_tex = MathTex(r'\text{Area} = ', r'\int_a^b f(x)\,dx').scale(0.8).next_to(x_fn_tex, DOWN)
        y_fn_tex = MathTex(r'x=f(y)').scale(0.8).move_to(x_fn_tex)
        y_int_tex = MathTex(r'\text{Area} = ', r'\int_a^b f(y)\,dy').scale(0.8).move_to(x_int_tex)
        self.play(Write(x_fn_tex))
        self.wait()
        self.play(Write(x_int_tex))
        self.play(ReplacementTransform(x_fn_tex, y_fn_tex))
        self.wait()
        self.play(ReplacementTransform(x_int_tex, y_int_tex))
        x_neg = MathTex(r'x<0\\', r'\Rightarrow f(y)<0\\', r'\Rightarrow dA<0').move_to(an.c2p(2, 3)).scale(0.8)
        x_pos = MathTex(r'x>0\\', r'\Rightarrow f(y)>0\\', r'\Rightarrow dA>0').move_to(an.c2p(5, -3)).scale(0.8)
        for x in x_pos:
            self.play(Write(x))
            self.wait()
        self.play(ShowCreationThenFadeOut(SurroundingRectangle(big_plus, color=BLUE)))
        for x in x_neg:
            self.play(Write(x))
            self.wait()
        self.play(ShowCreationThenFadeOut(SurroundingRectangle(big_minus, color=ORANGE)))
        self.play(y_int_tex.animate.move_to(ORIGIN))
        self.play(ShowCreationThenFadeOut(SurroundingRectangle(y_int_tex, color=BLUE)))
        self.play(*[FadeOut(x) for x in self.mobjects])
        cya = Text("Thank you for watching!", font_size=35).set_color_by_gradient(BLUE, GREEN, GOLD)
        cya1 = Text("Instructor: Kazi Rakibul Hasan", font_size=35).set_color_by_gradient(GOLD, ORANGE).next_to(cya,
                                                                                                               DOWN)
        cya2 = Text("Animation: Anwarul Bashir Shuaib", font_size=35).set_color_by_gradient(ORANGE, PURPLE).next_to(
            cya1, DOWN)
        self.play(Write(VGroup(cya, cya1, cya2).move_to(ORIGIN)))
