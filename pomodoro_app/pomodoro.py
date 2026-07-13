"""Pomodoro Clock - a simple desktop Pomodoro timer built with Tkinter."""

import tkinter as tk
from tkinter import messagebox

WORK_MINUTES = 25
SHORT_BREAK_MINUTES = 5
LONG_BREAK_MINUTES = 15
SESSIONS_BEFORE_LONG_BREAK = 4

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
DARK_GRAY = "#2b2b2b"
FONT_NAME = "Courier"


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Clock")
        self.root.config(padx=100, pady=50, bg=YELLOW)

        self.session_count = 0
        self.timer_running = False
        self.remaining_seconds = 0
        self.after_id = None

        self.title_label = tk.Label(
            text="Timer", font=(FONT_NAME, 40, "bold"), bg=YELLOW, fg=GREEN
        )
        self.title_label.grid(row=0, column=1)

        self.canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
        self.timer_text = self.canvas.create_text(
            100, 112, text="25:00", fill="white", font=(FONT_NAME, 35, "bold")
        )
        self.canvas.grid(row=1, column=1)

        self.start_button = tk.Button(
            text="Start", highlightthickness=0, command=self.start_timer
        )
        self.start_button.grid(row=2, column=0)

        self.reset_button = tk.Button(
            text="Reset", highlightthickness=0, command=self.reset_timer
        )
        self.reset_button.grid(row=2, column=2)

        self.check_marks = tk.Label(font=(FONT_NAME, 16, "bold"), fg=GREEN, bg=YELLOW)
        self.check_marks.grid(row=3, column=1)

        self.reset_timer()

    def start_timer(self):
        if self.timer_running:
            return
        self.timer_running = True

        if self.remaining_seconds == 0:
            self.session_count += 1
            if self.session_count % (SESSIONS_BEFORE_LONG_BREAK * 2 - 1) == 0:
                self.remaining_seconds = LONG_BREAK_MINUTES * 60
                self.title_label.config(text="Long Break", fg=RED)
            elif self.session_count % 2 == 0:
                self.remaining_seconds = SHORT_BREAK_MINUTES * 60
                self.title_label.config(text="Short Break", fg=PINK)
            else:
                self.remaining_seconds = WORK_MINUTES * 60
                self.title_label.config(text="Work", fg=GREEN)

        self.count_down(self.remaining_seconds)

    def count_down(self, count):
        minutes = count // 60
        seconds = count % 60
        self.canvas.itemconfig(self.timer_text, text=f"{minutes:02d}:{seconds:02d}")

        if count > 0:
            self.remaining_seconds = count
            self.after_id = self.root.after(1000, self.count_down, count - 1)
        else:
            self.timer_running = False
            self.remaining_seconds = 0
            self.mark_completed_session()
            messagebox.showinfo("Pomodoro Clock", f"{self.title_label['text']} session finished!")
            self.start_timer()

    def mark_completed_session(self):
        if self.title_label["text"] == "Work":
            marks = "✓" * ((self.session_count + 1) // 2)
            self.check_marks.config(text=marks)

    def reset_timer(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.timer_running = False
        self.session_count = 0
        self.remaining_seconds = 0
        self.canvas.itemconfig(self.timer_text, text="25:00")
        self.title_label.config(text="Timer", fg=GREEN)
        self.check_marks.config(text="")


def main():
    root = tk.Tk()
    PomodoroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
