from reportlab.pdfgen import canvas
import os
from reportlab.lib.units import cm

def create_pdf_from_list_of_images(img_dir: str, pdf_file_path: str) -> None:
    """Create pdf from a list of images in a directory.

    Args:
        img_dir (str): Directory containing images.
        pdf_file_path (str): Path where pdf file needs to be created.
    """
    pdf_file = canvas.Canvas(pdf_file_path)
    images_list = sorted(os.listdir(img_dir))
    if len(images_list)>0:
        for image_path in images_list:
            try:
                pdf_file.drawImage(image_path, 0, 200, 20*cm, 18*cm)
                pdf_file.showPage()
            except:
                pass
    pdf_file.save() 