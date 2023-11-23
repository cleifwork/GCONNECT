import os
import customtkinter
import subprocess
from PIL import Image

# Get the user's profile directory
user_profile = os.environ['USERPROFILE']
    
# Specify the wifi folder name as a variable
wifi_name = 'GCONNECT'
    
# Construct the full path
directory = os.path.join(user_profile, 'Desktop', wifi_name)

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

        self.title("WiFi Voucher Launchpad")
        self.geometry("300x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.logo_frame = MyLogoFrame(self, " STREAM | PLAY | ENJOY ", logo_path="./img/launchpad_logo.png")
        self.logo_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")      

        self.button_1 = customtkinter.CTkButton(self, text="EXTRACT VCODES", font=('Arial', 15), height=45, fg_color="#007dfe", hover_color="#0057b0", command=self.clean_csv)
        self.button_1.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.button_2 = customtkinter.CTkButton(self, text="UPLOAD VCODES", font=('Arial', 15), height=45, fg_color="#007dfe", hover_color="#0057b0", command=self.upload_voucher)
        self.button_2.grid(row=2, column=0, padx=10, pady=5, sticky="ew")        

        self.button_3 = customtkinter.CTkButton(self, text="SYNC GDRIVE-MD", font=('Arial', 15), height=45, fg_color="#007dfe", hover_color="#0057b0", command=self.sync_gdrivemd)
        self.button_3.grid(row=3, column=0, padx=10, pady=5, sticky="ew")        

        self.button_4 = customtkinter.CTkButton(self, text="EXTRUP VCODES", font=('Arial', 15), height=45, fg_color="#007dfe", hover_color="#0057b0", command=self.cleanup_csv)
        self.button_4.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        
        self.button_5 = customtkinter.CTkButton(self, text="PRINT VOUCHERS", font=('Arial', 15), height=45, fg_color="#007dfe", hover_color="#0057b0", command=self.print_voucher)
        self.button_5.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        # Footer
        self.footer_frame = customtkinter.CTkFrame(self)
        self.footer_frame.grid(row=6, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.footer_label = customtkinter.CTkLabel(self.footer_frame, 
                                                   text="\nCopyright © 2023 Toto's Digital Services Ltd. \nAll rights reserved. \n",
                                                   font=("Arial", 9))
        self.footer_label.pack()

    def clean_csv(self):
        subprocess.run(["python", "CleanCSV.py"])        

    def cleanup_csv(self):
        subprocess.run(["python", "CleanUpCSV.py"])

    def sync_gdrivemd(self):
        script_path = os.path.join(directory, "SyncGDriveMD.bat")
        subprocess.run([script_path])   

    def upload_voucher(self):
        subprocess.run(["python", "UpCSV.py"])

    def print_voucher(self):
        script_path = os.path.join(directory, "PrintVoucherServer.bat")
        subprocess.run([script_path])

app = App()
app.mainloop()
