"""Pomodoro Clock - Kivy app for Android with the timer docked top-right."""

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

DEFAULT_MINUTES = 25
MIN_MINUTES = 1
MAX_MINUTES = 90


class PomodoroWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=6, padding=10, **kwargs)
        self.size_hint = (None, None)
        self.size = (240, 190)

        self.total_minutes = DEFAULT_MINUTES
        self.remaining_seconds = self.total_minutes * 60
        self.timer_event = None
        self.is_running = False

        self.time_label = Label(text=self._format_time(), font_size=34, bold=True)
        self.add_widget(self.time_label)

        minute_row = BoxLayout(size_hint_y=None, height=40, spacing=4)
        minute_row.add_widget(Button(text="-", on_press=self.decrease_minutes))
        self.minutes_label = Label(text=f"{self.total_minutes} min")
        minute_row.add_widget(self.minutes_label)
        minute_row.add_widget(Button(text="+", on_press=self.increase_minutes))
        self.add_widget(minute_row)

        control_row = BoxLayout(size_hint_y=None, height=40, spacing=4)
        control_row.add_widget(Button(text="Start", on_press=self.start_timer))
        control_row.add_widget(Button(text="Pause", on_press=self.pause_timer))
        control_row.add_widget(Button(text="Stop", on_press=self.stop_timer))
        self.add_widget(control_row)

    def _format_time(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def _reset_display(self):
        self.remaining_seconds = self.total_minutes * 60
        self.minutes_label.text = f"{self.total_minutes} min"
        self.time_label.text = self._format_time()

    def increase_minutes(self, instance):
        if self.is_running:
            return
        if self.total_minutes < MAX_MINUTES:
            self.total_minutes += 1
            self._reset_display()

    def decrease_minutes(self, instance):
        if self.is_running:
            return
        if self.total_minutes > MIN_MINUTES:
            self.total_minutes -= 1
            self._reset_display()

    def start_timer(self, instance):
        if self.is_running:
            return
        if self.remaining_seconds == 0:
            self.remaining_seconds = self.total_minutes * 60
        self.is_running = True
        self.timer_event = Clock.schedule_interval(self._tick, 1)

    def pause_timer(self, instance):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        self.is_running = False

    def stop_timer(self, instance):
        self.pause_timer(instance)
        self._reset_display()

    def _tick(self, dt):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.time_label.text = self._format_time()
        else:
            self.pause_timer(None)
            self.time_label.text = "Done!"


class PomodoroApp(App):
    def build(self):
        root = FloatLayout()
        timer_widget = PomodoroWidget(pos_hint={"right": 0.98, "top": 0.98})
        root.add_widget(timer_widget)
        return root


if __name__ == "__main__":
    PomodoroApp().run()
