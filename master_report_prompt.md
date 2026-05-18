# Master Prompt — University Semester Project Report Generator

> **How to use:** Copy everything below the line, paste it in a new conversation, and replace the `[PLACEHOLDER]` fields with your new project's info.

---

## THE PROMPT (Copy from here)

```
Create a highly professional, visually stunning, university-level semester project report in Microsoft Word (.docx) format using Python (python-docx library). The report must look completely human-written, natural, polished, and premium — not AI-generated.

═══════════════════════════════════════════════════
PROJECT DETAILS (CHANGE THESE FOR EACH PROJECT)
═══════════════════════════════════════════════════

- Project Title: [YOUR PROJECT TITLE]
- Project Subtitle: [ONE LINE DESCRIPTION]
- University: Air University, Multan Campus
- Department: Department of Computer Science
- Course Name: [COURSE NAME]
- Section: BSCS-F-23-A
- Submitted To: [TEACHER NAME]
- Team Members: Muhammad Maauz Mansoor (233599), Zain Riaz, Zahid Zafar
- Semester: 6th Semester — Spring 2026
- Submission Date: May 2026
- GitHub URL: [REPO URL]
- Live URL: [DEPLOYED URL IF ANY]
- Screenshots folder: pic/ (contains numbered screenshots 1.PNG through 8.PNG with sub-images)

═══════════════════════════════════════════════════
DOCUMENT FORMATTING (DO NOT CHANGE)
═══════════════════════════════════════════════════

1. THEME: Modern White and Blue professional theme throughout
2. FONTS: Times New Roman for body text (12pt), Calibri for headings
3. HEADINGS: Blue colored (#1A5CB5), Bold, properly sized hierarchy (H1=16pt, H2=14pt, H3=12pt)
4. BODY TEXT: Justified alignment, 1.5 line spacing, 6pt space after paragraphs
5. MARGINS: Top/Bottom 2.54cm, Left 3.18cm, Right 2.54cm
6. PAGE BORDERS: Blue single-line border (#1A5CB5) on every page
7. HEADER: Project title in italic blue Calibri 9pt, centered on every page
8. FOOTER: Auto page numbers centered on every page
9. TABLE OF CONTENTS: Auto-generated field (user updates in Word with right-click > Update Field)

═══════════════════════════════════════════════════
COVER PAGE DESIGN (DO NOT CHANGE)
═══════════════════════════════════════════════════

1. AI-generated project logo/graphic at the top center (use generate_image tool, 2.5 inches wide)
2. Blue decorative line separator (━ × 50, blue colored)
3. University name: "AIR UNIVERSITY" in 24pt bold dark blue
4. "MULTAN CAMPUS" in 16pt bold blue
5. "Department of Computer Science" in 13pt gray
6. Another blue decorative line separator
7. "SEMESTER PROJECT REPORT" in 13pt bold blue
8. Project title in HUGE 42pt bold blue Calibri
9. Project subtitle in 16pt bold dark blue
10. One-line description in 11pt gray
11. Info table with 6 rows (Course, Section, Submitted To, Submitted By, Semester, Date)
    - Alternating row shading (light blue #E8F0FE on even rows)
    - Left column: Bold blue Calibri labels
    - Right column: Regular Times New Roman values
12. Bottom blue decorative line

═══════════════════════════════════════════════════
TABLE DESIGN (DO NOT CHANGE)
═══════════════════════════════════════════════════

All tables must use this exact styling:
- Header row: White text on solid blue (#1A5CB5) background, bold Calibri 10pt
- Data rows: Alternating white and light blue (#E8F0FE) shading
- Text: Times New Roman 10pt, center aligned
- Table Grid style with center alignment
- Always add one empty paragraph after each table

═══════════════════════════════════════════════════
SPECIAL ELEMENTS TO USE THROUGHOUT (DO NOT CHANGE)
═══════════════════════════════════════════════════

1. INFO BOXES: Blue-shaded (#E8F0FE) single-cell table callouts with:
   - Title: "ℹ [Title]" in bold dark blue Calibri 11pt
   - Body: Regular Times New Roman 10pt
   - Use for key insights, important notes, and highlights

2. CODE BLOCKS: Light gray (#F0F4F8) shaded single-cell tables with:
   - Optional caption in bold blue Calibri 10pt above
   - Code in Consolas 8pt dark blue
   - Use for showing key code snippets from the project

3. SECTION DIVIDERS: Blue decorative lines (━ × 50) in light blue 10pt, centered
   - Use between major transitions

4. IMAGE CAPTIONS: Centered, italic, gray (#555555), Times New Roman 10pt
   - Format: "Figure X.Y: Description"
   - Always add one empty paragraph after each image+caption

═══════════════════════════════════════════════════
DIAGRAMS TO GENERATE (USE generate_image TOOL)
═══════════════════════════════════════════════════

Generate ALL of the following diagrams using the AI image generation tool.
Every diagram prompt must include: "clean academic style, white background with blue accents, professional university-level diagram"

1.  System Architecture Diagram — showing all layers/components of the system
2.  Use Case Diagram — UML style with actor and system boundary
3.  Data Flow Diagram (Level 0 / Context) — external entities, central process, data flows
4.  System Flowchart — step-by-step process flow with decision diamonds
5.  Activity Diagram — UML swimlane style showing user and system activities
6.  Sequence Diagram — temporal message exchanges between components
7.  Class Diagram — UML classes with attributes, methods, relationships
8.  Entity Relationship Diagram — database entities with relationships and cardinality
9.  ML/Data Pipeline Infographic — horizontal stage-by-stage flow with icons
10. Ensemble/Core Mechanism Diagram — showing how the main algorithm/logic works
11. Neural Network / Model Architecture — layer-by-layer visualization
12. Module Interaction Diagram — how Python files/modules communicate
13. UI Navigation Workflow — screen flow from landing page through all features
14. Key Process Visualization — (e.g., SMOTE, preprocessing, or main algorithm visual)
15. Deployment Architecture — infrastructure topology (dev → GitHub → cloud → user)
16. Concept Map — mind-map style showing all project concepts and relationships

Also generate with matplotlib (for precise numbers):
17. ROC Curve Comparison — all models on one chart with AUC values
18. Model/Results Comparison Bar Chart — grouped bars for all metrics
19. Class/Data Distribution Chart — before/after preprocessing comparison
20. Feature Importance / SHAP Chart — horizontal bar chart with values
21. Project Timeline / Gantt Chart — phases with durations as horizontal bars

═══════════════════════════════════════════════════
REPORT CHAPTERS & CONTENT STRUCTURE
═══════════════════════════════════════════════════

Write the following chapters with DETAILED, natural, human-sounding content.
Use simple clear English. Avoid robotic or repetitive phrasing.

CHAPTER 1: INTRODUCTION
- 1.1 Background and Motivation (2-3 detailed paragraphs with industry context)
- Embed: Concept Map diagram
- 1.2 Problem Statement (bullet list of 4-5 specific technical challenges)
- 1.3 Project Objectives (professional table with ID, Description, Category columns)
- 1.4 Scope of the Project (2 paragraphs + Dataset/Input Overview table)
- 1.5 Proposed Solution Overview (2 paragraphs explaining the approach)

CHAPTER 2: TECHNOLOGIES AND TOOLS
- 2.1 Core Technologies (table with Technology, Version, Purpose, Category)
- 2.2 Development Tools (table with Tool, Purpose, Role in Project)

CHAPTER 3: REQUIREMENTS SPECIFICATION  
- 3.1 Functional Requirements (table with ID, Description, Priority, Status columns — 12-15 rows)
- 3.2 Non-Functional Requirements (table with ID, Description, Category, Target — 6-8 rows)

CHAPTER 4: SYSTEM DESIGN
- One subsection per diagram (4.1 through 4.15+)
- Each subsection: heading, 1 descriptive paragraph, embedded diagram image with caption
- Embed ALL 16 AI-generated diagrams here

CHAPTER 5: IMPLEMENTATION
- 5.1 Data Preprocessing (paragraphs + code snippet + data distribution chart + info box)
- 5.2 Model Training — ML (descriptions of each model)
- 5.3 Model Training — DL (descriptions + code snippet for architecture + hyperparameter table)
- 5.4 Core Algorithm/Mechanism (paragraphs explaining the main logic)
- 5.5 Dashboard/Frontend Development (bullet list of all modules/features)
- 5.6 Special Features (e.g., XAI, reporting, etc. + feature importance chart)
- 5.7 Deployment (paragraph + deployment architecture diagram)

CHAPTER 6: TESTING
- 6.1 Testing Methodology
- 6.2 Model/System Performance (results table with all metrics)
- 6.3 Key Observations (analysis paragraphs + ROC curve chart + model comparison chart + info box highlighting best result)
- 6.4 Functional Testing (table with TestCase ID, Description, Result — 10 rows, all PASS)

CHAPTER 7: RESULTS & OUTPUT SCREENSHOTS
- Insert ALL screenshots from pic/ folder
- Each screenshot: embedded image (5.5 inches wide) + caption below
- Organize by feature/module

CHAPTER 8: CONCLUSION (3-4 strong paragraphs summarizing achievements)

CHAPTER 9: FUTURE ENHANCEMENTS (6 bullet points)
- 9.1 Risk Analysis (table with Risk ID, Description, Impact, Mitigation — 5 rows)

CHAPTER 10: REFERENCES (10 academic/technical references in IEEE format)

APPENDIX
- A. Project Repository (GitHub URL)
- B. Live Application (Deployed URL)
- C. Project Directory Structure (code block with tree)
- D. Project Timeline (Gantt chart)

═══════════════════════════════════════════════════
WRITING STYLE RULES (DO NOT CHANGE)
═══════════════════════════════════════════════════

- Write like a polished university student, NOT like an AI
- Use simple, clear English words
- Avoid repetitive phrases like "In conclusion", "Furthermore", "Moreover"
- Every paragraph should add new information
- Be specific with numbers, versions, and technical details
- Maintain logical flow between sections
- Keep paragraphs 3-5 sentences long
- The Acknowledgement must mention the specific teacher name and university

═══════════════════════════════════════════════════
IMPLEMENTATION APPROACH
═══════════════════════════════════════════════════

Build the report using a modular Python approach:
1. report_styles.py — All formatting helpers (setup_document, add_blue_heading, add_para, add_centered_para, add_blue_table, add_image_with_caption, add_page_break, add_toc, add_page_border, add_header_footer, add_section_divider, add_info_box, add_code_block)
2. report_charts.py — matplotlib charts (ROC curves, comparison bars, distribution, feature importance, timeline)
3. report_part1.py — Cover page, front matter, introduction, technologies, requirements, system design
4. report_part2.py — Implementation, testing, results, conclusion, references, appendix
5. generate_report.py — Master script that calls everything in order

Generate ALL diagrams FIRST using generate_image tool, copy them to report_diagrams_v2/ folder, then build the document.

The final output must be a single .docx file that is submission-ready without any further editing needed.
```

---

> [!TIP]
> **Usage:** Just replace the `[PLACEHOLDER]` fields in the "PROJECT DETAILS" section at the top. Everything else stays exactly the same. The AI will replicate the identical premium formatting, diagram set, and document structure for any project.
