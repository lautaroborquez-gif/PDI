import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import imageio
import threading
import time
import os

def seconds_to_hhmmss(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

class SimpleVideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎞️ Reproductor de Video (con recorte y barra de progreso)")

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.scale = tk.Scale(root, from_=0, to=100, orient="horizontal", length=600,
                              command=self.on_scale_move)
        self.scale.pack(pady=5)

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="📂 Abrir video", command=self.load_video).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="▶ Play", command=self.play_video).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="⏸ Pausa", command=self.pause_video).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="⏮ Frame -", command=lambda: self.step_frame(-1)).grid(row=0, column=3, padx=5)
        tk.Button(control_frame, text="⏭ Frame +", command=lambda: self.step_frame(1)).grid(row=0, column=4, padx=5)
        tk.Button(control_frame, text="📍 IN", command=self.mark_in).grid(row=0, column=5, padx=5)
        tk.Button(control_frame, text="📍 OUT", command=self.mark_out).grid(row=0, column=6, padx=5)
        tk.Button(control_frame, text="✂ Recortar", command=self.cut_video).grid(row=0, column=7, padx=5)
        tk.Button(control_frame, text="🚪 Salir", command=root.quit).grid(row=0, column=8, padx=5)

        self.info_label = tk.Label(root, text="", font=("Arial", 10))
        self.info_label.pack()

        # Variables internas
        self.reader = None
        self.frame_index = 0
        self.playing = False
        self.marker_in = None
        self.marker_out = None
        self.fps = 60
        self.total_frames = 0
        self.video_path = None
        self.updating_scale = False

    def load_video(self):
        path = filedialog.askopenfilename(
            title="Selecciona un video",
            filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")]
        )
        if not path:
            return

        try:
            self.video_path = path
            self.reader = imageio.get_reader(path)
            meta = self.reader.get_meta_data()

            self.fps = meta.get("fps", 60)
            nframes = meta.get("fps",60)
            if nframes in [None,float("inf")] or nframes > 1e9:
                try:
                    nframes = self.reader.count_frames()
                except Exception:
                    nframes=0

            self.total_frames = int(nframes) if nframes > 0 else 0
            self.scale.config(to=self.total_frames - 1 if self.total_frames > 0 else 1)
            self.frame_index = 0
            self.update_frame()
            self.info_label.config(
                text=f"Video cargado: {os.path.basename(path)}\nFPS: {self.fps:.2f} | Total frames: {self.total_frames}"
            )
        except Exception as e:
            self.info_label.config(text=f"❌ Error cargando video: {e}")

    def update_frame(self):
        if not self.reader:
            return
        try:
            frame = self.reader.get_data(self.frame_index)
        except:
            return
        image = Image.fromarray(frame)
        image = image.resize((640, 360))
        imgtk = ImageTk.PhotoImage(image=image)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        current_time = self.frame_index / self.fps
        self.info_label.config(
            text=f"Frame: {self.frame_index+1}/{self.total_frames} | Tiempo: {seconds_to_hhmmss(current_time)}"
        )

        if not self.updating_scale:
            self.scale.set(self.frame_index)

    def play_video(self):
        if not self.reader:
            return
        self.playing = True
        threading.Thread(target=self._play_loop, daemon=True).start()

    def _play_loop(self):
        while self.playing and self.frame_index < self.total_frames - 1:
            self.frame_index += 1
            self.update_frame()
            time.sleep(1 / self.fps)

    def pause_video(self):
        self.playing = False

    def step_frame(self, step):
        if not self.reader:
            return
        self.frame_index = max(0, min(self.frame_index + step, self.total_frames - 1))
        self.update_frame()

    def on_scale_move(self, value):
        if not self.reader:
            return
        self.updating_scale = True
        self.frame_index = int(float(value))
        self.update_frame()
        self.updating_scale = False

    def mark_in(self):
        self.marker_in = self.frame_index / self.fps
        self.info_label.config(text=f"📍 Marcador IN: {seconds_to_hhmmss(self.marker_in)}")

    def mark_out(self):
        self.marker_out = self.frame_index / self.fps
        self.info_label.config(text=f"📍 Marcador OUT: {seconds_to_hhmmss(self.marker_out)}")

    def cut_video(self):
        if self.marker_in is None or self.marker_out is None:
            messagebox.showwarning("Aviso", "Primero marcá los puntos 📍 IN y 📍 OUT antes de recortar.")
            return
        if self.marker_in >= self.marker_out:
            messagebox.showerror("Error", "El punto IN debe ser anterior al punto OUT.")
            return
        if not self.reader or not self.video_path:
            messagebox.showerror("Error", "No hay video cargado.")
            return

        start_frame = int(self.marker_in * self.fps)
        end_frame = int(self.marker_out * self.fps)
        output_path = os.path.join(os.path.dirname(self.video_path), "video_recortado.mp4")

        try:
            writer = imageio.get_writer(output_path, fps=self.fps)
            for i in range(start_frame, min(end_frame, self.total_frames)):
                try:
                    frame = self.reader.get_data(i)
                    writer.append_data(frame)
                except:
                    break
            writer.close()
            messagebox.showinfo("✅ Recorte completado", f"El video recortado se guardó como:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo recortar el video:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleVideoPlayer(root)
    root.mainloop()
