import cv2
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk
from gui.theme import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("DocScan Pro")
        self.geometry("600x400")
        self.overrideredirect(True) # Remove window borders
        self.configure(fg_color=BG_DARK)
        
        # Center on screen
        self.update_idletasks()
        width = 600
        height = 400
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self._build_ui()
        self.attributes("-topmost", True)
        
    def _build_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color=BG_MEDIUM, corner_radius=20, border_width=2, border_color=ACCENT_PRIMARY)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Title
        ctk.CTkLabel(main_frame, text="DocScan Pro", font=("Segoe UI", 36, "bold"), text_color=ACCENT_PRIMARY).pack(pady=(40, 5))
        ctk.CTkLabel(main_frame, text="Document Scanner & OCR Pre-processor", font=("Segoe UI", 16), text_color=TEXT_PRIMARY).pack()
        
        # Details
        details_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        details_frame.pack(pady=30)
        
        ctk.CTkLabel(details_frame, text="Air University Multan Campus", font=("Segoe UI", 14, "bold"), text_color=ACCENT_YELLOW).pack()
        ctk.CTkLabel(details_frame, text="Course: CS 345 - Digital Image Processing", font=("Segoe UI", 12), text_color=TEXT_SECONDARY).pack(pady=2)
        ctk.CTkLabel(details_frame, text="Instructor: Sir Muhammad Faisal Idrees", font=("Segoe UI", 12), text_color=TEXT_SECONDARY).pack(pady=2)
        
        # Loading bar
        self.progress_lbl = ctk.CTkLabel(main_frame, text="Initializing components...", font=("Segoe UI", 10), text_color=TEXT_DIM)
        self.progress_lbl.pack(side="bottom", pady=(0, 20))
        
        self.progressbar = ctk.CTkProgressBar(main_frame, width=400, height=8, progress_color=ACCENT_PRIMARY)
        self.progressbar.pack(side="bottom", pady=(0, 10))
        self.progressbar.set(0)
        
    def update_progress(self, value, text):
        self.progressbar.set(value)
        self.progress_lbl.configure(text=text)
        self.update()


class MetricCard(ctk.CTkFrame):
    def __init__(self, master, title, unit="", color=ACCENT_PRIMARY, **kwargs):
        super().__init__(master, fg_color=BG_CARD, corner_radius=10, height=75, **kwargs)
        self.pack_propagate(False)
        self.unit = unit
        
        # Title
        self.lbl_title = ctk.CTkLabel(self, text=title, font=FONT_METRIC_LBL, text_color=TEXT_SECONDARY)
        self.lbl_title.pack(anchor="w", padx=12, pady=(8, 0))
        
        # Value
        self.lbl_val = ctk.CTkLabel(self, text=f"-- {unit}", font=FONT_METRIC_VAL, text_color=color)
        self.lbl_val.pack(anchor="w", padx=12, pady=(0, 5))
        
    def set_value(self, value):
        self.lbl_val.configure(text=f"{value} {self.unit}")


