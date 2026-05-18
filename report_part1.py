import os
from docx.shared import Pt, RGBColor
from report_styles import (
    add_blue_heading, add_para, add_blue_table, add_image_with_caption, 
    add_section_divider, add_info_box
)

def build_cover_page(doc):
    # Center alignment for cover
    def _c_para(text, size, bold=False, color=None, font_name='Calibri'):
        p = doc.add_paragraph()
        p.alignment = 1 # center
        r = p.add_run(text)
        r.font.name = font_name
        r.font.size = Pt(size)
        if bold: r.bold = True
        if color: r.font.color.rgb = color
        return p

    # Logo
    logo_path = r"e:\4th semester tasks\DIP-LABS\DIP-Project\report_diagrams_v2\00_logo.png"
    if os.path.exists(logo_path):
        p = doc.add_paragraph()
        p.alignment = 1
        r = p.add_run()
        r.add_picture(logo_path, width=Pt(180))
        
    _c_para("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 10, color=RGBColor(0x1A, 0x5C, 0xB5))
    
    _c_para("AIR UNIVERSITY", 24, bold=True, color=RGBColor(0x0A, 0x2A, 0x66))
    _c_para("MULTAN CAMPUS", 16, bold=True, color=RGBColor(0x1A, 0x5C, 0xB5))
    _c_para("Department of Computer Science", 13, color=RGBColor(0x55, 0x55, 0x55))
    
    _c_para("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 10, color=RGBColor(0x1A, 0x5C, 0xB5))
    
    # Spacing
    doc.add_paragraph()
    
    _c_para("SEMESTER PROJECT REPORT", 13, bold=True, color=RGBColor(0x1A, 0x5C, 0xB5))
    _c_para("DocScan Pro", 42, bold=True, color=RGBColor(0x1A, 0x5C, 0xB5))
    _c_para("High-Performance Document Scanner & OCR Pre-processor", 16, bold=True, color=RGBColor(0x0A, 0x2A, 0x66))
    _c_para("Advanced digital image processing toolkit built on Python and OpenCV", 11, color=RGBColor(0x55, 0x55, 0x55))
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    # Info Table
    headers = ["Project Information", "Details"]
    rows = [
        ["Course", "Digital Image Processing"],
        ["Section", "BSCS-F-23-A"],
        ["Submitted To", "Sir Faisal Idrees"],
        ["Submitted By", "Muhammad Maauz Mansoor (233599)\nZain Riaz\nZahid Zafar"],
        ["Semester", "6th Semester — Spring 2026"],
        ["Date", "May 2026"]
    ]
    add_blue_table(doc, headers, rows, col_widths=[Pt(150), Pt(300)])
    
    doc.add_paragraph()
    _c_para("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 10, color=RGBColor(0x1A, 0x5C, 0xB5))
    doc.add_page_break()

def build_chapter_1(doc):
    add_blue_heading(doc, 'CHAPTER 1: INTRODUCTION', level=1)
    
    add_blue_heading(doc, '1.1 Background and Motivation', level=2)
    add_para(doc, "In the modern digital era, the conversion of physical documents into high-quality digital formats is paramount for efficient archiving, retrieval, and automated text extraction. Traditional scanning processes often introduce geometric distortions, uneven illumination, and high-frequency noise, which significantly degrade the performance of Optical Character Recognition (OCR) systems. To address these challenges, advanced Digital Image Processing (DIP) techniques are required to restore and enhance document images before they are fed into downstream AI engines.")
    add_para(doc, "DocScan Pro was developed to bridge the gap between noisy raw captures and pristine, OCR-ready document formats. By leveraging mathematical morphology, frequency domain filtering, and adaptive spatial binarization, this project provides a robust, desktop-grade software solution tailored for professional document enhancement.")
    
    map_path = r"e:\4th semester tasks\DIP-LABS\DIP-Project\report_diagrams_v2\16_concept_map.png"
    add_image_with_caption(doc, map_path, "Figure 1.1: Core Concept Map of DocScan Pro Processing Pipeline")
    
    add_blue_heading(doc, '1.2 Problem Statement', level=2)
    add_para(doc, "The development of document digitization systems involves overcoming several specific technical challenges:")
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Geometric Distortions: ").bold = True
    p.add_run("Documents captured via mobile devices or flatbed scanners often exhibit perspective skew and rotational misalignment.")
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Uneven Illumination: ").bold = True
    p.add_run("Shadows and gradient lighting cause global thresholding methods to fail, resulting in black patches and loss of textual data.")
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Sensor Noise: ").bold = True
    p.add_run("High-frequency Gaussian and Salt & Pepper noise obscure fine text strokes, reducing readability.")
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Complex Layouts: ").bold = True
    p.add_run("Differentiating between dense text blocks and embedded figures requires sophisticated morphological segmentation.")

    add_blue_heading(doc, '1.3 Project Objectives', level=2)
    headers = ["ID", "Description", "Category"]
    rows = [
        ["OBJ-01", "Implement an automated deskewing algorithm using spatial contours and perspective transforms.", "Geometric Correction"],
        ["OBJ-02", "Design a Butterworth Low Pass Filter in the 2D frequency domain to suppress high-frequency noise.", "Frequency Domain"],
        ["OBJ-03", "Develop an adaptive Sauvola binarization engine to handle uneven illumination dynamically.", "Spatial Enhancement"],
        ["OBJ-04", "Integrate a Layout Analyzer using Connected Component Analysis and Morphological Dilation.", "Segmentation"],
        ["OBJ-05", "Build a high-performance, dark-themed GUI using CustomTkinter for real-time visualization.", "User Interface"]
    ]
    add_blue_table(doc, headers, rows)
    
    add_blue_heading(doc, '1.4 Scope of the Project', level=2)
    add_para(doc, "The scope of DocScan Pro encompasses the complete pre-processing pipeline required to clean and structure document images. It is designed to run locally on desktop environments, utilizing the CPU for intensive matrix operations via NumPy and OpenCV. The application handles standard image formats (JPEG, PNG, BMP) and provides both single-image interactive processing and high-volume batch processing capabilities.")
    add_para(doc, "The system does not inherently perform the final OCR text extraction; rather, it acts as the critical pre-processing layer that guarantees optimal inputs for engines like Tesseract or AWS Textract.")
    
    add_blue_heading(doc, '1.5 Proposed Solution Overview', level=2)
    add_para(doc, "The proposed solution is a 5-stage sequential processing pipeline. First, the Geometric Correction module detects the primary document boundary and rectifies any perspective skew. Second, the Frequency Domain Filter applies a 2D Fast Fourier Transform (FFT) to shift the image into the frequency domain, where a Butterworth Low Pass Filter attenuates noise frequencies before inverse transformation.")
    add_para(doc, "Following noise reduction, Contrast Limited Adaptive Histogram Equalization (CLAHE) is applied to normalize lighting. The image is then passed to the Binarization Engine, which utilizes the Sauvola local thresholding method to separate text from the background. Finally, the Layout Analyzer employs Sobel edge detection and morphological dilation to cluster text into distinct bounding boxes, preparing the document for structural analysis.")
    
    add_section_divider(doc)
    
def build_chapter_2(doc):
    add_blue_heading(doc, 'CHAPTER 2: TECHNOLOGIES AND TOOLS', level=1)
    
    add_blue_heading(doc, '2.1 Core Technologies', level=2)
    headers = ["Technology", "Version", "Purpose", "Category"]
    rows = [
        ["Python", "3.13.0", "Core programming language and execution environment.", "Language"],
        ["OpenCV (cv2)", "4.9+", "Matrix manipulations, filtering, and computer vision algorithms.", "Library"],
        ["NumPy", "1.26+", "High-performance N-dimensional array processing and FFT computations.", "Library"],
        ["CustomTkinter", "5.2.2", "Modern, hardware-accelerated dark theme GUI components.", "Framework"]
    ]
    add_blue_table(doc, headers, rows)
    
    add_blue_heading(doc, '2.2 Development Tools', level=2)
    headers = ["Tool", "Purpose", "Role in Project"]
    rows = [
        ["VS Code", "Integrated Development Environment", "Primary code editor, debugging, and linting."],
        ["Git & GitHub", "Version Control", "Source code management and collaborative tracking."],
        ["Matplotlib", "Data Visualization", "Rendering histograms and real-time metric plotting."],
        ["Pillow (PIL)", "Image Management", "Interfacing between OpenCV arrays and Tkinter canvas rendering."]
    ]
    add_blue_table(doc, headers, rows)
    
    add_section_divider(doc)

def build_chapter_3(doc):
    add_blue_heading(doc, 'CHAPTER 3: REQUIREMENTS SPECIFICATION', level=1)
    
    add_blue_heading(doc, '3.1 Functional Requirements', level=2)
    headers = ["ID", "Description", "Priority", "Status"]
    rows = [
        ["FR-01", "System shall allow users to load single images via file dialog.", "High", "Implemented"],
        ["FR-02", "System shall perform automatic document boundary detection and deskewing.", "High", "Implemented"],
        ["FR-03", "System shall apply a 2D FFT and Butterworth filter for noise reduction.", "High", "Implemented"],
        ["FR-04", "System shall enhance contrast using CLAHE.", "High", "Implemented"],
        ["FR-05", "System shall binarize images using Sauvola adaptive thresholding.", "High", "Implemented"],
        ["FR-06", "System shall allow dynamic tuning of filter cutoffs and thresholding parameters.", "Medium", "Implemented"],
        ["FR-07", "System shall analyze document layout and draw bounding boxes around text.", "High", "Implemented"],
        ["FR-08", "System shall provide a dedicated Morphology Lab for erosion, dilation, and opening.", "Medium", "Implemented"],
        ["FR-09", "System shall provide a Noise Simulator for Gaussian, Rayleigh, and Salt & Pepper noise.", "Low", "Implemented"],
        ["FR-10", "System shall compute real-time quality metrics (PSNR, MSE, SSIM).", "Medium", "Implemented"],
        ["FR-11", "System shall support Batch Processing of multiple images in a selected directory.", "High", "Implemented"],
        ["FR-12", "System shall generate a structured text report containing all computed metrics.", "Low", "Implemented"]
    ]
    add_blue_table(doc, headers, rows)
    
    add_blue_heading(doc, '3.2 Non-Functional Requirements', level=2)
    headers = ["ID", "Description", "Category", "Target"]
    rows = [
        ["NFR-01", "Pipeline execution for a 1080p image should complete under 1.5 seconds.", "Performance", "< 1.5s"],
        ["NFR-02", "GUI must remain responsive during heavy FFT computations using threading.", "Usability", "Zero blocking"],
        ["NFR-03", "Application must utilize a modern dark theme to reduce eye strain.", "Design", "CustomTkinter"],
        ["NFR-04", "System must not exceed 500MB of RAM during single-image processing.", "Resource", "< 500MB"],
        ["NFR-05", "Codebase must follow modular OOP principles for maintainability.", "Architecture", "Modular"],
        ["NFR-06", "Application must be fully cross-platform compatible (Windows, Linux, macOS).", "Portability", "Cross-OS"]
    ]
    add_blue_table(doc, headers, rows)
    
    add_section_divider(doc)

def build_chapter_4(doc):
    add_blue_heading(doc, 'CHAPTER 4: SYSTEM DESIGN', level=1)
    add_para(doc, "The system design phase outlines the architectural patterns, data flow, and object-oriented structure of DocScan Pro. Visual models have been generated to map out the interactions between the UI layer, processing engines, and mathematical algorithms.")
    
    diagrams = [
        ("4.1 System Architecture", "01_sys_arch.png", "The System Architecture diagram illustrates the multi-layered approach, decoupling the CustomTkinter frontend from the intensive OpenCV and NumPy backend processing modules."),
        ("4.2 Use Case Diagram", "02_use_case.png", "The Use Case diagram maps out the primary interactions between the end-user and the system, highlighting features like batch processing, parameter tuning, and metric visualization."),
        ("4.3 Data Flow Diagram (Level 0)", "03_dfd.png", "This context-level DFD shows the flow of raw pixel data through the central DIP pipeline, ultimately resulting in a structured, binarized output alongside quality metrics."),
        ("4.4 System Flowchart", "04_flowchart.png", "The System Flowchart provides a step-by-step procedural view of the image processing pipeline, including decision nodes for skew thresholding and dynamic parameter application."),
        ("4.5 Activity Diagram", "05_activity.png", "The Activity Diagram utilizes UML swimlanes to separate user-initiated UI events from background thread computations, ensuring GUI responsiveness is maintained."),
        ("4.6 Sequence Diagram", "06_sequence.png", "The Sequence Diagram visualizes the temporal exchange of messages between the UI Controller, the PipelineWorker thread, and the underlying mathematical modules during a processing cycle."),
        ("4.7 Class Diagram", "07_class.png", "The Class Diagram outlines the Object-Oriented structure of the Python codebase, defining attributes, methods, and relationships between classes like BinarizationEngine and FrequencyFilter."),
        ("4.8 Entity Relationship Diagram", "08_erd.png", "The ERD models the logical relationship between the document entity, its associated processing configuration parameters, and the resulting evaluation metrics."),
        ("4.9 Data Pipeline Infographic", "09_pipeline.png", "This horizontal infographic presents a high-level, stage-by-stage visual summary of the core image transformations applied to the document."),
        ("4.10 Core Mechanism (Adaptive Binarization)", "10_core_mechanism.png", "This diagram specifically illustrates the sliding window mechanism used by the Sauvola algorithm to calculate local standard deviation and mean for dynamic thresholding."),
        ("4.11 Filter Architecture (Frequency Domain)", "11_filter_architecture.png", "This layer-by-layer visualization breaks down the 2D Fast Fourier Transform process, showing the shifting of zero-frequency components and the application of the Butterworth LPF mask."),
        ("4.12 Module Interaction Diagram", "12_module_interaction.png", "This diagram displays how independent Python files (e.g., gui_app.py, layout_analyzer.py) import and utilize each other's functionalities."),
        ("4.13 UI Navigation Workflow", "13_ui_workflow.png", "The UI Workflow maps the screen navigation from the landing page through the main processing tabs, morphology lab, and batch processing panels."),
        ("4.14 Key Process (Layout Analysis)", "14_key_process.png", "This diagram visualizes the Connected Component Analysis logic, showing how dilated text pixels are clustered into unified bounding boxes representing text paragraphs."),
        ("4.15 Deployment Architecture", "15_deployment.png", "The Deployment topology shows the application's lifecycle from local development scripts to a packaged desktop executable running on the end user's machine.")
    ]
    
    base_dir = r"e:\4th semester tasks\DIP-LABS\DIP-Project\report_diagrams_v2"
    
    for title, filename, desc in diagrams:
        add_blue_heading(doc, title, level=2)
        add_para(doc, desc)
        img_path = os.path.join(base_dir, filename)
        add_image_with_caption(doc, img_path, f"Figure {title[:4]}: {title[4:]}")
    
    add_section_divider(doc)
