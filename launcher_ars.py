import customtkinter as ctk
import subprocess
import os
import sys
import time
import platform
import psutil
import webbrowser
from PIL import Image

ctk.set_appearance_mode("Dark")

class ArsCraftLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.base_path = os.path.dirname(os.path.realpath(__file__))
        self.github_url = "https://github.com/Ars-byte"
        
        self.os_info = platform.system().lower()
        self.kernel_info = platform.version() if platform.system() == "Windows" else platform.release()
        self.cpu_info = self.get_cpu_info()
        self.gpu_info = self.get_gpu_info()

        self.title("Arscraft-launcher")
        self.geometry("550x480")
        self.resizable(False, False)
        self.configure(fg_color="#000000")

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(30, 20), padx=30, fill="x")

        img_path = os.path.join(self.base_path, "assets", "github_avatar.png")
        if os.path.exists(img_path):
            my_image = ctk.CTkImage(light_image=Image.open(img_path),
                                    dark_image=Image.open(img_path),
                                    size=(60, 60))
            self.profile_pic = ctk.CTkLabel(self.header_frame, image=my_image, text="")
            self.profile_pic.pack(side="left", padx=(0, 15))
        
        self.title_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.title_container.pack(side="left", fill="y")

        self.title_label = ctk.CTkLabel(
            self.title_container, 
            text="Arscraft-launcher", 
            font=("Inter", 24, "bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(anchor="w")

        self.link_label = ctk.CTkLabel(
            self.title_container,
            text="my github profile: github.com/Ars-byte",
            font=("Inter", 11),
            text_color="#666666",
            cursor="hand2"
        )
        self.link_label.pack(anchor="w")
        self.link_label.bind("<Button-1>", lambda e: webbrowser.open(self.github_url))

        self.info_box = ctk.CTkTextbox(
            self, 
            fg_color="#121212", 
            text_color="#a0a0a0", 
            border_color="#252525",
            border_width=1,
            corner_radius=15,
            font=("Monospace", 11),
            padx=20,
            pady=20
        )
        self.info_box.pack(expand=True, fill="both", padx=30, pady=(0, 30))
        
        self.info_box.insert("0.0", f"system: {self.os_info}\n")
        self.info_box.insert("end", f"kernel: {self.kernel_info}\n")
        self.info_box.insert("end", f"cpu:    {self.cpu_info}\n")
        self.info_box.insert("end", f"gpu:    {self.gpu_info}\n")
        self.info_box.insert("end", "—" * 30 + "\n")
        self.info_box.insert("end", f"status: link {self.github_url} ready\n")
        self.info_box.configure(state="disabled")

        self.launch_btn = ctk.CTkButton(
            self, 
            text="Launch Application", 
            command=self.launch,
            fg_color="#ffffff", 
            text_color="#000000",
            hover_color="#d1d1d1",
            font=("Inter", 14, "bold"),
            corner_radius=12,
            height=50
        )
        self.launch_btn.pack(pady=(0, 40), padx=30, fill="x")

    def get_cpu_info(self):
        if platform.system() == "Windows":
            return platform.processor()
        else:
            try:
                return subprocess.check_output("grep -m 1 'model name' /proc/cpuinfo | cut -d: -f2", shell=True).decode().strip()
            except:
                return platform.processor()

    def get_gpu_info(self):
        try:
            if platform.system() == "Windows":
                cmd = "wmic path win32_VideoController get name"
                gpu_data = subprocess.check_output(cmd, shell=True).decode().split("\n")
                return gpu_data[1].strip()
            else:
                gpu_data = subprocess.check_output("lspci | grep -E 'VGA|3D'", shell=True).decode().strip()
                return gpu_data.split(": ")[-1] if ":" in gpu_data else gpu_data
        except:
            return "unknown graphics"

    def write_log(self, text):
        self.info_box.configure(state="normal")
        self.info_box.insert("end", f"> {text}\n")
        self.info_box.see("end")
        self.info_box.configure(state="disabled")
        self.update()

    def launch(self):
        self.launch_btn.configure(state="disabled", text="RUNNING...")
        self.write_log("Starting Arscraft...")
        
        game_path = os.path.join(self.base_path, "main.py")

        if os.path.exists(game_path):
            self.write_log("Initializing environment...")
            time.sleep(0.5)
            self.withdraw()
            try:
                subprocess.run([sys.executable, game_path], check=True, cwd=self.base_path)
            except Exception as e:
                self.deiconify()
                self.write_log(f"ERROR: {str(e)}")
            finally:
                self.destroy()
        else:
            self.write_log("CRITICAL: 'main.py' not found.")
            self.launch_btn.configure(state="normal", text="Launch Application")

if __name__ == "__main__":
    app = ArsCraftLauncher()
    app.mainloop()
