import cv2
import numpy as np
import customtkinter as ctk
from gui.theme import *
from gui.image_utils import cv2_to_tk, resize_for_display

class MorphologyLabView(ctk.CTkFrame):
    def __init__(self, master, get_image_cb, log_cb, **kwargs):
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self.get_image = get_image_cb
        self.log = log_cb
        self.source_img = None
        self.processed_img = None
        self._build_ui()
        
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        # Left Control Panel
        ctrl = ctk.CTkFrame(self, fg_color=BG_MEDIUM, corner_radius=12)
        ctrl.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        
        ctk.CTkLabel(ctrl, text="Morphology Lab", font=FONT_TITLE, text_color=ACCENT_PRIMARY).pack(pady=(20, 5))
        ctk.CTkLabel(ctrl, text="Test morphological operations", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(pady=(0, 20))
        
        # Controls
        ctk.CTkLabel(ctrl, text="Operation:", font=FONT_SUBHEADING, text_color=TEXT_PRIMARY).pack(anchor="w", padx=20)
        self.var_op = ctk.StringVar(value="Erosion")
        ops = ["Erosion", "Dilation", "Opening", "Closing", "Gradient"]
        self.op_menu = ctk.CTkOptionMenu(ctrl, values=ops, variable=self.var_op, command=self._apply)
        self.op_menu.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(ctrl, text="Kernel Shape:", font=FONT_SUBHEADING, text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(10, 0))
        self.var_shape = ctk.StringVar(value="Rect")
        shapes = ["Rect", "Cross", "Ellipse"]
        self.shape_menu = ctk.CTkOptionMenu(ctrl, values=shapes, variable=self.var_shape, command=self._apply)
        self.shape_menu.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(ctrl, text="Kernel Size:", font=FONT_SUBHEADING, text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(10, 0))
        self.lbl_ks = ctk.CTkLabel(ctrl, text="3 x 3", font=FONT_MONO, text_color=ACCENT_YELLOW)
        self.lbl_ks.pack(anchor="w", padx=20)
        self.sl_ks = ctk.CTkSlider(ctrl, from_=1, to=31, number_of_steps=15, command=self._on_ks_change)
        self.sl_ks.set(3)
        self.sl_ks.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(ctrl, text="Iterations:", font=FONT_SUBHEADING, text_color=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(10, 0))
        self.lbl_it = ctk.CTkLabel(ctrl, text="1", font=FONT_MONO, text_color=ACCENT_YELLOW)
        self.lbl_it.pack(anchor="w", padx=20)
        self.sl_it = ctk.CTkSlider(ctrl, from_=1, to=10, number_of_steps=9, command=self._on_it_change)
        self.sl_it.set(1)
        self.sl_it.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkButton(ctrl, text="Load Binarized Image", fg_color="#1b5e20", hover_color="#2e7d32", command=self._load_source).pack(fill="x", padx=20, pady=(30, 5))
        ctk.CTkButton(ctrl, text="💾 Save Result", fg_color="#1565c0", hover_color="#0d47a1", command=self._save_result).pack(fill="x", padx=20, pady=(5, 20))
        
        # Right Display Panel
        self.disp = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        self.disp.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.disp.pack_propagate(False)
        
        self.lbl_img = ctk.CTkLabel(self.disp, text="Load an image to start.", font=FONT_HEADING, text_color=TEXT_DIM)
        self.lbl_img.pack(expand=True, fill="both")
        
        self.disp.bind("<Configure>", self._on_resize)
        self.tk_img = None
        
    def _on_ks_change(self, val):
        k = int(val)
        if k % 2 == 0: k += 1
        self.sl_ks.set(k)
        self.lbl_ks.configure(text=f"{k} x {k}")
        self._apply()
        
    def _on_it_change(self, val):
        i = int(val)
        self.lbl_it.configure(text=str(i))
        self._apply()
        
    def _load_source(self):
        img = self.get_image("Binarized")
        if img is None:
            img = self.get_image("Original")
            if img is None:
                self.log("Please load and process an image in the Main tab first.")
                return
        
        # Ensure grayscale/binary
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            
        self.source_img = img
        self._apply()
        self.log("Loaded source image into Morphology Lab.")
        
    def _save_result(self):
        if self.processed_img is None:
            self.log("No morphology result to save.")
            return
            
        from tkinter import filedialog
        import os
        path = filedialog.asksaveasfilename(
            defaultextension=".png", 
            initialfile="DocScan_Morphology.png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
        )
        if path:
            cv2.imwrite(path, self.processed_img)
            self.log(f"Saved morphology result to {os.path.basename(path)}")
        
    def _apply(self, *args):
        if self.source_img is None: return
        
        op = self.var_op.get()
        shape_str = self.var_shape.get()
        k_size = int(self.sl_ks.get())
        iters = int(self.sl_it.get())
        
        shape_map = {
            "Rect": cv2.MORPH_RECT,
            "Cross": cv2.MORPH_CROSS,
            "Ellipse": cv2.MORPH_ELLIPSE
        }
        kernel = cv2.getStructuringElement(shape_map[shape_str], (k_size, k_size))
        
        op_map = {
            "Erosion": cv2.erode,
            "Dilation": cv2.dilate,
            "Opening": lambda src, k, i: cv2.morphologyEx(src, cv2.MORPH_OPEN, k, iterations=i),
            "Closing": lambda src, k, i: cv2.morphologyEx(src, cv2.MORPH_CLOSE, k, iterations=i),
            "Gradient": lambda src, k, i: cv2.morphologyEx(src, cv2.MORPH_GRADIENT, k, iterations=i)
        }
        
        try:
            if op in ["Erosion", "Dilation"]:
                self.processed_img = op_map[op](self.source_img, kernel, iterations=iters)
            else:
                self.processed_img = op_map[op](self.source_img, kernel, iters)
                
            self._render()
        except Exception as e:
            self.log(f"Morphology error: {e}")
            
    def _on_resize(self, event):
        if self.processed_img is not None:
            self._render()
            
    def _render(self):
        if self.processed_img is None: return
        w = max(100, self.disp.winfo_width() - 10)
        h = max(100, self.disp.winfo_height() - 10)
        
        resized = resize_for_display(self.processed_img, max_w=w, max_h=h)
        self.tk_img = cv2_to_tk(resized, (w, h))
        self.lbl_img.configure(image=self.tk_img, text="")
