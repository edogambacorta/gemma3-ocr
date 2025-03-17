import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "This is a test PDF file.")
    c.drawString(100, 730, "It contains some text for OCR processing.")
    c.drawString(100, 710, "Let's see how well the Gemma-3 OCR app handles it.")
    c.save()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "test.pdf")
    create_pdf(pdf_path)
    print(f"Script directory: {script_dir}")
    print(f"PDF path: {pdf_path}")
    
    if os.path.exists(pdf_path):
        print(f"PDF created successfully. File size: {os.path.getsize(pdf_path)} bytes")
    else:
        print("Failed to create PDF file.")
    
    print("Directory contents:")
    for item in os.listdir(script_dir):
        print(f"- {item}")
