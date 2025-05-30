import customtkinter as ctk

class App(ctk.CTk):
    # Initialise the CTK app
    def __init__(self):
        super().__init__()

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
        # Label above the slider
        label = ctk.CTkLabel(self, text="How Long Will You Work For ?", text_color="white")
        label.pack(pady=(0, 10))

        # Work time variable and slider
        self.work_time_var = ctk.DoubleVar(value=30)
        slider = ctk.CTkSlider(self, from_=5, to=120, variable=self.work_time_var, width=200)
        slider.pack(padx=100, pady=60, expand=True)

        # Start button
        start_button = ctk.CTkButton(self, text="Start", command=self.go)
        start_button.pack(pady=10)

    # Start button action
    def go(self):
        work_time = self.work_time_var.get()
        print(f"Work time set to: {work_time} minutes")
        # This is where you'd swap to a timer screen

# Entry point
def main():
    App()

if __name__ == '__main__':
    main()
