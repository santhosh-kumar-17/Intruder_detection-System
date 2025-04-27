import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import io

def sharpen_image_from_pixmap(pix):
    # Convert pixmap to bytes
    img_bytes = pix.tobytes("ppm")  # Get image bytes in PPM format
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)

    # Decode with OpenCV
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Apply sharpening kernel
    sharpen_kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
    sharpened_img = cv2.filter2D(img, -1, sharpen_kernel)

    # Convert back to bytes using PIL
    img_pil = Image.fromarray(cv2.cvtColor(sharpened_img, cv2.COLOR_BGR2RGB))
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    buf.seek(0)

    # Create new pixmap from bytes
    new_pix = fitz.Pixmap(buf)
    return new_pix
def convert2_non_editable_pdf(input_path, output_path):
    try:
        doc = fitz.open(input_path)
        new_doc = fitz.open()

        for i in range(len(doc)):
            page = doc[i]
            mat = fitz.Matrix(1, 1)
            pix = page.get_pixmap(matrix=mat, alpha=False)

            # Sharpen the pixmap
            sharp_pix = sharpen_image_from_pixmap(pix)

            # Insert sharpened image into new PDF
            new_page = new_doc.new_page(width=sharp_pix.width, height=sharp_pix.height)
            new_page.insert_image(fitz.Rect(0, 0, sharp_pix.width, sharp_pix.height), pixmap=sharp_pix)

        new_doc.save(output_path)
        print("PDF has been converted to non-editable with sharpened pages.")
        return True

    except Exception as e:
        print("Exception raised in PDF conversion:", str(e))
        return False

input_path = "C:\Users\santh\Downloads\Telegram Desktop\Santhosh_Kumar_MCA.pdf"
outputpath = "C:\Users\santh\Downloads\Telegram Desktop\Santhosh_Kumar_MCA1.pdf"
