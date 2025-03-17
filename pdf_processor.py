import PyPDF2
from PIL import Image
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_images_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    images = []
    for page in pdf_reader.pages:
        if '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj].get_data()
                    img = Image.frombytes("RGB", size, data)
                    images.append(img)
    return images

def placeholder_ocr(image):
    # This is a placeholder function for OCR
    return "Image OCR is currently disabled for troubleshooting."

def process_pdf(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    images = extract_images_from_pdf(pdf_file)
    
    # Use placeholder OCR for image-based content
    image_text = ""
    for img in images:
        image_text += placeholder_ocr(img) + "\n"
    
    return text, image_text

def combine_text(text, image_text):
    return f"Text from PDF:\n{text}\n\nText from Images:\n{image_text}"
