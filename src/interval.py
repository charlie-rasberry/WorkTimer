from tkinter import messagebox as mbx
import customtkinter as ctk

# TODO
#   1. Create JSON file to store daily cycle counts persistently.
#   2. Implement functions to load and save cycle data.
#   3. Increment today's cycle count on each cycle completion.
#   4. Design a calendar-style heatmap like GitHub contribution graph:
#   - Map cycle counts to green shades.
#   - Add hover tooltips showing cycle count per day.
#   5. Integrate heatmap UI into the app.
#   6. Test data persistence and visual correctness.
#   7. Add documentation and comments for maintainability.


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.work_label = None
        self.break_label = None
        self.timer_label = None
        self.timer_after_id = None
        self.remaining_time = None

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("work-interval-app")
        self.geometry('400x400')

        self.work_time_var = ctk.DoubleVar(value=1800)
        self.break_time_var = ctk.DoubleVar(value=300)

        self.configuration_window()
        self.mainloop()

    def configuration_window(self):
        self.clear_window()

        ctk.CTkLabel(self, text="How Long Will You Work For ?", text_color="white", font=("Liberation Mono", 15)).pack(pady=(20, 0))
        ctk.CTkSlider(self, from_=5, to=7200, variable=self.work_time_var, width=200,
                      command=lambda v: self.update_label(self.work_label, v)).pack(padx=100, pady=5, expand=True)
        work_time_in_hrs_min_sec = self.convert_hours_mins_secs(int(self.break_time_var.get()))
        self.work_label = ctk.CTkLabel(self, text=work_time_in_hrs_min_sec)
        self.work_label.pack(pady=(0, 20))

        ctk.CTkLabel(self, text="How Long Do You Plan To Take Breaks For ?", text_color="white", font=("Liberation Mono", 15)).pack(pady=(20, 0))
        ctk.CTkSlider(self, from_=5, to=7200, variable=self.break_time_var, width=200,
                      command=lambda v: self.update_label(self.break_label, v)).pack(padx=20, pady=5, expand=True)
        break_time_in_hrs_min_sec = self.convert_hours_mins_secs(int(self.break_time_var.get()))
        self.break_label = ctk.CTkLabel(self, text=break_time_in_hrs_min_sec)
        self.break_label.pack(pady=(0, 20))

        ctk.CTkButton(self, text="Start", command=self.start_work).pack(pady=10)

    def convert_hours_mins_secs(self, time):
        hours = time // 3600
        mins = (time % 3600) // 60
        secs = time % 60
        time_str = f"{hours:02d}:{mins:02d}:{secs:02d}"
        return time_str

    def update_label(self, label_widget, value):
        time_str = self.convert_hours_mins_secs(int(float(value)))
        label_widget.configure(text=time_str)

    def clear_window(self):
        if self.timer_after_id:
            self.after_cancel(self.timer_after_id)
            self.timer_after_id = None
        for widget in self.winfo_children():
            widget.destroy()

    def start_work(self):
        self.clear_window()
        self.remaining_time = int(self.work_time_var.get())

        self.timer_label = ctk.CTkLabel(self, text="", font=("Liberation Mono", 24))
        self.timer_label.pack(pady=20)

        frame = ctk.CTkFrame(self)
        frame.pack()

        ctk.CTkButton(frame, text="<< Menu", command=self.configuration_window).pack(side="left", padx=(20, 10))
        ctk.CTkButton(frame, text="Skip >>", command=self.skip_timer).pack(side="left", padx=(10, 20))

        self.update_countdown(self.show_break_transition)

    def show_break_transition(self):
        self.clear_window()

        transition_label = ctk.CTkLabel(self, text="Go For a Short Break", font=("Liberation Mono", 18))
        transition_label.pack(pady=30)

        self.after(3000, lambda: transition_label.configure(text="Starting Break Timer . . ."))

        self.after(4000, lambda: (
            mbx.showinfo("Timer Finished", "Begin A Short Break Now!"),
            self.start_break()
        ))

    def start_break(self):
        self.clear_window()
        self.remaining_time = int(self.break_time_var.get())

        self.timer_label = ctk.CTkLabel(self, text="Break Time", font=("Liberation Mono", 24))
        self.timer_label.pack(pady=20)

        frame = ctk.CTkFrame(self)
        frame.pack()

        ctk.CTkButton(frame, text="<< Menu", command=self.configuration_window).pack(side="left", padx=(20, 10))
        ctk.CTkButton(frame, text="Skip >>", command=self.skip_timer).pack(side="left", padx=(10, 20))

        self.update_countdown(self.end_break)

    def end_break(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Break Finished. Good job!", font=("Liberation Mono", 18)).pack(pady=30)
        ctk.CTkButton(self, text="Start Again", command=self.start_work).pack(pady=10)
        ctk.CTkButton(self, text="Back to Menu", command=self.configuration_window).pack(pady=10)

    def skip_timer(self):
        self.remaining_time = 0

    def update_countdown(self, on_finish_callback):
        if self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            time_str = f"{mins:02d}:{secs:02d}"
            self.timer_label.configure(text=time_str)
            self.remaining_time -= 1
            self.timer_after_id = self.after(1000, lambda: self.update_countdown(on_finish_callback))
        else:
            on_finish_callback()


# Entry point
def main():
    App()

if __name__ == '__main__':
    main()
