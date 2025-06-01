from tkinter import messagebox as mbx
import customtkinter as ctk
import time

class App(ctk.CTk):
    # Initialise the CTK app

    def __init__(self):
        super().__init__()

        #   some attrs
        self.timer_after_id = None
        self.remaining_time = None
        self.temp = None
        self.timer_label = None
        self.t = None
        self.start_button = None
        self.config_slider = None
        self.config_label = None
        self.work_time_var = None
        # Appearance settings
        ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"
        ctk.set_default_color_theme("blue")

        # Window setup
        self.title("work-interval-app")
        self.geometry('400x400')

        # Show the config screen
        self.configuration_window()

        # Start the event loop
        self.mainloop()


    # Configuration screen
    def configuration_window(self):

        # default val for time
        self.work_time_var = ctk.DoubleVar(value=30)
        
        # Label above the slider
        self.config_label = ctk.CTkLabel(self, text="How Long Will You Work For ?", text_color="white")
        self.config_label.pack(pady=(0, 10))

        # Work time variable and slider
        self.config_slider = ctk.CTkSlider(self, from_=5, to=120, variable=self.work_time_var, width=200)
        self.config_slider.pack(padx=100, pady=60, expand=True)

        # Start button
        self.start_button = ctk.CTkButton(self, text="Start", command=self.go)
        self.start_button.pack(pady=10)

    #   helper to wipe a window
    def clear_window(self):
        # root.destroy()
        for widget in self.winfo_children():
            widget.pack_forget()

# Start button action
    #   change window to display a timer and a back button and wait til timer runs out to run break
    def go(self):
        work_time_seconds = int(self.work_time_var.get())
        self.clear_window()
        self.remaining_time = work_time_seconds
        self.timer_label = ctk.CTkLabel(self, text="", font=("Arial", 24))
        self.timer_label.pack(pady=20)
        self.update_countdown() # Start the process

    def update_countdown(self):
        if self.remaining_time > 0:
            # 1. Display current time
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
            # 2. Decrement time
            self.remaining_time -= 1
            # 3. Reschedule THIS function for the next second
            self.timer_after_id = self.after(1000, self.update_countdown)
        else:
            # Time is up: Perform final action
            self.timer_label.configure(text="Time's Up!")
            mbx.showinfo("Timer Finished", "Begin A Short Break Now!")
            # Optionally, reset or go to another screen
            # self.clear_window()
            # self.configuration_window()



# Entry point
def main():
    App()

if __name__ == '__main__':
    main()
