import os
import threading 
import customtkinter
import subprocess as sub
from PIL import Image
from utils import exe_dir, python_exe


class MyLogoFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, logo_path):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.logo_path = logo_path

        self.title_label = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.logo = customtkinter.CTkImage(Image.open(self.logo_path), size=(240, 150))
        self.logo_label = customtkinter.CTkLabel(self, image=self.logo, text="")
        self.logo_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Define reusable fonts
        try:
            self.button_font = customtkinter.CTkFont(family="Arial Rounded MT Bold", size=15)
        except Exception:  # Fallback if Arial Rounded MT Bold isn't available
            self.button_font = customtkinter.CTkFont(family="Arial", size=15)

        # Define reusable button styles
        self.button_styles = {
            "font": self.button_font,
            "height": 45,
            "fg_color": "#007dfe",
            "hover_color": "#0057b0",
        }

        self.title("GConnect V3")
        self.geometry("300x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Correctly resolve logo path
        logo_path = os.path.join(exe_dir, "img", "launchpad_logo.png")
        self.logo_frame = MyLogoFrame(self, "WIFI VOUCHER SOLUTION", logo_path=logo_path)
        self.logo_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.button_1 = customtkinter.CTkButton(
            self,
            text="RUN INITIAL CONFIG",
            command=lambda: self.run_in_thread(self.ini_config),
            **self.button_styles,  # Apply reusable styles
        )
        self.button_1.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.button_4 = customtkinter.CTkButton(
            self,
            text="EXTRUP & SYNC",
            command=lambda: self.run_in_thread(self.upsync_csv),
            **self.button_styles,  # Apply reusable styles
        )
        self.button_4.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.button_5 = customtkinter.CTkButton(
            self,
            text="PRINT VOUCHERS",
            command=lambda: self.run_in_thread(self.print_voucher),
            **self.button_styles,  # Apply reusable styles
        )
        self.button_5.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        # Footer
        self.footer_frame = customtkinter.CTkFrame(self)
        self.footer_frame.grid(row=6, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.footer_label = customtkinter.CTkLabel(
            self.footer_frame,
            text="\nCopyright © 2024 Toto's Digital Services Ltd. \nAll rights reserved. \n",
            font=("Arial", 9),
        )
        self.footer_label.pack()

        self.lock = threading.Lock()  # Lock to prevent concurrent execution

    def run_in_thread(self, func):
        if self.lock.locked():
            print("Another script is already running. Please wait.")
            return

        thread = threading.Thread(target=func)
        thread.start()

    def execute_script(self, script_path):
        with self.lock:
            try:
                # Use Popen to execute the script
                process = sub.Popen(
                    [python_exe, script_path],
                    stdout=sub.PIPE,
                    stderr=sub.PIPE,
                    text=True,
                )

                # Stream the output in real-time
                for line in process.stdout:
                    print(line.strip())

                process.wait()  # Wait for the process to complete
                if process.returncode != 0:
                    print(f"Script error: {process.stderr.read().strip()}")

            except FileNotFoundError as e:
                print(f"Error: {e}")

    def ini_config(self):
        self.execute_script(os.path.join(exe_dir, "IniConfig.py"))

    def upsync_csv(self):
        self.execute_script(os.path.join(exe_dir, "CleanUpSynCSV.py"))

    def print_voucher(self):
        self.execute_script(os.path.join(exe_dir, "PrintVoucherServer.py"))


app = App()
app.mainloop()