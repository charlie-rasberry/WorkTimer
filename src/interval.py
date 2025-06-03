from tkinter import messagebox as mbx
import customtkinter as ctk

# --- interval.py --- One-Filer Simple App as An Easy Way to Track Your Work in Intervals ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Timer state variables
        self.timer_after_id = None
        self.remaining_time = None

        # Appearance and window setup
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("work-interval-app")
        self.geometry('400x400')

        # Interval values
        self.work_time_var = ctk.DoubleVar(value=1800)
        self.break_time_var = ctk.DoubleVar(value=300)

        # Display the configuration window
        self.configuration_window()
        self.mainloop()

    def configuration_window(self):
        self.clear_window()

        # Work timer config
        ctk.CTkLabel(self, text="How Long Will You Work For ?", text_color="white", font=("Liberation Mono", 15)).pack(pady=(20, 0))
        ctk.CTkSlider(self, from_=5, to=7200, variable=self.work_time_var, width=200).pack(padx=100, pady=20, expand=True)

        # Break timer config
        ctk.CTkLabel(self, text="How Long Do You Plan To Take Breaks For ?", text_color="white", font=("Liberation Mono", 15)).pack(pady=(20, 0))
        ctk.CTkSlider(self, from_=5, to=7200, variable=self.break_time_var, width=200).pack(padx=20, pady=20, expand=True)

        # Start button
        ctk.CTkButton(self, text="Start", command=self.start_work).pack(pady=10)

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

        ctk.CTkButton(self, text="<< Menu", command=self.configuration_window).pack(pady=10)
        ctk.CTkButton(self, text="Skip >>", command=self.skip_timer).pack(pady=10)

        self.update_countdown(self.start_break)

    def start_break(self):
        self.clear_window()
        mbx.showinfo("Timer Finished", "Begin A Short Break Now!")

        self.remaining_time = int(self.break_time_var.get())
        self.timer_label = ctk.CTkLabel(self, text="Break Time", font=("Liberation Mono", 24))
        self.timer_label.pack(pady=20)

        ctk.CTkButton(self, text="<< Menu", command=self.configuration_window).pack(pady=10)
        ctk.CTkButton(self, text="Skip >>", command=self.skip_timer).pack(pady=10)

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