class SectionHeader(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        lbl = ctk.CTkLabel(self, text=title, font=("Segoe UI", 11, "bold"), text_color=ACCENT_PRIMARY)
        lbl.pack(anchor="w", padx=10, pady=(15, 2))
        
        line = ctk.CTkFrame(self, fg_color=BORDER_COLOR, height=1)
        line.pack(fill="x", padx=10, pady=(0, 8))


class ImageDisplay(ctk.CTkFrame):
    """
    Advanced Image Display component supporting:
    - Normal viewing
    - Pixel Magnifier (Zoom tool on hover)
    - Before/After interactive slider (Drag to compare)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BG_CARD, corner_radius=12, **kwargs)
        self.pack_propagate(False)
        
        self.mode = "normal"  # normal, magnifier, compare
        self.img_before = None
        self.img_after = None
        self.tk_img = None
        self.tk_img_before = None
        
        # Use Tkinter Canvas for advanced drawing
        import tkinter as tk
        self.canvas = tk.Canvas(self, bg=BG_CARD, highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<Leave>", self._on_mouse_leave)
        
        self.slider_pos = 0.5 # 50% split for compare mode
        self.zoom_size = 150
        self.zoom_factor = 4
        
        self.canvas.create_text(
            self.winfo_width()//2, self.winfo_height()//2, 
            text="Please load a document image to begin processing.", 
            fill=TEXT_DIM, font=("Segoe UI", 14), tags="placeholder"
        )
        self.bind("<Configure>", self._on_resize)
        self.w = 100
        self.h = 100

    def _on_resize(self, event):
        self.w = event.width
        self.h = event.height
        if self.mode == "compare" and self.img_before is not None and self.img_after is not None:
            self.set_compare(self.img_before, self.img_after)
        elif self.img_after is not None:
            self.update_image(self.img_after)
        else:
            self.canvas.coords("placeholder", self.w//2, self.h//2)

    def set_mode(self, mode):
        self.mode = mode
        self._redraw()
        
    def set_compare(self, img_before, img_after):
        self.img_before = img_before
        self.img_after = img_after
        self.mode = "compare"
        self._redraw()
        
    def update_image(self, img):
        if img is None: return
        self.img_after = img
        if self.mode == "compare": self.mode = "normal"
        self._redraw()
        
    def _redraw(self):
        self.canvas.delete("all")
        if self.img_after is None:
            self.canvas.create_text(
                self.w//2, self.h//2, 
                text="Please load a document image to begin processing.", 
                fill=TEXT_DIM, font=("Segoe UI", 14), tags="placeholder"
            )
            return
            
        w, h = max(100, self.w-10), max(100, self.h-10)
        
        from gui.image_utils import resize_for_display, cv2_to_tk
        
        if self.mode == "compare" and self.img_before is not None:
            # Resize both to same dimensions
            resized_b = resize_for_display(self.img_before, max_w=w, max_h=h)
            resized_a = resize_for_display(self.img_after, max_w=w, max_h=h)
            
            self.tk_img_before = cv2_to_tk(resized_b, (w,h))
            self.tk_img = cv2_to_tk(resized_a, (w,h))
            
            if not self.tk_img or not self.tk_img_before: return
            
            img_w, img_h = self.tk_img.width(), self.tk_img.height()
            x_offset = (w - img_w) // 2 + 5
            y_offset = (h - img_h) // 2 + 5
            
            split_x = int(img_w * self.slider_pos)
            
            # Draw before (left)
            self.canvas.create_image(x_offset, y_offset, anchor="nw", image=self.tk_img_before, tags="img_b")
            # Draw after (right) - crop using a window
            self.canvas.create_window(x_offset + split_x, y_offset, anchor="nw", 
                                      window=self._create_cropped_frame(self.tk_img, split_x, img_w, img_h),
                                      tags="img_a")
            
            # Draw slider line
            line_x = x_offset + split_x
            self.canvas.create_line(line_x, y_offset, line_x, y_offset+img_h, fill=ACCENT_PRIMARY, width=3, tags="slider")
            self.canvas.create_oval(line_x-8, y_offset+img_h//2-8, line_x+8, y_offset+img_h//2+8, fill=ACCENT_PRIMARY, outline="white", tags="slider_handle")
            
            # Labels
            self.canvas.create_text(x_offset+10, y_offset+10, text="BEFORE", fill="white", anchor="nw", font=("Segoe UI", 12, "bold"))
            self.canvas.create_text(x_offset+img_w-10, y_offset+10, text="AFTER", fill="white", anchor="ne", font=("Segoe UI", 12, "bold"))
            
        else:
            # Normal or Magnifier
            resized = resize_for_display(self.img_after, max_w=w, max_h=h)
            self.tk_img = cv2_to_tk(resized, (w,h))
            if self.tk_img:
                x_offset = (w - self.tk_img.width()) // 2 + 5
                y_offset = (h - self.tk_img.height()) // 2 + 5
                self.canvas.create_image(x_offset, y_offset, anchor="nw", image=self.tk_img, tags="img")

    def _create_cropped_frame(self, tk_img, start_x, w, h):
        import tkinter as tk
        f = tk.Frame(self.canvas, width=w-start_x, height=h, bg=BG_CARD)
        lbl = tk.Label(f, image=tk_img, bg=BG_CARD, borderwidth=0)
        lbl.place(x=-start_x, y=0)
        return f

    def _on_mouse_drag(self, event):
        if self.mode != "compare" or not self.tk_img: return
        w = max(100, self.w-10)
        img_w = self.tk_img.width()
        x_offset = (w - img_w) // 2 + 5
        
        # Calculate new pos
        rel_x = event.x - x_offset
        self.slider_pos = max(0.01, min(0.99, rel_x / img_w))
        self._redraw()

    def _on_mouse_move(self, event):
        if self.mode != "magnifier" or self.img_after is None or not self.tk_img: return
        
        self.canvas.delete("mag")
        
        w, h = max(100, self.w-10), max(100, self.h-10)
        img_w, img_h = self.tk_img.width(), self.tk_img.height()
        x_offset = (w - img_w) // 2 + 5
        y_offset = (h - img_h) // 2 + 5
        
        # Check if inside image
        if not (x_offset <= event.x <= x_offset+img_w and y_offset <= event.y <= y_offset+img_h):
            return
            
        # Calculate coordinate in original image
        rel_x = event.x - x_offset
        rel_y = event.y - y_offset
        
        orig_h, orig_w = self.img_after.shape[:2]
        orig_x = int((rel_x / img_w) * orig_w)
        orig_y = int((rel_y / img_h) * orig_h)
        
        # Extract patch
        patch_size = self.zoom_size // self.zoom_factor
        y1 = max(0, orig_y - patch_size//2)
        y2 = min(orig_h, orig_y + patch_size//2)
        x1 = max(0, orig_x - patch_size//2)
        x2 = min(orig_w, orig_x + patch_size//2)
        
        patch = self.img_after[y1:y2, x1:x2].copy()
        if patch.size == 0: return
        
        # Resize patch
        zoomed = cv2.resize(patch, (self.zoom_size, self.zoom_size), interpolation=cv2.INTER_NEAREST)
        
        from gui.image_utils import cv2_to_tk
        self.tk_mag_img = cv2_to_tk(zoomed, (self.zoom_size, self.zoom_size))
        
        # Draw glass
        mag_x = event.x + 20
        mag_y = event.y + 20
        # Prevent going off screen
        if mag_x + self.zoom_size > self.w: mag_x = event.x - self.zoom_size - 20
        if mag_y + self.zoom_size > self.h: mag_y = event.y - self.zoom_size - 20
        
        self.canvas.create_image(mag_x, mag_y, anchor="nw", image=self.tk_mag_img, tags="mag")
        self.canvas.create_rectangle(mag_x, mag_y, mag_x+self.zoom_size, mag_y+self.zoom_size, outline=ACCENT_PRIMARY, width=2, tags="mag")

    def _on_mouse_leave(self, event):
        self.canvas.delete("mag")


class HistogramViewer(ctk.CTkToplevel):
    def __init__(self, master, image, title="Image Histogram"):
        super().__init__(master)
        self.title(f"Histogram - {title}")
        self.geometry("600x450")
        self.configure(fg_color=BG_DARK)
        
        self.image = image
        self._build_plot()
        
    def _build_plot(self):
        fig = Figure(figsize=(6, 4), facecolor='#16213e')
        ax = fig.add_subplot(111)
        
        ax.set_facecolor('#1a1a2e')
        ax.tick_params(colors='#e8eaed')
        ax.xaxis.label.set_color('#e8eaed')
        ax.yaxis.label.set_color('#e8eaed')
        ax.title.set_color('#00d4ff')
        ax.spines['bottom'].set_color('#5f6368')
        ax.spines['top'].set_color('none') 
        ax.spines['right'].set_color('none')
        ax.spines['left'].set_color('#5f6368')
        
        if len(self.image.shape) == 2:
            # Grayscale
            ax.hist(self.image.ravel(), 256, [0, 256], color='#00e676', alpha=0.8)
            ax.set_title("Grayscale Histogram")
        else:
            # Color
            colors = ('b', 'g', 'r')
            for i, col in enumerate(colors):
                hist = cv2.calcHist([self.image], [i], None, [256], [0, 256])
                ax.plot(hist, color=col)
                ax.fill_between(range(256), hist.flatten(), color=col, alpha=0.3)
            ax.set_title("Color Histogram")
            
        ax.set_xlim([0, 256])
        ax.set_xlabel("Pixel Value (Intensity)")
        ax.set_ylabel("Frequency")
        
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        btn_close = ctk.CTkButton(self, text="Close", fg_color="#ff5252", hover_color="#d32f2f", command=self.destroy)
        btn_close.pack(pady=(0, 10))


class LogPanel(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, font=FONT_MONO, fg_color=BG_INPUT, text_color=ACCENT_GREEN, **kwargs)
        self.configure(state="disabled")
        
    def log(self, message):
        self.configure(state="normal")
        self.insert("end", f"> {message}\n")
        self.see("end")
        self.configure(state="disabled")
