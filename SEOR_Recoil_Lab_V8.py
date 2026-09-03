from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider

Window.clearcolor = (0.025, 0.02, 0.055, 1)

PURPLE = (0.62, 0.25, 1, 1)
CYAN = (0.10, 0.75, 1, 1)
PINK = (1.0, 0.20, 0.62, 1)
GREEN = (0.20, 0.90, 0.52, 1)
WHITE = (0.95, 0.95, 1, 1)
GRAY = (0.55, 0.55, 0.65, 1)


class SEORApp(App):
    title = "SEOR Recoil Lab"

    def build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        root.add_widget(Label(
            text="SEOR",
            font_size=dp(32),
            bold=True,
            color=PURPLE,
            size_hint_y=None,
            height=dp(40)
        ))

        root.add_widget(Label(
            text="RECOIL LAB  •  V8.0",
            font_size=dp(12),
            color=GRAY,
            size_hint_y=None,
            height=dp(24)
        ))

        scroll = ScrollView(do_scroll_x=False)

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[dp(2), dp(2), dp(2), dp(20)],
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(self.heading("ОБЩИЙ КОНТРОЛЬ ОТДАЧИ"))

        content.add_widget(Label(
            text="Для всего оружия",
            color=GRAY,
            font_size=dp(13),
            size_hint_y=None,
            height=dp(25)
        ))

        self.percent = Label(
            text="0%",
            color=CYAN,
            font_size=dp(44),
            bold=True,
            size_hint_y=None,
            height=dp(65)
        )
        content.add_widget(self.percent)

        self.slider = Slider(
            min=0,
            max=100,
            value=0,
            step=1,
            size_hint_y=None,
            height=dp(50),
            cursor_size=(dp(28), dp(28))
        )
        self.slider.bind(value=self.slider_changed)
        content.add_widget(self.slider)

        marks = GridLayout(
            cols=5,
            size_hint_y=None,
            height=dp(25)
        )
        for text in ("0%", "25%", "50%", "75%", "100%"):
            marks.add_widget(Label(
                text=text,
                color=GRAY,
                font_size=dp(10)
            ))
        content.add_widget(marks)

        self.status = Label(
            text="Контроль отключён",
            color=WHITE,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(self.status)

        content.add_widget(self.heading("БЫСТРЫЕ ЗНАЧЕНИЯ"))

        quick = GridLayout(
            cols=4,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(48)
        )

        values = [
            (25, CYAN),
            (50, PURPLE),
            (75, PINK),
            (100, GREEN)
        ]

        for value, color in values:
            b = self.button(str(value) + "%", color)
            b.bind(on_release=lambda x, v=value: self.set_value(v))
            quick.add_widget(b)

        content.add_widget(quick)

        content.add_widget(self.heading("ПРОФИЛЬ"))

        self.profile = Label(
            text=self.profile_text(0),
            color=WHITE,
            font_size=dp(15),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(125)
        )
        self.profile.bind(
            size=lambda obj, value: setattr(obj, "text_size", value)
        )
        content.add_widget(self.profile)

        copy = self.button(
            "СКОПИРОВАТЬ ПРОФИЛЬ",
            CYAN,
            52
        )
        copy.bind(on_release=self.copy_profile)
        content.add_widget(copy)

        reset = self.button(
            "СБРОСИТЬ",
            PINK,
            48
        )
        reset.bind(on_release=lambda x: self.set_value(0))
        content.add_widget(reset)

        content.add_widget(Label(
            text=(
                "SEOR V8.0\n"
                "Общий визуальный профиль для всего оружия.\n"
                "Не изменяет память, файлы или процесс игры.\n"
                "Root не требуется."
            ),
            color=GRAY,
            font_size=dp(10),
            halign="center",
            size_hint_y=None,
            height=dp(70)
        ))

        scroll.add_widget(content)
        root.add_widget(scroll)

        return root

    def heading(self, text):
        return Label(
            text=text,
            color=PURPLE,
            bold=True,
            font_size=dp(14),
            halign="left",
            size_hint_y=None,
            height=dp(30)
        )

    def button(self, text, color, height=48):
        return Button(
            text=text,
            font_size=dp(13),
            bold=True,
            color=WHITE,
            background_normal="",
            background_color=(
                color[0] * 0.5,
                color[1] * 0.5,
                color[2] * 0.5,
                1
            ),
            size_hint_y=None,
            height=dp(height)
        )

    def slider_changed(self, instance, value):
        self.update_value(int(value))

    def set_value(self, value):
        self.slider.value = value
        self.update_value(value)

    def update_value(self, value):
        value = int(value)

        self.percent.text = str(value) + "%"
        self.profile.text = self.profile_text(value)

        if value == 0:
            self.percent.color = CYAN
            self.status.text = "Контроль отключён"
        elif value < 50:
            self.percent.color = CYAN
            self.status.text = "Низкий уровень контроля"
        elif value < 80:
            self.percent.color = PURPLE
            self.status.text = "Средний уровень контроля"
        elif value < 100:
            self.percent.color = PINK
            self.status.text = "Высокий уровень контроля"
        else:
            self.percent.color = GREEN
            self.status.text = "Максимальный уровень"

    def profile_text(self, value):
        return (
            "Режим: ВСЁ ОРУЖИЕ\n"
            "Контроль: " + str(value) + "%\n"
            "Профиль: SEOR Universal\n\n"
            "Значение является визуальным профилем\n"
            "и не меняет отдачу внутри игры."
        )

    def copy_profile(self, button):
        value = int(self.slider.value)

        text = (
            "SEOR RECOIL LAB V8.0\n"
            "Mode: Universal\n"
            "All weapons: " + str(value) + "%\n"
            "Type: Visual profile"
        )

        try:
            Clipboard.copy(text)
            self.status.text = "Профиль скопирован"
        except Exception:
            self.status.text = "Не удалось скопировать"

if __name__ == "__main__":
    SEORApp().run()
