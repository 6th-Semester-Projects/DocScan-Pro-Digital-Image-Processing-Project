import os
import cv2
import glob
import threading
import customtkinter as ctk
from tkinter import filedialog
from gui.theme import *

# DIP Modules
from modules.deskew_corrector import DeskewCorrector
from modules.frequency_filter import FrequencyFilter
from modules.binarization_engine import BinarizationEngine
from modules.layout_analyzer import LayoutAnalyzer
from utils.histogram_utils import histogram_equalization

class BatchProcessorView(ctk.CTkFrame):
    def __init__(self, master, log_callback, **kwargs):
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self.log = log_callback
        self._build_ui()
        
    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color=BG_MEDIUM, corner_radius=12)
        container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(container, text="Batch Processing Mode", font=FONT_TITLE, text_color=ACCENT_PRIMARY).pack(pady=(20, 5))
        ctk.CTkLabel(container, text="Process multiple document images at once.", font=FONT_BODY, text_color=TEXT_SECONDARY).pack(pady=(0, 20))
        
        # Directories
        dir_frame = ctk.CTkFrame(container, fg_color="transparent")
        dir_frame.pack(fill="x", padx=40, pady=10)
        
        self.lbl_input = ctk.CTkLabel(dir_frame, text="Input Directory: Not Selected", font=FONT_MONO, text_color=TEXT_PRIMARY, anchor="w")
        self.lbl_input.pack(fill="x", pady=5)
        
        btn_in = ctk.CTkButton(dir_frame, text="Select Input Folder", fg_color="#1565c0", command=self._sel_in)
        btn_in.pack(anchor="w", pady=(0, 15))
        
        self.lbl_output = ctk.CTkLabel(dir_frame, text="Output Directory: Not Selected", font=FONT_MONO, text_color=TEXT_PRIMARY, anchor="w")
        self.lbl_output.pack(fill="x", pady=5)
        
        btn_out = ctk.CTkButton(dir_frame, text="Select Output Folder", fg_color="#e65100", command=self._sel_out)
        btn_out.pack(anchor="w")
        
        # Options
        opt_frame = ctk.CTkFrame(container, fg_color=BG_CARD, corner_radius=10)
        opt_frame.pack(fill="x", padx=40, pady=20)
        
        ctk.CTkLabel(opt_frame, text="Pipeline Settings", font=FONT_SUBHEADING, text_color=ACCENT_GREEN).pack(pady=10)
        
        self.var_filt = ctk.StringVar(value="butterworth")
        ctk.CTkSegmentedButton(opt_frame, values=["butterworth", "gaussian"], variable=self.var_filt).pack(pady=5)
        
        self.var_bin = ctk.StringVar(value="sauvola")
        ctk.CTkSegmentedButton(opt_frame, values=["sauvola", "otsu"], variable=self.var_bin).pack(pady=5)
        
        # Run
        self.btn_run = ctk.CTkButton(container, text="START BATCH PROCESS", font=("Segoe UI", 14, "bold"), height=50, fg_color="#00695c", command=self._start_batch)
        self.btn_run.pack(pady=20, padx=40, fill="x")
        
        # Progress
        self.lbl_prog = ctk.CTkLabel(container, text="Ready", font=FONT_BODY, text_color=TEXT_SECONDARY)
        self.lbl_prog.pack(pady=(10, 0))
        self.progressbar = ctk.CTkProgressBar(container, width=500, progress_color=ACCENT_GREEN)
        self.progressbar.pack(pady=10)
        self.progressbar.set(0)
        
        self.in_dir = None
        self.out_dir = None
        
    def _sel_in(self):
        d = filedialog.askdirectory()
        if d:
            self.in_dir = d
            self.lbl_input.configure(text=f"Input: {d}")
            
    def _sel_out(self):
        d = filedialog.askdirectory()
        if d:
            self.out_dir = d
            self.lbl_output.configure(text=f"Output: {d}")
            
    def _start_batch(self):
        if not self.in_dir or not self.out_dir:
            self.log("Please select both input and output directories.")
            return
            
        files = glob.glob(os.path.join(self.in_dir, "*.[jp][pn]*"))
        if not files:
            self.log("No valid images found in input directory.")
            return
            
        self.btn_run.configure(state="disabled")
        threading.Thread(target=self._process_files, args=(files,), daemon=True).start()
        
    def _process_files(self, files):
        total = len(files)
        self.log(f"Starting batch process for {total} images...")
        
        f_type = self.var_filt.get()
        b_type = self.var_bin.get()
        
        dc = DeskewCorrector()
        ff = FrequencyFilter(filter_type=f_type)
        be = BinarizationEngine(method=b_type)
        la = LayoutAnalyzer()
        
        for i, path in enumerate(files):
            try:
                self.after(0, self.lbl_prog.configure, {"text": f"Processing {i+1}/{total}: {os.path.basename(path)}"})
                img = cv2.imread(path, cv2.IMREAD_COLOR)
                if img is None: continue
                
                corr, _ = dc.process(img)
                filt, _ = ff.process(corr)
                enh = histogram_equalization(filt)
                bina, _ = be.process(enh)
                lay, _ = la.process(bina, corr)
                
                # Save final
                out_path = os.path.join(self.out_dir, f"proc_{os.path.basename(path)}")
                cv2.imwrite(out_path, lay)
                
            except Exception as e:
                self.log(f"Error processing {os.path.basename(path)}: {e}")
                
            # Update progress
            self.after(0, self.progressbar.set, (i+1)/total)
            
        self.after(0, self._batch_complete)
        
    def _batch_complete(self):
        self.btn_run.configure(state="normal")
        self.lbl_prog.configure(text="Batch processing complete!")
        self.log("Batch processing finished successfully.")
