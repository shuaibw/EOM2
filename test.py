from manim import *


class SquareToCircle(Scene):
    def construct(self):
        text = Text(r'Area by Integration', font='Impact').set_color_by_gradient(ORANGE, PURPLE, GREEN).shift(UP)
        text2 = Text(r'যোগজীকরণের মাধ্যমে ক্ষেত্রফল নির্ণয়', font="Li Shamim Cholontika Unicode").set_color_by_gradient(
            ORANGE, PURPLE,
            GREEN)
        text2.next_to(text, DOWN, buff=0.6)
        grp = VGroup(text, text2)
        self.play(Write(grp))
        self.wait(1.5)
        self.play(FadeOut(grp))
