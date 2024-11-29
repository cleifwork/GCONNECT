import os
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

        self.title("GConnect V3")
        self.geometry("300x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Correctly resolve logo path
        logo_path = os.path.join(exe_dir, "img", "launchpad_logo.png")
        self.logo_frame = MyLogoFrame(self, "WIFI VOUCHER SOLUTION", logo_path=logo_path)
        self.logo_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")      

        self.button_1 = customtkinter.CTkButton(self, text="RUN INITIAL CONFIG", font=('Arial', 15), height=45, fg_color="#007dfe", hover_color="#0057b0", command=self.ini_config)
        self.button_1.grid(row=1, column=0, padx=10, pady=5, sticky="ew")               

        self.button_4 = customtkinter.CTkButton(self, text="EXTRUP & SYNC", font=('Arial', 15), height=45, fg_color="#007dfe", hover_color="#0057b0", command=self.upsync_csv)
        self.button_4.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        
        self.button_5 = customtkinter.CTkButton(self, text="PRINT VOUCHERS", font=('Arial', 15), height=45, fg_color="#007dfe", hover_color="#0057b0", command=self.print_voucher)
        self.button_5.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        # Footer
        self.footer_frame = customtkinter.CTkFrame(self)
        self.footer_frame.grid(row=6, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.footer_label = customtkinter.CTkLabel(self.footer_frame, 
                                                   text="\nCopyright © 2024 Toto's Digital Services Ltd. \nAll rights reserved. \n",
                                                   font=("Arial", 9))
        self.footer_label.pack()
        
    def ini_config(self):
        try:
            sub.run([python_exe, os.path.join(exe_dir, "IniConfig.py")], check=True)
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except sub.CalledProcessError as e:
            print(f"Script error: {e}")

    def upsync_csv(self):
        try:
            sub.run([python_exe, os.path.join(exe_dir, "CleanUpSynCSV.py")], check=True)
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except sub.CalledProcessError as e:
            print(f"Script error: {e}")

    def print_voucher(self):
        try:
            sub.run([python_exe, os.path.join(exe_dir, "PrintVoucherServer.py")], check=True)
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except sub.CalledProcessError as e:
            print(f"Script error: {e}")                        


app = App()
app.mainloop()
