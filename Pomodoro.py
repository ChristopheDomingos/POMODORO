import time
import winsound
import tkinter as tk

# Constants for time intervals (in seconds)
POMODORO_DURATION = 25 * 60  # 25 minutes
SHORT_BREAK_DURATION = 5 * 60  # 5 minutes
LONG_BREAK_DURATION = 30 * 60  # 30 minutes
POMODOROS_BEFORE_LONG_BREAK = 4  # Number of Pomodoros before a long break

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.attributes('-alpha', 0.7)  # Set window transparency (0.0 to 1.0)
        self.root.attributes('-topmost', True)  # Set window to stay on top

        self.pomodoro_number = 1
        self.is_break = False
        self.running = False
        self.remaining_time = 0
        self.timer = None

        self.label = tk.Label(root, text=f"Pomodoro {self.pomodoro_number}: {self.format_time(POMODORO_DURATION)}", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.toggle_timer)
        self.start_button.pack(pady=5)

        # Create a label to display text during Pomodoro and breaks
        self.deus_label = tk.Label(root, text="DEUS", font=("Helvetica", 14))
        self.deus_label.pack(pady=5)

        # Store the time when the "Stop" button is pressed
        self.stopped_time = 0

        # Counter for completed Pomodoros
        self.completed_pomodoros = 0

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def toggle_timer(self):
        if not self.running:
            self.running = True
            self.start_button.config(text="Stop")
            if self.stopped_time > 0:
                # If stopped_time is set (after "Stop" button is pressed), resume from that point
                self.remaining_time = self.stopped_time
            elif not self.is_break:
                self.remaining_time = POMODORO_DURATION
            else:
                self.remaining_time = SHORT_BREAK_DURATION if self.pomodoro_number % (POMODOROS_BEFORE_LONG_BREAK + 1) != 0 else LONG_BREAK_DURATION
            self.update_label()
            self.run_timer()
        else:
            self.stop_pomodoro()

    def stop_pomodoro(self):
        self.running = False
        self.stopped_time = self.remaining_time  # Store the current remaining time
        self.start_button.config(text="Start")
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None

    def run_timer(self):
        if self.remaining_time > 0 and self.running:
            self.remaining_time -= 1
            self.timer = self.root.after(1000, self.run_timer)
            self.update_label()
        else:
            self.play_sound()
            if not self.is_break:
                self.pomodoro_number += 1
                self.completed_pomodoros += 1
                # Set text for Pomodoro
                self.deus_label.config(text="DEUS")
            else:
                # Set text for breaks
                if self.completed_pomodoros % POMODOROS_BEFORE_LONG_BREAK == 0:
                    self.deus_label.config(text="Não nos deixais cair em tentação\n- Assim como nós perdoamos a quem nos tem ofendido")
                else:
                    self.deus_label.config(text="Não nos deixais cair in tentação")

            self.is_break = not self.is_break

            if self.completed_pomodoros == POMODOROS_BEFORE_LONG_BREAK:
                # Long break after every 4 Pomodoros
                self.remaining_time = LONG_BREAK_DURATION
                self.completed_pomodoros = 0
                self.label.config(text=f"Take a Long Break: {self.format_time(LONG_BREAK_DURATION)}")
            else:
                # Short break or next Pomodoro
                self.remaining_time = SHORT_BREAK_DURATION if self.is_break else POMODORO_DURATION
                self.label.config(text=f"Rest: {self.format_time(SHORT_BREAK_DURATION)}" if self.is_break else f"Pomodoro {self.pomodoro_number}: {self.format_time(POMODORO_DURATION)}")
            self.run_timer()

    def update_label(self):
        self.label.config(text=f"Rest: {self.format_time(self.remaining_time)}" if self.is_break else f"Pomodoro {self.pomodoro_number}: {self.format_time(self.remaining_time)}")

    def play_sound(self):
        try:
            winsound.Beep(300, 500)  # Play a short beep sound (400 Hz) for 0.5 second
        except AttributeError:
            print("Sound notification not available on this platform.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)

    # Set minimum window size
    root.minsize(200, 100)

    root.mainloop()
