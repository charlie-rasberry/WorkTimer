import customtkinter as ctk


def go():
    work_time = work_time_var.get()
    print(f"Work time set to: {work_time} minutes")


def main():
    # Set global appearance settings
    ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"
    ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

    # Initialise the window
    root = ctk.CTk()
    root.title("work-interval-app")
    root.geometry('400x400')

    # Label above the slider
    label = ctk.CTkLabel(root, text="How Long Will You Work For ?", text_color="white")
    label.pack(pady=(0, 10))

    # Work time variable and slider
    global work_time_var
    work_time_var = ctk.DoubleVar(value=30)

    slider = ctk.CTkSlider(root, from_=5, to=120, variable=work_time_var, width=200)
    slider.pack(padx=100, pady=60, expand=True)

    # Start button
    start_button = ctk.CTkButton(root, text="Start", command=go)
    start_button.pack(pady=10)

    root.mainloop()


if __name__ == '__main__':
    main()
