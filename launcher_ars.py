import customtkinter as ctk
import subprocess
import os
import sys
import time

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

class QtLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.base_path = os.path.dirname(os.path.realpath(__file__))
        
        self.title("Ursina Project Manager")
        self.geometry("550x400")
        self.resizable(False, False)
        self.configure(fg_color="#1a1a1a")

        self.header_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", height=70, corner_radius=0)
        self.header_frame.pack(fill="x", side="top")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="URSINA CRAFT", 
            font=("Ubuntu", 24, "bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(pady=15, padx=20, side="left")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=20)

        self.info_box = ctk.CTkTextbox(
            self.main_frame, 
            fg_color="#000000", 
            text_color="#e0e0e0", 
            border_color="#404040",
            border_width=1,
            font=("Monospace", 12)
        )
        self.info_box.pack(expand=True, fill="both", pady=(0, 20))
        self.info_box.insert("0.0", "Estado: Sistema listo\nDirectorio: " + self.base_path + "\n")
        self.info_box.configure(state="disabled")

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="x", side="bottom", padx=30, pady=20)

        self.launch_btn = ctk.CTkButton(
            self.button_frame, 
            text="Launch Application", 
            command=self.launch,
            fg_color="#ffffff",
            text_color="#000000",
            hover_color="#cccccc",
            font=("Arial", 14, "bold"),
            corner_radius=4,
            height=40
        )
        self.launch_btn.pack(side="right", padx=(10, 0))

        self.exit_btn = ctk.CTkButton(
            self.button_frame, 
            text="Exit", 
            command=self.quit,
            fg_color="#333333", 
            text_color="#ffffff",
            hover_color="#444444",
            width=80,
            height=40,
            corner_radius=4
        )
        self.exit_btn.pack(side="right")

    def write_log(self, text):
        self.info_box.configure(state="normal")
        self.info_box.insert("end", f"[INFO] {text}\n")
        self.info_box.see("end")
        self.info_box.configure(state="disabled")
        self.update()

    def launch(self):
        self.launch_btn.configure(state="disabled", text="Running...")
        self.write_log("Iniciando secuencia de ejecución...")
        
        game_path = os.path.join(self.base_path, "main.py")

        if os.path.exists(game_path):
            self.write_log("Cargando módulos de Ursina...")
            time.sleep(0.4)
            self.withdraw()
            
            try:
                subprocess.run([sys.executable, game_path], check=True, cwd=self.base_path)
            except Exception as e:
                self.deiconify()
                self.write_log(f"ERROR: {str(e)}")
            finally:
                self.destroy()
        else:
            self.write_log("CRITICAL: 'main.py' no detectado.")
            self.launch_btn.configure(state="normal", text="Launch Application")

if __name__ == "__main__":
    app = QtLauncher()
    app.mainloop()