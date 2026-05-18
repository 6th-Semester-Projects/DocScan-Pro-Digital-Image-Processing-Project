"""
Document Scanner & OCR Pre-processor - Professional GUI Application
Air University Multan Campus | CS 345 | Spring 2026
"""
import os
import sys
import threading
import time
import cv2
import customtkinter as ctk
from tkinter import filedialog

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.theme import *
from gui.components import SplashScreen, MetricCard, SectionHeader, ImageDisplay, LogPanel, HistogramViewer
from gui.batch_processor import BatchProcessorView
from gui.morphology_lab import MorphologyLabView

# DIP Modules
from modules.deskew_corrector import DeskewCorrector
from modules.frequency_filter import FrequencyFilter
from modules.binarization_engine import BinarizationEngine
from modules.layout_analyzer import LayoutAnalyzer
from modules.output_formatter import OutputFormatter
from modules.metrics import MetricsCalculator
from modules.noise_simulator import NoiseSimulator
from utils.histogram_utils import histogram_equalization, clahe_enhancement
from utils.edge_utils import canny_edges, sobel_edges, laplacian_edges

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DocScanProApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.withdraw() # Hide main window until splash finishes
        splash = SplashScreen(self)
        
        self.title("DocScan Pro - High-Performance Document Scanner & OCR Pre-processor")
        self.geometry("1440x900")
        self.minsize(1200, 768)
        self.configure(fg_color=BG_DARK)
        
        # State
        self.original_img = None
        self.images = {}
        self.metrics_data = {}
        self.pipeline_ran = False
        
        # Simulate loading process for splash
        splash.update_progress(0.3, "Loading core modules...")
        splash.update_progress(0.6, "Initializing DIP engines...")
        
        self._build_ui()
        
        splash.update_progress(0.9, "Building UI components...")
        splash.update_progress(1.0, "Ready.")
        
        self.deiconify() # Show main window FIRST to prevent mainloop exit
        self.update()
        splash.destroy() # Then destroy splash
        
        self.log_panel.log("Application initialized. Ready.")
        
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # --- TOP HEADER ---
        header = ctk.CTkFrame(self, fg_color=BG_MEDIUM, corner_radius=0, height=70)
        header.grid(row=0, column=0, sticky="new")
        header.pack_propagate(False)
        
        title_lbl = ctk.CTkLabel(header, text="DocScan Pro", font=FONT_TITLE, text_color=ACCENT_PRIMARY)
        title_lbl.pack(side="left", padx=25, pady=15)
        
        subtitle_lbl = ctk.CTkLabel(header, text="Semester Project: Digital Image Processing | Air University Multan", 
                                    font=FONT_BODY, text_color=TEXT_SECONDARY)
        subtitle_lbl.pack(side="left", padx=10, pady=20)
        
        # --- MAIN TABVIEW ---
        self.tabview = ctk.CTkTabview(self, fg_color=BG_DARK, segmented_button_fg_color=BG_MEDIUM, 
                                      segmented_button_selected_color=ACCENT_PRIMARY)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.tab_main = self.tabview.add("Main Processing")
        self.tab_batch = self.tabview.add("Batch Mode")
        self.tab_morph = self.tabview.add("Morphology Lab")
        
        self._build_main_tab(self.tab_main)
        
        # Add external views
        self.batch_view = BatchProcessorView(self.tab_batch, log_callback=self.log_panel.log)
        self.batch_view.pack(expand=True, fill="both")
        
        self.morph_view = MorphologyLabView(self.tab_morph, get_image_cb=self.images.get, log_cb=self.log_panel.log)
        self.morph_view.pack(expand=True, fill="both")
        
    def _build_main_tab(self, parent):
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # --- LEFT SIDEBAR (Controls) ---
        sidebar = ctk.CTkScrollableFrame(parent, width=320, fg_color=BG_MEDIUM, corner_radius=12)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        # 1. Input Section
        SectionHeader(sidebar, "1. IMAGE INPUT").pack(fill="x")
        
        btn_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=5)
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        
        btn_load = ctk.CTkButton(btn_frame, text="Load Image", font=FONT_SUBHEADING, height=40,
                                 fg_color="#1565c0", hover_color="#0d47a1", command=self.load_image)
        btn_load.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        btn_sample = ctk.CTkButton(btn_frame, text="Test Sample", font=FONT_SUBHEADING, height=40,
                                   fg_color="#455a64", hover_color="#263238", command=self.load_sample)
        btn_sample.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        # 2. Pipeline Controls
        SectionHeader(sidebar, "2. PIPELINE SETTINGS").pack(fill="x")
        
        # Frequency Filter
        ctk.CTkLabel(sidebar, text="Frequency Filter:", font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", padx=15)
        self.var_filter = ctk.StringVar(value="butterworth")
        opt_filter = ctk.CTkSegmentedButton(sidebar, values=["butterworth", "gaussian"], variable=self.var_filter, 
                                            selected_color=ACCENT_PURPLE, selected_hover_color="#9c27b0")
        opt_filter.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(sidebar, text="LPF Cutoff Frequency:", font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", padx=15, pady=(5,0))
        self.slider_cutoff = ctk.CTkSlider(sidebar, from_=10, to=150, number_of_steps=140, button_color=ACCENT_PURPLE)
        self.slider_cutoff.set(60)
        self.slider_cutoff.pack(fill="x", padx=15, pady=5)
        
        # Binarization
        ctk.CTkLabel(sidebar, text="Binarization Method:", font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", padx=15, pady=(10,0))
        self.var_bin = ctk.StringVar(value="sauvola")
        opt_bin = ctk.CTkSegmentedButton(sidebar, values=["sauvola", "otsu"], variable=self.var_bin,
                                         selected_color=ACCENT_GREEN, selected_hover_color="#388e3c")
        opt_bin.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(sidebar, text="Sauvola Window Size:", font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", padx=15, pady=(5,0))
        self.slider_w = ctk.CTkSlider(sidebar, from_=5, to=61, number_of_steps=28, button_color=ACCENT_GREEN)
        self.slider_w.set(25)
        self.slider_w.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(sidebar, text="Sauvola K Value:", font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(anchor="w", padx=15, pady=(5,0))
        self.slider_k = ctk.CTkSlider(sidebar, from_=0.05, to=0.5, number_of_steps=45, button_color=ACCENT_GREEN)
        self.slider_k.set(0.2)
        self.slider_k.pack(fill="x", padx=15, pady=5)
        
        # Run Button
        self.btn_run = ctk.CTkButton(sidebar, text="► RUN FULL PIPELINE", font=("Segoe UI", 14, "bold"), 
                                     height=50, fg_color="#00695c", hover_color="#004d40", command=self.run_pipeline)
        self.btn_run.pack(fill="x", padx=15, pady=25)
        
        # 3. Utilities
        SectionHeader(sidebar, "3. NOISE & EDGE UTILS").pack(fill="x")
        
        util_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        util_frame.pack(fill="x", padx=15, pady=5)
        util_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.var_noise = ctk.StringVar(value="gaussian")
        combo_noise = ctk.CTkComboBox(util_frame, values=["gaussian", "salt_pepper", "uniform", "poisson", "rayleigh"], 
                                      variable=self.var_noise)
        combo_noise.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        btn_noise = ctk.CTkButton(util_frame, text="Add Noise", fg_color="#e65100", hover_color="#bf360c", 
                                  command=self.apply_noise)
        btn_noise.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        self.var_edge = ctk.StringVar(value="canny")
        combo_edge = ctk.CTkComboBox(util_frame, values=["canny", "sobel", "laplacian"], variable=self.var_edge)
        combo_edge.grid(row=1, column=0, padx=(0, 5), pady=10, sticky="ew")
        
        btn_edge = ctk.CTkButton(util_frame, text="Detect Edges", fg_color="#6a1b9a", hover_color="#4a148c", 
                                 command=self.apply_edge)
        btn_edge.grid(row=1, column=1, padx=(5, 0), pady=10, sticky="ew")
        
        # 4. Export
        SectionHeader(sidebar, "4. EXPORT RESULTS").pack(fill="x")
        ctk.CTkButton(sidebar, text="Generate Text Report", height=40, fg_color="#b71c1c", hover_color="#7f0000", 
                      command=self.export_report).pack(fill="x", padx=15, pady=(5, 20))
        
        # --- CENTER PANEL (Image & Navigation) ---
        center = ctk.CTkFrame(parent, fg_color=BG_DARK, corner_radius=0)
        center.grid(row=0, column=1, sticky="nsew", padx=5, pady=0)
        center.grid_rowconfigure(1, weight=1)
        center.grid_columnconfigure(0, weight=1)
        
        # Stage Navigation
        nav_frame = ctk.CTkScrollableFrame(center, fg_color=BG_MEDIUM, height=75, corner_radius=10, orientation="horizontal")
        nav_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        self.stage_btns = {}
        for name, color in STAGE_COLORS.items():
            btn = ctk.CTkButton(nav_frame, text=name, font=FONT_SUBHEADING, height=36, width=100,
                                fg_color=BG_CARD, hover_color=color, text_color=TEXT_PRIMARY,
                                command=lambda n=name: self.show_stage(n))
            btn.pack(side="left", padx=8, pady=12)
            self.stage_btns[name] = btn
            
        # Extras nav
        self.btn_noise_stage = ctk.CTkButton(nav_frame, text="Noise Demo", font=FONT_SUBHEADING, height=36, width=100,
                                             fg_color=BG_CARD, hover_color="#ff7043", text_color=TEXT_PRIMARY,
                                             command=lambda: self.show_stage("Noise Demo"))
        self.btn_noise_stage.pack(side="left", padx=8, pady=12)
        self.btn_edge_stage = ctk.CTkButton(nav_frame, text="Edge Detection", font=FONT_SUBHEADING, height=36, width=100,
                                             fg_color=BG_CARD, hover_color="#26c6da", text_color=TEXT_PRIMARY,
                                             command=lambda: self.show_stage("Edges"))
        self.btn_edge_stage.pack(side="left", padx=8, pady=12)
        
        # Interaction tools
        tool_frame = ctk.CTkFrame(center, fg_color=BG_DARK, height=40)
        tool_frame.grid(row=2, column=0, sticky="ew", pady=(5, 0))
        
        ctk.CTkLabel(tool_frame, text="View Mode:", font=FONT_SUBHEADING, text_color=TEXT_PRIMARY).pack(side="left", padx=10)
        self.var_mode = ctk.StringVar(value="Normal")
        ctk.CTkSegmentedButton(tool_frame, values=["Normal", "Magnifier", "Compare Before/After"], 
                               variable=self.var_mode, command=self._change_view_mode).pack(side="left")
        
        # New Feature Buttons
        btn_hist = ctk.CTkButton(tool_frame, text="View Histogram", font=FONT_SUBHEADING, height=30, width=120,
                                 fg_color="#00695c", hover_color="#004d40", command=self.show_histogram)
        btn_hist.pack(side="right", padx=10)
        
        btn_reset = ctk.CTkButton(tool_frame, text="Reset App", font=FONT_SUBHEADING, height=30, width=100,
                                  fg_color="#b71c1c", hover_color="#7f0000", command=self.reset_app)
        btn_reset.pack(side="right", padx=10)
        
        # Image Display Canvas
        self.img_display = ImageDisplay(center)
        self.img_display.grid(row=1, column=0, sticky="nsew")
        
        # --- RIGHT PANEL (Metrics & Info) ---
        right_panel = ctk.CTkFrame(parent, width=300, fg_color=BG_MEDIUM, corner_radius=12)
        right_panel.grid(row=0, column=2, sticky="nsew", padx=(10, 0), pady=0)
        right_panel.grid_rowconfigure(4, weight=1)
        
        # Metrics
        SectionHeader(right_panel, "QUALITY METRICS").pack(fill="x")
        self.card_psnr = MetricCard(right_panel, "PSNR", "dB", ACCENT_GREEN)
        self.card_psnr.pack(fill="x", padx=15, pady=5)
        self.card_mse = MetricCard(right_panel, "MSE", "", ACCENT_ORANGE)
        self.card_mse.pack(fill="x", padx=15, pady=5)
        self.card_ssim = MetricCard(right_panel, "SSIM", "", ACCENT_PURPLE)
        self.card_ssim.pack(fill="x", padx=15, pady=5)
        
        # Info
        SectionHeader(right_panel, "IMAGE INFO").pack(fill="x")
        self.info_text = ctk.CTkTextbox(right_panel, font=FONT_MONO, fg_color=BG_CARD, text_color=TEXT_SECONDARY, height=120)
        self.info_text.pack(fill="x", padx=15, pady=5)
        self.info_text.insert("1.0", "No image loaded.")
        self.info_text.configure(state="disabled")
        
        # Log
        SectionHeader(right_panel, "SYSTEM LOG").pack(fill="x")
        self.log_panel = LogPanel(right_panel)
        self.log_panel.pack(fill="both", expand=True, padx=15, pady=(5, 15))

    # ================= LOGIC =================
    
    def _change_view_mode(self, mode):
        if mode == "Normal":
            self.img_display.set_mode("normal")
        elif mode == "Magnifier":
            self.img_display.set_mode("magnifier")
        elif mode == "Compare Before/After":
            if self.original_img is not None and hasattr(self, 'current_stage') and self.current_stage in self.images:
                self.img_display.set_compare(self.original_img, self.images[self.current_stage])
            else:
                self.var_mode.set("Normal")
                self.log_panel.log("Load and process an image to use Compare mode.")

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self._process_load(path)
            
    def load_sample(self):
        sample_path = os.path.join(os.path.dirname(__file__), "input_images", "test_document.jpg")
        if os.path.exists(sample_path):
            self._process_load(sample_path)
        else:
            self.log_panel.log("Sample image not found in input_images/ folder.")
            
    def _process_load(self, path):
        try:
            self.original_img = cv2.imread(path, cv2.IMREAD_COLOR)
            if self.original_img is None:
                raise ValueError("Could not read image file.")
                
            self.images.clear()
            self.images["Original"] = self.original_img.copy()
            self.metrics_data = {}
            self.pipeline_ran = False
            self.current_stage = "Original"
            self.var_mode.set("Normal")
            
            # Reset UI
            for btn in self.stage_btns.values():
                btn.configure(fg_color=BG_CARD)
            self.stage_btns["Original"].configure(fg_color=STAGE_COLORS["Original"])
            
            self.img_display.update_image(self.original_img)
            self._update_info(path)
            self.log_panel.log(f"Successfully loaded {os.path.basename(path)}")
            
            # Reset metrics
            self.card_psnr.set_value("--")
            self.card_mse.set_value("--")
            self.card_ssim.set_value("--")
            
        except Exception as e:
            self.log_panel.log(f"Error loading image: {str(e)}")

    def _update_info(self, path):
        h, w = self.original_img.shape[:2]
        ch = self.original_img.shape[2] if len(self.original_img.shape) == 3 else 1
        size_kb = os.path.getsize(path) / 1024
        
        info = f"File: {os.path.basename(path)}\n"
        info += f"Resolution: {w} x {h}\n"
        info += f"Channels: {ch}\n"
        info += f"Size: {size_kb:.1f} KB\n"
        info += f"Data Type: {self.original_img.dtype}"
        
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", "end")
        self.info_text.insert("1.0", info)
        self.info_text.configure(state="disabled")

    def show_stage(self, stage_name):
        if stage_name in self.images:
            self.current_stage = stage_name
            
            # Highlight button
            for name, btn in self.stage_btns.items():
                btn.configure(fg_color=STAGE_COLORS[name] if name == stage_name else BG_CARD)
                
            self.btn_noise_stage.configure(fg_color="#ff7043" if stage_name=="Noise Demo" else BG_CARD)
            self.btn_edge_stage.configure(fg_color="#26c6da" if stage_name=="Edges" else BG_CARD)
            
            if self.var_mode.get() == "Compare Before/After":
                self.img_display.set_compare(self.original_img, self.images[stage_name])
            else:
                self.img_display.update_image(self.images[stage_name])
                
            self.log_panel.log(f"Viewing stage: {stage_name}")
            
            # Update metrics if available
            if stage_name in self.metrics_data:
                m = self.metrics_data[stage_name]
                self.card_psnr.set_value(f"{m['PSNR']:.2f}")
                self.card_mse.set_value(f"{m['MSE']:.1f}")
                self.card_ssim.set_value(f"{m['SSIM']:.4f}")
            else:
                self.card_psnr.set_value("--")
                self.card_mse.set_value("--")
                self.card_ssim.set_value("--")
        else:
            self.log_panel.log(f"Stage '{stage_name}' not available. Run the pipeline first.")

    def run_pipeline(self):
        if self.original_img is None:
            self.log_panel.log("Error: Load an image before running the pipeline.")
            return
            
        self.btn_run.configure(state="disabled", text="PROCESSING...")
        self.log_panel.log("Starting Document Processing Pipeline...")
        
        # Run in thread to prevent UI freezing
        threading.Thread(target=self._pipeline_thread_worker, daemon=True).start()

    def _pipeline_thread_worker(self):
        try:
            img = self.original_img.copy()
            mc = MetricsCalculator()
            orig_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape)==3 else img.copy()

            # 1. Deskew
            self.after(0, lambda: self.log_panel.log("[1/5] Geometric Correction..."))
            dc = DeskewCorrector(max_skew_angle=15)
            corrected, _ = dc.process(img)
            self.images["Corrected"] = corrected
            
            # 2. FFT Filter
            f_type = self.var_filter.get()
            cutoff = int(self.slider_cutoff.get())
            self.after(0, lambda: self.log_panel.log(f"[2/5] Frequency Filter ({f_type}, D0={cutoff})..."))
            
            ff = FrequencyFilter(filter_type=f_type, cutoff=cutoff)
            filtered, _ = ff.process(corrected)
            self.images["FFT Filtered"] = filtered
            
            corr_gray = cv2.cvtColor(corrected, cv2.COLOR_BGR2GRAY) if len(corrected.shape)==3 else corrected
            m_fft = mc.compute_all(corr_gray, filtered)
            self.metrics_data["FFT Filtered"] = m_fft
            
            # 3. Enhancement
            self.after(0, lambda: self.log_panel.log("[3/5] Contrast Enhancement (CLAHE)..."))
            enhanced = clahe_enhancement(filtered, clip_limit=2.0, tile_size=(8,8))
            self.images["Enhanced"] = enhanced
            
            m_enh = mc.compute_all(corr_gray, enhanced)
            self.metrics_data["Enhanced"] = m_enh
            
            # 4. Binarization
            b_method = self.var_bin.get()
            w = int(self.slider_w.get())
            if w % 2 == 0: w += 1
            k = self.slider_k.get()
            
            self.after(0, lambda: self.log_panel.log(f"[4/5] Binarization ({b_method}, w={w}, k={k:.2f})..."))
            be = BinarizationEngine(method=b_method, window_size=w, k=k)
            binarized, _ = be.process(enhanced, method=b_method)
            self.images["Binarized"] = binarized
            
            m_bin = mc.compute_all(corr_gray, binarized)
            self.metrics_data["Binarized"] = m_bin
            
            # 5. Layout Analysis
            self.after(0, lambda: self.log_panel.log("[5/5] Layout Analysis (Text/Image blocks)..."))
            la = LayoutAnalyzer()
            layout_vis, _ = la.process(binarized, corrected)
            self.images["Layout"] = layout_vis
            
            # Done
            self.pipeline_ran = True
            self.after(0, self._pipeline_complete)
            
        except Exception as e:
            self.after(0, lambda err=e: self._pipeline_error(err))

    def _pipeline_complete(self):
        self.btn_run.configure(state="normal", text="► RUN FULL PIPELINE")
        self.log_panel.log("Pipeline executed successfully!")
        self.show_stage("Layout")
        
    def _pipeline_error(self, err):
        self.btn_run.configure(state="normal", text="► RUN FULL PIPELINE")
        self.log_panel.log(f"PIPELINE ERROR: {str(err)}")

    def apply_noise(self):
        if self.original_img is None:
            self.log_panel.log("Load an image first.")
            return
            
        noise_type = self.var_noise.get()
        self.log_panel.log(f"Simulating {noise_type} noise...")
        
        noisy_img = NoiseSimulator.apply_noise(self.original_img, noise_type)
        self.images["Noise Demo"] = noisy_img
        
        # Calculate metrics against original
        mc = MetricsCalculator()
        orig_g = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY) if len(self.original_img.shape)==3 else self.original_img
        noise_g = cv2.cvtColor(noisy_img, cv2.COLOR_BGR2GRAY) if len(noisy_img.shape)==3 else noisy_img
        m = mc.compute_all(orig_g, noise_g)
        self.metrics_data["Noise Demo"] = m
        
        self.show_stage("Noise Demo")
        
    def apply_edge(self):
        src = self.images.get("Corrected", self.original_img)
        if src is None:
            self.log_panel.log("Load an image first.")
            return
            
        edge_type = self.var_edge.get()
        self.log_panel.log(f"Applying {edge_type} edge detection...")
        
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if len(src.shape)==3 else src
        
        if edge_type == "canny":
            res = canny_edges(gray)
        elif edge_type == "sobel":
            res = sobel_edges(gray)
        elif edge_type == "laplacian":
            res = laplacian_edges(gray)
            
        self.images["Edges"] = res
        self.show_stage("Edges")

    def export_report(self):
        if not self.pipeline_ran:
            self.log_panel.log("Please run the pipeline before generating a report.")
            return
            
        d = filedialog.askdirectory()
        if d:
            of = OutputFormatter(output_dir=d)
            of.save_pipeline_results({k: v for k, v in self.images.items() if k in STAGE_COLORS})
            src = self.images.get("Corrected", self.original_img)
            of.create_edge_comparison(src)
            of.create_comparison_figure({k: v for k, v in self.images.items() if k in STAGE_COLORS})
            
            info = {"filename": "document", "filesize_kb": 100} # Mock for formatter
            of.generate_text_report(info, self.metrics_data, list(STAGE_COLORS.keys()))
            
            self.log_panel.log(f"Results and report exported successfully to:\n{d}")

    def show_histogram(self):
        if self.original_img is None:
            self.log_panel.log("Please load an image first to view its histogram.")
            return
            
        stage = getattr(self, 'current_stage', 'Original')
        img_to_show = self.images.get(stage, self.original_img)
        
        self.log_panel.log(f"Generating histogram for stage: {stage}")
        # HistogramViewer is a Toplevel window, it handles its own display
        HistogramViewer(self, img_to_show, title=stage)

    def reset_app(self):
        self.original_img = None
        self.images = {}
        self.metrics_data = {}
        self.pipeline_ran = False
        self.current_stage = "Original"
        self.var_mode.set("Normal")
        
        for btn in self.stage_btns.values():
            btn.configure(fg_color=BG_CARD)
            
        self.btn_noise_stage.configure(fg_color=BG_CARD)
        self.btn_edge_stage.configure(fg_color=BG_CARD)
        
        self.img_display.update_image(None)
        
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", "end")
        self.info_text.insert("1.0", "No image loaded.")
        self.info_text.configure(state="disabled")
        
        self.card_psnr.set_value("--")
        self.card_mse.set_value("--")
        self.card_ssim.set_value("--")
        
        self.log_panel.log("Application state has been reset.")

if __name__ == "__main__":
    app = DocScanProApp()
    app.mainloop()
