import os
from docx import Document
from report_styles import setup_document, add_header_footer, add_toc, add_blue_heading
from report_part1 import build_cover_page, build_chapter_1, build_chapter_2, build_chapter_3, build_chapter_4
from report_part2 import build_chapter_5, build_chapter_6, build_chapter_7, build_chapter_8, build_chapter_9, build_chapter_10, build_appendix

def generate_full_report():
    print("Initializing document...")
    doc = Document()
    
    print("Applying global styles and margins...")
    setup_document(doc)
    add_header_footer(doc, "DocScan Pro - Semester Project: Digital Image Processing")
    
    print("Building Cover Page...")
    build_cover_page(doc)
    
    print("Building Table of Contents...")
    add_blue_heading(doc, 'TABLE OF CONTENTS', level=1)
    doc.add_paragraph("Please right-click here and select 'Update Field' to generate the Table of Contents.")
    add_toc(doc)
    doc.add_page_break()
    
    print("Building Chapter 1: Introduction...")
    build_chapter_1(doc)
    doc.add_page_break()
    
    print("Building Chapter 2: Technologies and Tools...")
    build_chapter_2(doc)
    doc.add_page_break()
    
    print("Building Chapter 3: Requirements Specification...")
    build_chapter_3(doc)
    doc.add_page_break()
    
    print("Building Chapter 4: System Design...")
    build_chapter_4(doc)
    doc.add_page_break()
    
    print("Building Chapter 5: Implementation...")
    build_chapter_5(doc)
    doc.add_page_break()
    
    print("Building Chapter 6: Testing and Analysis...")
    build_chapter_6(doc)
    doc.add_page_break()
    
    print("Building Chapter 7: Results & Output Screenshots...")
    build_chapter_7(doc)
    doc.add_page_break()
    
    print("Building Chapter 8: Conclusion...")
    build_chapter_8(doc)
    doc.add_page_break()
    
    print("Building Chapter 9: Future Enhancements...")
    build_chapter_9(doc)
    doc.add_page_break()
    
    print("Building Chapter 10: References...")
    build_chapter_10(doc)
    
    print("Building Appendix...")
    build_appendix(doc)
    
    # Save document
    output_path = r"e:\4th semester tasks\DIP-LABS\DIP-Project\DocScan_Pro_Semester_Project_Report.docx"
    print(f"Saving document to {output_path}...")
    doc.save(output_path)
    print("Document successfully generated!")

if __name__ == "__main__":
    generate_full_report()
