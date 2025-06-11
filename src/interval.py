import json
from tkinter import messagebox as mbx
import customtkinter as ctk
import data_manager
from datetime import date, timedelta

# A simple tooltip class to show info on hover
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True) # Remove window decorations
        self.tooltip_window.geometry(f"+{x}+{y}")
        label = ctk.CTkLabel(self.tooltip_window, text=self.text, corner_radius=5, fg_color="#2B2B2B")
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.session_cycles = 0
        self.session_work_seconds = 0
        self.session_break_seconds = 0
        self.work_label = None
        self.break_label = None
        self.timer_label = None
        self.timer_after_id = None
        self.remaining_time = None
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("work-interval-app")
        self.geometry('550x450')

        self.work_time_var = ctk.DoubleVar(value=1800)
        self.break_time_var = ctk.DoubleVar(value=300)
        self.create_home_window()
        self.mainloop()

    def create_stats_window(self):
        self.clear_window()
        self.geometry('550x450')

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(main_frame, text="Work Cycles History", font=("Liberation Mono", 18, "bold")).pack(pady=(0, 10))

        heatmap_frame = ctk.CTkFrame(main_frame)
        heatmap_frame.pack(pady=5)
        self._create_heatmap(heatmap_frame)

        stats_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        stats_frame.pack(pady=20)
        ctk.CTkLabel(stats_frame, text="Current Session Stats", font=("Liberation Mono", 16, "bold")).pack()
        ctk.CTkLabel(stats_frame, text=f"Completed Cycles: {self.session_cycles}").pack()
        ctk.CTkLabel(stats_frame, text=f"Total Work Time: {self.convert_hours_mins_secs(self.session_work_seconds)}").pack()
        ctk.CTkLabel(stats_frame, text=f"Total Break Time: {self.convert_hours_mins_secs(self.session_break_seconds)}").pack()

        ctk.CTkButton(self, text="Back to Home", command=self.create_home_window).pack(pady=(0, 20))

    def _create_heatmap(self, parent_frame):
        data = data_manager.load_data()
        today = date.today()
        start_date = today - timedelta(days=120)
        start_date -= timedelta(days=(start_date.weekday() + 1) % 7)

        days_of_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, day in enumerate(["Mon", "Wed", "Fri"]):
            label = ctk.CTkLabel(parent_frame, text=day, font=("Liberation Mono", 10))
            label.grid(row=(i * 2) + 1, column=0, padx=(0,5))

        for week in range(18):
            for day in range(7):
                current_date = start_date + timedelta(days=(week * 7) + day)
                if current_date > today:
                    color = "transparent"
                    tooltip_text = f"{current_date.isoformat()}: No data"
                else:
                    date_str = current_date.isoformat()
                    count = data.get(date_str, 0)
                    color = self._get_color_for_count(count)
                    tooltip_text = f"{date_str}: {count} cycle(s)"

                day_frame = ctk.CTkFrame(parent_frame, width=15, height=15, fg_color=color, corner_radius=3)
                day_frame.grid(row=day, column=week + 1, padx=2, pady=2)
                Tooltip(day_frame, tooltip_text)

    def _get_color_for_count(self, count):
        if count == 0: return "#424242"
        elif 1 <= count <= 2: return "#39d353"
        elif 3 <= count <= 5: return "#26a641"
        elif 6 <= count <= 8: return "#006d32"
        else: return "#0e4429"

    def create_home_window(self):
        self.clear_window()
        self.geometry('400x400')
        ctk.CTkLabel(self, text="Work Interval Timer", font=("Liberation Mono", 28, "bold")).pack(pady=(50, 20))
        ctk.CTkLabel(self, text="Focus. Break. Repeat.", font=("Liberation Mono", 16)).pack(pady=(0, 50))
        ctk.CTkButton(self, text="Start New Session", command=self.configuration_window, width=200, height=40).pack(pady=10)
        ctk.CTkButton(self, text="View History", command=self.create_stats_window, width=200, height=40).pack(pady=10)

    def configuration_window(self):
        self.clear_window()
        self.geometry('400x400')
        self.session_cycles = 0
        self.session_work_seconds = 0
        self.session_break_seconds = 0
        ctk.CTkLabel(self, text="How Long Will You Work For ?", text_color="white", font=("Liberation Mono", 15)).pack(pady=(20, 0))
        ctk.CTkSlider(self, from_=5, to=7200, variable=self.work_time_var, width=200, command=lambda v: self.update_label(self.work_label, v)).pack(padx=100, pady=5, expand=True)
        self.work_label = ctk.CTkLabel(self, text=self.convert_hours_mins_secs(int(self.work_time_var.get())))
        self.work_label.pack(pady=(0, 20))
        ctk.CTkLabel(self, text="How Long Do You Plan To Take Breaks For ?", text_color="white", font=("Liberation Mono", 15)).pack(pady=(20, 0))
        ctk.CTkSlider(self, from_=5, to=7200, variable=self.break_time_var, width=200, command=lambda v: self.update_label(self.break_label, v)).pack(padx=20, pady=5, expand=True)
        self.break_label = ctk.CTkLabel(self, text=self.convert_hours_mins_secs(int(self.break_time_var.get())))
        self.break_label.pack(pady=(0, 20))
        frame = ctk.CTkFrame(self)
        frame.pack(pady=10)
        ctk.CTkButton(frame, text="<< Home", command=self.create_home_window).pack(side="left", padx=(0, 5))
        ctk.CTkButton(frame, text="Start", command=self.start_work).pack(side="left", padx=(5, 0))

    def convert_hours_mins_secs(self, time):
        time = int(time)
        hours, remainder = divmod(time, 3600)
        mins, secs = divmod(remainder, 60)
        return f"{hours:02d}:{mins:02d}:{secs:02d}"

    def update_label(self, label_widget, value):
        label_widget.configure(text=self.convert_hours_mins_secs(value))

    def clear_window(self):
        if self.timer_after_id: self.after_cancel(self.timer_after_id); self.timer_after_id = None
        for widget in self.winfo_children(): widget.destroy()

    def start_work(self):
        self.clear_window(); self.geometry('400x400')
        self.remaining_time = int(self.work_time_var.get())
        ctk.CTkLabel(self, text="Work Session", font=("Liberation Mono", 18)).pack(pady=(40, 0))
        self.timer_label = ctk.CTkLabel(self, text="", font=("Liberation Mono", 24)); self.timer_label.pack(pady=20)
        frame = ctk.CTkFrame(self); frame.pack()
        ctk.CTkButton(frame, text="<< Home", command=self.create_home_window).pack(side="left", padx=(20, 10))
        ctk.CTkButton(frame, text="Skip >>", command=self.skip_timer).pack(side="left", padx=(10, 20))
        self.update_countdown(self.show_break_transition)

    def show_break_transition(self):
        self.session_work_seconds += self.work_time_var.get()
        self.clear_window()
        transition_label = ctk.CTkLabel(self, text="Great work! Time for a break.", font=("Liberation Mono", 18)); transition_label.pack(pady=30)
        self.after(2000, lambda: transition_label.configure(text="Starting Break Timer . . ."))
        self.after(3000, self.start_break)

    def start_break(self):
        self.clear_window(); self.geometry('400x400')
        self.remaining_time = int(self.break_time_var.get())
        ctk.CTkLabel(self, text="Break Time", font=("Liberation Mono", 18)).pack(pady=(40, 0))
        self.timer_label = ctk.CTkLabel(self, text="", font=("Liberation Mono", 24)); self.timer_label.pack(pady=20)
        frame = ctk.CTkFrame(self); frame.pack()
        ctk.CTkButton(frame, text="<< Home", command=self.create_home_window).pack(side="left", padx=(20, 10))
        ctk.CTkButton(frame, text="Skip >>", command=self.skip_timer).pack(side="left", padx=(10, 20))
        self.update_countdown(self.end_break)

    def end_break(self):
        self.session_cycles += 1; self.session_break_seconds += self.break_time_var.get()
        print(f"Session stats: {self.session_cycles} cycles, {self.session_work_seconds:.0f}s work, {self.session_break_seconds:.0f}s break")
        data_manager.increment_today_cycle_count()
        self.clear_window(); self.geometry('400x400')
        ctk.CTkLabel(self, text="Break Finished. Well done!", font=("Liberation Mono", 18)).pack(pady=30)
        ctk.CTkButton(self, text="Start Next Work Session", command=self.start_work).pack(pady=10)
        ctk.CTkButton(self, text="Back to Home", command=self.create_home_window).pack(pady=10)

    def skip_timer(self):
        self.remaining_time = 0

    def update_countdown(self, on_finish_callback):
        if self.remaining_time >= 0:
            time_str = self.convert_hours_mins_secs(self.remaining_time)
            if self.timer_label.cget("text") != time_str: self.timer_label.configure(text=time_str)
            self.remaining_time -= 1
            self.timer_after_id = self.after(1000, lambda: self.update_countdown(on_finish_callback))
        else:
            self.after(500, on_finish_callback)

def main():
    App()

if __name__ == '__main__':
    main()