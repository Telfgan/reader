import pytesseract
from PIL import Image

from DjangoReader.services.helper import toBase64

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract(path_to_image, language):
    img = Image.open(path_to_image)

    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(
        img,
        lang=language,
        config=custom_config
    )

    return toBase64(text)
